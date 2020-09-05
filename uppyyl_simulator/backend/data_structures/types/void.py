"""A void data type implementation for Uppaal."""
import typing

from uppyyl_simulator.backend.data_structures.types.base import UppaalType


class UppaalVoid(UppaalType):
    """A Uppaal void data type."""

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

    @staticmethod
    def get_raw_data():
        """Gets the raw data.

        Returns:
            The raw data.
        """
        return None

    def __init__(self):
        """Initializes UppaalVoid."""
        pass

    def copy(self):
        """Copies the UppaalVoid instance.

        Returns:
            The copied UppaalVoid instance.
        """
        copy_obj = self.__class__()
        return copy_obj
