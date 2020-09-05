"""A struct data type implementation for Uppaal."""

import collections

from uppyyl_simulator.backend.data_structures.state.variable import UppaalVariable
from uppyyl_simulator.backend.data_structures.types.base import UppaalType


class UppaalStruct(collections.abc.MutableMapping, UppaalType):
    """A Uppaal struct data type."""
    const = False
    meta = False
    field_types = []

    @classmethod
    def make_new_type(cls, name, field_classes):
        """Derives a new type from this class.

        Args:
            name: The new type name.
            field_classes: The field classes of the new type.

        Returns:
            The new type.
        """
        new_clazz = type(name, (cls,), {})
        new_clazz.field_types = field_classes
        return new_clazz

    def __init__(self, init=None):
        """Initializes UppaalStruct."""
        self.fields = {}
        for field_name, field_class in self.__class__.field_types:
            field_var = UppaalVariable(name=field_name, val=field_class())
            self.fields[field_name] = field_var

        if init is not None:
            self.assign(vals=init)

    def update_paths(self, scope_path, base_var_path):
        """Updates the paths of the contained variables, e.g., if base path changed.

        Args:
            scope_path: The list of scope path segments (e.g., ["constant", "instances", "Inst1"]).
            base_var_path: The list of variable path segments (e.g., ["c", "field1", 1]).
        """
        for i, (field_key, field_var) in enumerate(self.fields.items()):
            sub_var_path = base_var_path.copy()
            sub_var_path.append(field_key)
            field_var.update_path(scope_path=scope_path, var_path=sub_var_path)
            field_var.update_name_from_path()

    # def update_names(self, base_name):
    #     """Updates the names of the contained variables, e.g., if base variable name or location changed.
    #
    #     Args:
    #         base_name: The base name (e.g., "x[0]" results in "x[0].field1", "x[0].field2", ... as element names)
    #     """
    #     for i, (field_key, field_var) in enumerate(self.fields.items()):
    #         name = f'{base_name}.{field_key}'
    #         field_var.update_name(name=name)

    def get_raw_data(self):
        """Gets the raw data.

        Returns:
            The raw data.
        """
        vals = {}
        for i, (field_key, field_var) in enumerate(self.fields.items()):
            vals[field_key] = field_var.get_raw_data()
        return vals

    def assign(self, vals):
        """Assigns other values to the variables in the struct.

        Args:
            vals: The assigned values.
        """
        assert len(vals) == len(self.fields)  # __dict__
        for i, (field_key, field_var) in enumerate(self.fields.items()):
            field_var.assign(vals[i])

    def assign_from(self, other):
        """Assign corresponding values from another struct to the individual struct elements.

        Args:
            other: The other Uppaal array.
        """
        self.assign(list(other.fields.values()))

    def copy(self):
        """Copies the UppaalStruct instance.

        Returns:
            The copied UppaalStruct instance.
        """
        copy_obj = self.__class__()
        copy_obj.assign_from(self)
        return copy_obj

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __getitem__(self, key):
        return self.fields[key]

    def __delitem__(self, key):
        del self.fields[key]

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

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
        return f'U{self.__str__()}'

    def __str__(self):
        string = ', '.join(map(lambda kv: f"'{kv[0]}':{kv[1].val}", self.fields.items()))
        string = f'{{{string}}}'

        return string
