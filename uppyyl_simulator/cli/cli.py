"""This module implements a CLI for the Uppyyl Simulator."""

import argparse
import glob
import os
import re
import readline
import shlex
from cmd import Cmd
from enum import Enum

from colorama import Fore, Back

from uppyyl_simulator.backend.simulator.simulator import Simulator

readline.set_completer_delims(' \t\n')


##############################
# Helper Classes and Objects #
##############################
class ArgumentParserError(Exception):
    """Exception raised for argument parsing errors."""
    pass


class ArgumentParser(argparse.ArgumentParser):
    """A helper subclass of argparse.ArgumentParser that disables exiting the program on parsing errors."""

    def error(self, message):
        """The overwritten error function which is called when an argument parsing error occurs.

        Args:
            message: The error message.
        """
        usage = self.format_usage()[:-1]
        raise ArgumentParserError(f'{message} ({usage})')


load_parser = ArgumentParser(prog='load', add_help=False)
load_parser.add_argument('filepath', metavar='filepath')

transition_pattern = re.compile(r't(\d+)')


class View(Enum):
    """An enum for the possible graphical views."""
    STATE = 1
    OP_SEQ = 2


def _complete_path(path):
    if os.path.isdir(path):
        return False, glob.glob(os.path.join(path, '*'))
    else:
        return True, glob.glob(path + '*')


