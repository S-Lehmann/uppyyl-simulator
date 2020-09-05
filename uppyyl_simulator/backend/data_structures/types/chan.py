"""An channel data type implementation for Uppaal."""
import typing

from uppyyl_simulator.backend.data_structures.types.base import UppaalType


class UppaalChan(UppaalType):
    """A Uppaal channel data type."""
    broadcast = False
    urgent = False

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

    def __init__(self):
        """Initializes UppaalChan."""
        pass

    @staticmethod
    def get_raw_data():
        """Gets the raw data.

        Returns:
            The raw data.
        """
        return None

    def assign(self, other):
        """Assigns another value to this channel variable object.

        Args:
            other: The assigned value.
        """
        pass

    def copy(self):
        """Copies the UppaalChan instance.

        Returns:
            The copied UppaalChan instance.
        """
        copy_obj = self.__class__()
        return copy_obj

    def _type_quantifier_info_string(self):
        """Generates a string representation of type quantifiers."""
        qualifier_strs = []
        if self.__class__.broadcast:
            qualifier_strs.append("broadcast")
        if self.__class__.urgent:
            qualifier_strs.append("urgent")
        string = f'[{",".join(qualifier_strs)}]' if qualifier_strs else ''
        return string

    def __str__(self):
        return f'Uppaal_chan{self._type_quantifier_info_string()}()'
