"""An clock data type implementation for Uppaal."""
import typing

from uppyyl_simulator.backend.data_structures.types.base import UppaalType


class UppaalClock(UppaalType):
    """A Uppaal clock data type."""

    @classmethod
    def make_new_type(cls, name):
        """Derives a new type from this class.
        Args:
            name: The new type name.

        Returns:
            The new type.
        """
        new_clazz = typing.cast(cls, type(name, (cls,), {}))
        return new_clazz

    def __init__(self, name=None):
        """Initializes UppaalClock.

        Args:
            name: The clock name.
        """
        self.name = name

    @staticmethod
    def get_raw_data():
        """Gets the raw data.

        Returns:
            The raw data.
        """
        return None

    def assign(self, other):
        """Assigns another value to this clock variable object.

        Args:
            other: The assigned value.
        """
        pass

    def copy(self):
        """Copies the UppaalClock instance.

        Returns:
            The copied UppaalClock instance.
        """
        copy_obj = self.__class__(name=self.name)
        return copy_obj

    def __str__(self):
        return f'Uppaal_clock()'
