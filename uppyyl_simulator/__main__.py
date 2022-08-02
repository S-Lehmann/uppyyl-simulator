"""The main entry point of the Uppyyl Simulator module."""

from uppyyl_simulator.cli.cli import UppyylSimulatorCLI


def main():
    """The main function."""
    prompt = UppyylSimulatorCLI()
    prompt.cmdloop()


if __name__ == '__main__':
    main()
