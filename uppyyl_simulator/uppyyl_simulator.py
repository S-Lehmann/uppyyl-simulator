"""This module provides the CLI entry point via main().
"""

__version__ = "0.1.0"

from .cli.cli import UppyylSimulatorCLI


def main():
    """The main function."""
    prompt = UppyylSimulatorCLI()
    prompt.cmdloop()