########################
# Uppyyl Simulator CLI #
########################
class UppyylSimulatorCLI(Cmd):
    """A CLI for the Uppyyl Simulator."""

    prompt = 'uppyyl_simulator> '
    intro = ""

    def __init__(self):
        """Initializes UppyylSimulatorCLI."""
        super(UppyylSimulatorCLI, self).__init__()
        self.uppaal_simulator = Simulator()
        self.active_trans_idx = 0
        self.active_view = View.STATE

        init_model = "./res/models/example_system.xml"
        self.uppaal_simulator.load_system(system_path=init_model)

        help_message = "This is the Uppyyl Simulator CLI. Type ? to list commands."
        self.print_view(message=help_message)

    def print_state_view(self, message=""):
        """Prints the state view.

        Args:
            message: An optional information message.
        """
        trace_string = self.get_trace_string()
        state_string = self.get_state_string()
        transition_string = self.get_transitions_string()

        self.clear()
        print(f'{Fore.BLUE}Message:{Fore.RESET} {message}')
        print(f'\n--| {Fore.BLUE}Trace{Fore.RESET} |----------------------------')
        print(trace_string)
        print(f'\n--| {Fore.BLUE}State{Fore.RESET} |----------------------------')
        print(state_string)
        print(f'\n--| {Fore.BLUE}Transitions{Fore.RESET} |----------------------')
        print(transition_string)
        print(f'')

    def print_op_seq_view(self, message=""):
        """Prints the operation sequence view.

        Args:
            message: An optional information message.
        """
        op_seq_string = self.get_operation_sequence_string()

        self.clear()
        print(f'{Fore.BLUE}Message:{Fore.RESET} {message}')
        print(f'\n--| {Fore.BLUE}Operation Sequence{Fore.RESET} |----------------------------\n')
        print(op_seq_string)
        print(f'')

    def print_view(self, message=""):
        """Prints the current view.

        Args:
            message: An optional information message.
        """
        if self.active_view == View.STATE:
            self.print_state_view(message=message)
        elif self.active_view == View.OP_SEQ:
            self.print_op_seq_view(message=message)

    def get_trace_string(self):
        """Constructs the string representation of the trace.

        Returns:
            The trace string.
        """
        trace_strs = []
        for i, trace in enumerate(self.uppaal_simulator.transition_trace):
            if i == self.active_trans_idx:
                trace_strs.append(f'{Back.LIGHTBLACK_EX}{i}:{trace.short_string()}{Back.RESET}')
            else:
                trace_strs.append(f'{i}:{trace.short_string()}')
        string = " -> ".join(trace_strs)
        return string

    def get_state_string(self):
        """Constructs the string representation of the state.

        Returns:
            The state string.
        """
        state = self.uppaal_simulator.transition_trace[self.active_trans_idx].target_state
        string = ""
        string += f'{Fore.BLUE}Variables:{Fore.RESET} {state.get_variable_state_string()}\n'
        curr_loc_strs = []
        for inst_name, loc in state.location_state.items():
            curr_loc_strs.append(f'{inst_name}: {loc.name if loc.name else "_"} ({loc.id})')
        string += f'{Fore.BLUE}Locations:{Fore.RESET} {" | ".join(curr_loc_strs)}\n'
        string += f'{Fore.BLUE}DBM:{Fore.RESET}\n'
        string += str(state.dbm_state)
        return string

    def get_transitions_string(self):
        """Constructs the string representation of the transitions.

        Returns:
            The transitions string.
        """
        state = self.uppaal_simulator.transition_trace[self.active_trans_idx].target_state
        transitions = state.transitions
        trans_strs = []
        for i, trans in enumerate(transitions):
            trans_strs.append(f't{i + 1}: {trans.short_string()}')
        string = "\n".join(trans_strs)
        return string

    def get_operation_sequence_string(self):
        """Constructs the string representation of the operation sequence.

        Returns:
            The operation sequence string.
        """
        op_strs = []
        max_line_length = 0
        for trans in self.uppaal_simulator.transition_trace[:self.active_trans_idx + 1]:
            trans_op_strs = []
            flattened_op_seq = trans.dbm_op_sequence.get_flattened()
            for i, op in enumerate(flattened_op_seq):
                op_str = str(op)
                max_line_length = max(max_line_length, len(op_str))
                trans_op_strs.append(op_str)
            op_strs.append((trans.short_string(), trans_op_strs))

        line_strs = []
        colors = [Back.LIGHTBLACK_EX, Back.BLACK]
        color_idx = 0
        for trans_idx, (trans_str, trans_op_strs) in enumerate(op_strs):
            color = colors[color_idx]
            if not trans_op_strs:
                continue
                # line_strs.append(f'{color}{"".ljust(max_line_length + 2)}{Back.RESET} | {trans_idx}:{trans_str}')
            else:
                for i, op_str in enumerate(trans_op_strs):
                    if i == 0:
                        line_strs.append(f'{color}{op_str.ljust(max_line_length + 2)}{Back.RESET} |'
                                         f' {trans_idx}:{trans_str}')
                    else:
                        line_strs.append(f'{color}{op_str.ljust(max_line_length + 2)}{Back.RESET} |')
            color_idx = (color_idx + 1) % len(colors)
        string = "\n".join(line_strs)
        return string

    @staticmethod
    def do_exit(_arg=None):
        """Performs the "exit" command."""
        return True

    @staticmethod
    def help_exit():
        """Shows help for the "exit" command."""
        print('Exits the application. Shorthand: x, q, or Ctrl-D.')

    def do_load(self, arg):
        """Performs the "load" command."""
        args = shlex.split(arg)
        try:
            parsed_args = load_parser.parse_args(args)
        except ArgumentParserError as e:
            self.print_view(message=f'{Fore.RED}{e}{Fore.RESET}')
            return

        model_path = parsed_args.filepath
        try:
            with open(model_path) as file:
                uppaal_test_model_str = file.read()
            self.uppaal_simulator.set_system(uppaal_test_model_str)
            self.active_trans_idx = 0
            self.print_view(message=f'Model "{model_path}" loaded successfully.')
        except FileNotFoundError as e:
            self.print_view(message=f'{Fore.RED}{e}{Fore.RESET}')

    @staticmethod
    def complete_load(text, _line, _start_idx, _end_idx):
        """Autocompletes the path argument of the "load" command."""
        if text[0] in ['"', "'"]:
            is_file, choices = _complete_path(text[1:])
            choices = list(map(lambda p: text[0] + p, choices))
            if len(choices) == 1 and is_file:
                choices[0] += text[0]
        else:
            is_file, choices = _complete_path(text)
        return choices

    @staticmethod
    def help_load():
        """Shows help for the "load" command."""
        load_parser.print_help()

    def do_state(self, _):
        """Performs the "state" command."""
        self.active_view = View.STATE
        self.print_view(message=f'Switched to state view.')

    @staticmethod
    def help_state():
        """Shows help for the "state" command."""
        print('Switches to state view.')

    def do_seq(self, _):
        """Performs the "seq" command."""
        self.active_view = View.OP_SEQ
        self.print_view(message=f'Switched to operation sequence view.')

    @staticmethod
    def help_seq():
        """Shows help for the "seq" command."""
        print('Switches to operation sequence view.')

    def do_g(self, arg):
        """Performs the "g" (goto) command."""
        args = shlex.split(arg)
        trans_idx = int(args[0])
        max_idx = len(self.uppaal_simulator.transition_trace) - 1
        self.active_trans_idx = max(0, min(max_idx, trans_idx))
        self.print_view(message=f'Goto transition {self.active_trans_idx}.')

    @staticmethod
    def help_g():
        """Shows help for the "g" command."""
        print('Goto transition n.')

    def do_f(self, arg):
        """Performs the "f" (forward) command."""
        args = shlex.split(arg)
        step_num = int(args[0]) if args else 1
        max_idx = len(self.uppaal_simulator.transition_trace) - 1
        self.active_trans_idx = min(max_idx, self.active_trans_idx + step_num)
        self.print_view(message=f'Stepped forward to transition {self.active_trans_idx}.')

    @staticmethod
    def help_f():
        """Shows help for the "f" command."""
        print('Steps n transitions forwards (default: n=1).')

    def do_b(self, arg):
        """Performs the "b" (backward) command."""
        args = shlex.split(arg)
        step_num = int(args[0]) if args else 1
        self.active_trans_idx = max(0, self.active_trans_idx - step_num)
        self.print_view(message=f'Stepped backward to transition {self.active_trans_idx}.')

    @staticmethod
    def help_b():
        """Shows help for the "b" command."""
        print('Steps n transitions backwards (default: n=1).')

    def do_r(self, arg):
        """Performs the "r" (random transition(s)) command."""
        args = shlex.split(arg)
        step_num = int(args[0]) if args else 1
        self.uppaal_simulator.revert_to_state_by_index(self.active_trans_idx)
        for i in range(0, step_num):
            self.uppaal_simulator.simulate_step()
        self.active_trans_idx = len(self.uppaal_simulator.transition_trace) - 1
        self.print_view(message=f'{step_num} transitions executed successfully.')

    @staticmethod
    def help_r():
        """Shows help for the "r" command."""
        print('Executes n random transitions (default: n=1).')

    @staticmethod
    def clear():
        """Clears the console."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def emptyline(self):
        """Performs an empty command."""
        self.print_view(message=f'')

    def default(self, inp):
        """Performs a "default" command (i.e., no specific "do_..." function exists)."""
        # Exit
        if inp == 'x' or inp == 'q':
            return self.do_exit()

        # Transition (short command via "t_")
        res = transition_pattern.match(inp)
        if res:
            trans_num = int(res.group(1))
            self.uppaal_simulator.revert_to_state_by_index(self.active_trans_idx)
            if trans_num > len(self.uppaal_simulator.transitions):
                self.print_view(message=f'Transition "{inp}" does not exist.')
                return
            trans = self.uppaal_simulator.transitions[trans_num - 1]
            self.uppaal_simulator.execute_transition(trans)
            self.active_trans_idx = len(self.uppaal_simulator.transition_trace) - 1
            self.print_view(message=f'Transition "{trans.short_string()}" executed successfully.')
            return

        self.print_view(message=f'')

    do_EOF = do_exit
    help_EOF = help_exit
