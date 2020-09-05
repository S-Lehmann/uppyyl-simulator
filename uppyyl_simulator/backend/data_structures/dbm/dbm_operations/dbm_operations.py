"""Implementations of supported DBM operations, operation sequences, and corresponding generators."""

import abc
import collections
import re

from uppyyl_simulator.backend.data_structures.dbm.dbm import (
    DBMConstraint, switch_relation
)
from uppyyl_simulator.backend.helper.helper import indent

####################################
# DBM Operation Sequence Generator #
####################################
command_pattern = re.compile(r"(\w+)\((.*)?\) *(\[id *= *(\w+)])?")


class DBMOperationGenerator:
    """A DBM operation generator."""

    def __init__(self):
        """Initializes DBMOperationGenerator."""
        pass

    @staticmethod
    def generate_reset(clock, val):
        """Generates a "reset" DBM operation instance.

        Args:
            clock: The name of the clock to reset.
            val: The reset value.

        Returns:
            A "reset" DBM operation instance.
        """
        return Reset(clock, val)

    @staticmethod
    def generate_constraint(clock1, clock2, rel, val):
        """Generates a "constraint" DBM operation instance.

        Args:
            clock1: The name of the first clock.
            clock2: The name of the second clock.
            rel: The constraint relation (i.e., "<", "<=", ">", ">=", or "==")
            val: The reset value.

        Returns:
            A "constraint" DBM operation instance.
        """
        if rel == "==":
            op_seq = DBMOperationSequence()
            op_seq.append(Constraint(clock1, clock2, "<=", val))
            op_seq.append(Constraint(clock1, clock2, ">=", val))
            return op_seq
        else:
            return Constraint(clock1, clock2, rel, val)

    @staticmethod
    def generate_delay_future():
        """Generates a "delay future" DBM operation instance.

        Returns:
            A "delay future" DBM operation instance.
        """
        return DelayFuture()

    @staticmethod
    def generate_close():
        """Generates a "close" DBM operation instance.

        Returns:
            A "close" DBM operation instance.
        """
        return Close()

    def generate_from_program_line(self, program_line):
        """Derives a DBM operation from a program line.

        Args:
            program_line: The program line.

        Returns:
            The DBM operation instance.
        """
        command_data = self._analyse_program_line(program_line)
        command = command_data["command"]
        args = command_data["args"]

        if command == "DelayFuture":
            return self.generate_delay_future()
        elif command == "Close":
            return self.generate_close()
        elif command == "Reset":
            return self.generate_reset(clock=args[0], val=int(args[1]))
        elif command == "Constraint":
            return self.generate_constraint(clock1=args[0], clock2=args[1], rel=args[2], val=int(args[3]))
        else:
            raise Exception(f'Command type {command} not supported.')

    def generate_from_program(self, program_str):
        """Derives (a sequence of) DBM operations from a program.

        Args:
            program_str: The program text string.

        Returns:
            The DBM operation sequence.
        """
        op_seq = DBMOperationSequence()
        program_lines = program_str.splitlines()
        for program_line in program_lines:
            op = self.generate_from_program_line(program_line)
            op_seq.append(op)

        return op_seq

    @staticmethod
    def _analyse_program_line(program_line):
        """Analyses of single program line regarding command type and arguments.

        Args:
            program_line: The program line.

        Returns:
            Analysis info on command name, arguments, and optional DBM ID.
        """
        command_match = command_pattern.search(program_line)
        if not command_match:
            raise Exception(f'Line "{program_line}" is not a valid command. Abort.')

        command = command_match.group(1)
        arg_part = command_match.group(2)
        dbm_id = command_match.group(4)

        args = list(map(lambda x: x.strip(), arg_part.split(",")))

        return {"command": command, "args": args, "dbm_id": dbm_id}


#################
# DBM Operation #
#################
class DBMOperation(abc.ABC):
    """An abstract DBM operation."""

    def __init__(self):
        """Initializes DBMOperation."""
        pass

    @abc.abstractmethod
    def apply(self, dbm):
        """Applies the DBM operation to a DBM.

        Args:
            dbm: The target DBM.

        Returns:
            The resulting DBM.
        """
        pass


