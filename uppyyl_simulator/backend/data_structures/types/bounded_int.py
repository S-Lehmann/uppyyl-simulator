"""An bounded integer data type implementation for Uppaal."""
import typing

from uppyyl_simulator.backend.data_structures.types.base import UppaalIterableMetatype
from uppyyl_simulator.backend.data_structures.types.int import UppaalInt


class UppaalBoundedInt(UppaalInt, metaclass=UppaalIterableMetatype):
    """A Uppaal bounded integer data type."""
    const = False
    meta = False

    bounds = (UppaalInt.INT16_MIN, UppaalInt.INT16_MAX)

    @classmethod
    def make_new_type(cls, name, bounds):
        """Derives a new type from this class.

        Args:
            name: The new type name.
            bounds: The value bounds of the new type.

        Returns:
            The new type.
        """
        new_clazz = typing.cast(cls, UppaalIterableMetatype(name, (cls,), {}))
        new_clazz.set_bounds(bounds)
        return new_clazz

    @classmethod
    def class_iterator(cls):
        """Creates an iterator over the range spanned by the bounds.

        Returns:
            The iterator over interval values.
        """
        return iter(map(lambda v: UppaalInt(v), range(cls.bounds[0], cls.bounds[1] + 1)))

    @classmethod
    def length(cls):
        """Provides the size of the value range.

        Returns:
            The value range size.
        """
        return (cls.bounds[1] - cls.bounds[0]) + 1

    @classmethod
    def set_bounds(cls, bounds=None):
        """Sets the bounds of the UppaalBoundedInt (sub-)class.

        Args:
            bounds: The upper and lower bound values.
        """
        if bounds:
            cls.bounds = (int(bounds[0]), int(bounds[1]))

    def __init__(self, init=None):
        """Initializes UppaalBoundedInt.

        Args:
            init: The initial bounded integer value.
        """
        bounds = self.__class__.bounds
        # Init to 0 if possible, otherwise to lowest possible value within bounds
        val = max(0, bounds[0]) if (init is None) else init
        super().__init__(val)  # TODO: Restructure int data type to avoid duplicate init value assignment

    def get_raw_data(self):
        """Gets the raw data.

        Returns:
            The raw data.
        """
        return self.val

    def assign(self, other):
        """Assigns another value to this bounded int variable object.

        Args:
            other: The assigned value.
        """
        val = int(other)
        bounds = self.__class__.bounds
        if val < bounds[0] or val > bounds[1]:
            raise Exception(f'Value {val} for Uppaal_bounded_int lies outside bounds [{bounds[0]},{bounds[1]}].')
        self.val = val

    def copy(self):
        """Copies the UppaalBoundedInt instance.

        Returns:
            The copied UppaalBoundedInt instance.
        """
        copy_obj = self.__class__(init=self.val)
        return copy_obj

    def _type_quantifier_info_string(self):
        """Generates a string representation of type quantifiers."""
        qualifier_strs = []
        if self.__class__.const:
            qualifier_strs.append("const")
        if self.__class__.meta:
            qualifier_strs.append("meta")
        string = f'[{",".join(qualifier_strs)}]' if qualifier_strs else ''
        return string

    def __repr__(self):
        return f'U({self.__str__()})'

    def __str__(self):
        string = ""
        string += f'{self.val} (\u2208 [{self.bounds[0]},{self.bounds[1]}])'
        return string
