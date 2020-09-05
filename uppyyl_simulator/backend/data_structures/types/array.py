"""An array data type implementation for Uppaal."""

import collections
import typing

from uppyyl_simulator.backend.data_structures.state.variable import UppaalVariable
from uppyyl_simulator.backend.data_structures.types.base import UppaalType
from uppyyl_simulator.backend.data_structures.types.bounded_int import UppaalBoundedInt
from uppyyl_simulator.backend.data_structures.types.scalar import UppaalScalar


class UppaalArray(collections.abc.Sequence, UppaalType):
    """A Uppaal array data type."""
    const = False
    meta = False

    clazz = None
    dim = None
    start = None

    @classmethod
    def make_new_type(cls, name, dims, clazz):
        """Derives a new type from this class.

        Args:
            name: The new type name.
            dims: The dimensions of the new array type.
            clazz: The base clazz of the new array type values.

        Returns:
            The new type.
        """
        if len(dims) > 1:
            clazz = cls.make_new_type(name, dims[1:], clazz)
        new_clazz = typing.cast(cls, type(name, (cls,), {}))
        new_clazz.clazz = clazz
        new_clazz.set_dim(dims[0])
        return new_clazz

    @classmethod
    def set_dim(cls, dim_obj):
        """Sets the dimension of the UppaalArray (sub-)class.

        Args:
            dim_obj: The target dimension. If the dimension object is a bounded integer or scalar type, its class length
                     is used to determine the array size (e.g., a size of 4 for int[0,3]).
        """
        if isinstance(dim_obj, type):
            if issubclass(dim_obj, UppaalBoundedInt):
                cls.dim = len(dim_obj)
                cls.start = dim_obj.bounds[0]
            elif issubclass(dim_obj, UppaalScalar):
                cls.dim = len(dim_obj)
                cls.start = 0
                raise Exception("Array indexed by scalar not implemented yet.")
        else:
            cls.dim = int(dim_obj)
            cls.start = 0

    def __init__(self, init=None):
        """Initializes UppaalArray."""
        clazz = self.__class__.clazz
        dim = self.__class__.dim

        self.data = []
        for i in range(0, dim):
            elem_var = UppaalVariable(name=None, val=clazz())
            self.data.append(elem_var)

        if init is not None:
            self.assign(vals=init)

    def __getitem__(self, idx):
        start = self.__class__.start
        return self.data[idx - start]

    def __len__(self):
        return len(self.data)

    def update_paths(self, scope_path, base_var_path):
        """Updates the paths of the contained variables, e.g., if base path changed.

        Args:
            scope_path: The list of scope path segments (e.g., ["constant", "instances", "Inst1"]).
            base_var_path: The list of variable path segments (e.g., ["c", "field1", 1]).
        """
        for i, list_var in enumerate(self.data):
            sub_var_path = base_var_path.copy()
            sub_var_path.append(i)
            list_var.update_path(scope_path=scope_path, var_path=sub_var_path)
            list_var.update_name_from_path()

    # def update_names(self, base_name):
    #     """Updates the names of the contained variables, e.g., if base variable name or location changed.
    #
    #     Args:
    #         base_name: The base name (e.g., "x[0]" results in "x[0][0]", "x[0][1]", ... as element names)
    #     """
    #     for i, list_var in enumerate(self.data):
    #         name = f'{base_name}[{i}]'
    #         list_var.update_name(name=name)

    def get_raw_data(self):
        """Gets the raw data.

        Returns:
            The raw data.
        """
        vals = []
        for i, list_var in enumerate(self.data):
            vals.append(list_var.get_raw_data())
        return vals

    def assign(self, vals):
        """Assigns other values to the variables in the array.

        Args:
            vals: The assigned values.
        """
        for i, list_var in enumerate(self.data):
            list_var.assign(vals[i])

    def assign_from(self, other):
        """Assign corresponding values from another array to the individual array elements.

        Args:
            other: The other Uppaal array.
        """
        self.assign(other.data)

    def copy(self):
        """Copies the UppaalArray instance.

        Returns:
            The copied UppaalArray instance.
        """
        copy_obj = self.__class__()
        copy_obj.assign_from(self)
        return copy_obj

    def __eq__(self, other):
        if not isinstance(other, UppaalArray):
            raise Exception("For UppaalArray comparison, both operands must be of type UppaalArray.")
        eq = len(self.data) == len(other.data) and all(map(lambda so: so[0] == so[1], zip(self.data, other.data)))
        return eq

    def __ne__(self, other):
        neq = not (self == other)
        return neq

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
        string = ""
        string += f'[{", ".join(map(lambda v: str(v.val), self.data))}]'
        return string