##########################
# DBM Operation Sequence #
##########################
class DBMOperationSequence(DBMOperation, collections.abc.MutableSequence):
    """A DBM operation sequence."""

    def __init__(self):
        """Initializes DBMOperationSequence."""
        super().__init__()
        self.sequence = []

    def apply(self, dbm):
        """Applies the DBM operation sequence to a DBM.

        Args:
            dbm: The target DBM.

        Returns:
            The resulting DBM.
        """
        for operation in self.sequence:
            operation.apply(dbm)
        return dbm

    def __setitem__(self, idx, value):
        self.sequence[idx] = value

    def __getitem__(self, idx_or_slice):
        if isinstance(idx_or_slice, slice):
            sub_seq = DBMOperationSequence()
            sub_seq.sequence = self.sequence[idx_or_slice]
            return sub_seq
        else:
            return self.sequence[idx_or_slice]

    def __delitem__(self, idx):
        del self.sequence[idx]

    def __len__(self):
        return len(self.sequence)

    def __iter__(self):
        return iter(self.get_flattened().sequence)

    def __reversed__(self):
        return reversed(self.get_flattened().sequence)

    def __add__(self, other):
        new_sequence = DBMOperationSequence()
        new_sequence.sequence = self.sequence + other.sequence
        return new_sequence

    def get_flattened_length(self):
        """Gets the summed count of all innermost nested DBM operations.

        Returns:
            The nested sequence length.
        """
        length = 0
        for operation in self.sequence:
            if isinstance(operation, DBMOperationSequence):
                length += operation.get_flattened_length()
            else:
                length += 1
        return length

    def insert(self, idx, val):
        """Inserts a value into the operation sequence at position idx.

        Args:
            idx: The index at which the value is inserted.
            val: The value to insert.

        Returns:
            None
        """
        self.sequence.insert(idx, val)

    def get_flattened(self):
        """Generates a flattened DBM operation sequence (i.e., (multi-)nested sequences are replaced by their elements)

        Returns:
            The flattened DBM operation sequence.
        """
        op_seq = DBMOperationSequence()
        for operation in self.sequence:
            if isinstance(operation, DBMOperationSequence):
                op_seq.extend(operation.get_flattened())
            else:
                op_seq.append(operation)
        return op_seq

    def flatten(self):
        """Flattens the DBM operation sequence.

        Returns:
            None
        """
        self.sequence = self.get_flattened()

    def copy(self):
        """Copies the DBMOperationSequence instance.

        Returns:
            The copied DBMOperationSequence instance.
        """
        copy_obj = DBMOperationSequence()
        for operation in self.sequence:
            op_copy = operation.copy()
            copy_obj.append(op_copy)
        return copy_obj

    def __str__(self):
        op_strs = []
        for operation in self.sequence:
            if isinstance(operation, DBMOperationSequence):
                op_str = indent(str(operation), 2)
            else:
                op_str = f'{operation}'
            op_strs.append(op_str)

        string = "\n".join(op_strs)
        return string


#########
# Reset #
#########
class Reset(DBMOperation):
    """A Reset operation."""

    def __init__(self, clock, val):
        """Initializes Reset.

        Args:
            clock: The name of the clock to reset.
            val: The reset value.
        """
        super().__init__()
        self.clock = clock
        self.val = int(val)

    def apply(self, dbm):
        """Applies the Reset operation to a DBM.

        Args:
            dbm: The target DBM.

        Returns:
            The resulting DBM.
        """
        dbm.reset(self.clock, self.val)
        return dbm

    def copy(self):
        """Copies the Reset instance.

        Returns:
            The copied Reset instance.
        """
        return Reset(self.clock, self.val)

    def __str__(self):
        return f'Reset({self.clock} = {self.val})'


##############
# Constraint #
##############
class Constraint(DBMOperation):  # "<=" constraint
    """A Constraint operation."""

    def __init__(self, clock1, clock2, rel, val):
        """Initializes Constraint.

        Args:
            clock1: The name of the first clock.
            clock2: The name of the second clock.
            rel: The constraint relation (i.e., "<", "<=", ">", ">=", or "==")
            val: The reset value.
        """
        super().__init__()
        if rel == "<=" or rel == "<":
            self.clock1 = clock1
            self.clock2 = clock2
            self.rel = rel
            self.val = int(val)
        elif rel == ">=" or rel == ">":
            self.clock1 = clock2
            self.clock2 = clock1
            self.rel = switch_relation(rel)
            self.val = -int(val)
        else:
            raise Exception(f'Relation "{rel}" not supported for Constraint operation.')

    def apply(self, dbm):
        """Applies the Constraint operation to a DBM.

        Args:
            dbm: The target DBM.

        Returns:
            The resulting DBM.
        """
        dbm_constr = DBMConstraint()
        dbm_constr.clock1 = self.clock1 if self.clock1 else "T0_REF"
        dbm_constr.clock2 = self.clock2 if self.clock2 else "T0_REF"
        dbm_constr.rel = self.rel
        dbm_constr.val = self.val

        dbm.conjugate(dbm_constr)
        return dbm

    def copy(self):
        """Copies the Constraint instance.

        Returns:
            The copied Constraint instance.
        """
        return Constraint(self.clock1, self.clock2, self.rel, self.val)

    def __str__(self):
        clock1 = self.clock1 if self.clock1 else "T0_REF"
        clock2 = self.clock2 if self.clock2 else "T0_REF"
        return f'Constraint({clock1} - {clock2} {self.rel} {self.val})'


###############
# DelayFuture #
###############
class DelayFuture(DBMOperation):
    """A DelayFuture operation."""

    def __init__(self):
        """Initializes DelayFuture."""
        super().__init__()

    def apply(self, dbm):
        """Applies the DelayFuture operation to a DBM.

        Args:
            dbm: The target DBM.

        Returns:
            The resulting DBM.
        """
        dbm.delay_future()
        return dbm

    @staticmethod
    def copy():
        """Copies the DelayFuture instance.

        Returns:
            The copied DelayFuture instance.
        """
        return DelayFuture()

    def __str__(self):
        return f'DelayFuture()'


#########
# Close #
#########
class Close(DBMOperation):
    """A Close operation."""

    def __init__(self):
        """Initializes Close."""
        super().__init__()

    def apply(self, dbm):
        """Applies the Close operation to a DBM.

        Args:
            dbm: The target DBM.

        Returns:
            The resulting DBM.
        """
        dbm.canonicalize()
        return dbm

    @staticmethod
    def copy():
        """Copies the Close instance.

        Returns:
            The copied Close instance.
        """
        return Close()

    def __str__(self):
        return f'Close()'
