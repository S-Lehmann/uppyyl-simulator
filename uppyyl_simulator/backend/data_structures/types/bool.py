"""A bool data type implementation for Uppaal."""
import typing

from uppyyl_simulator.backend.data_structures.types.base import UppaalType, BASE_BINARY_OPS


class UppaalBool(UppaalType):
    """A Uppaal bool data type."""
    const = False
    meta = False

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

    def __init__(self, init=None):
        """Initializes UppaalBool.

         Args:
             init: The initial bool value.
         """
        self.val = None
        val = False if (init is None) else init
        self.assign(val)

    def get_raw_data(self):
        """Gets the raw data.

        Returns:
            The raw data.
        """
        return self.val

    def assign(self, other):
        """Assigns another value to this bool variable object.

        Args:
            other: The assigned value.
        """
        self.val = bool(other)

    def apply_binary_op(self, other, op):
        """Applies a binary operation to this bool variable object.

        Args:
            other: The assigned value.
            op: The string identifier of the binary operation.

        Returns:
            The resulting value of the binary operation.
        """
        op_func = BASE_BINARY_OPS[op]
        return UppaalBool(op_func(self.val, bool(other)))

    def copy(self):
        """Copies the UppaalBool instance.

        Returns:
            The copied UppaalBool instance.
        """
        copy_obj = self.__class__(init=self.val)
        return copy_obj

    def __int__(self):
        return int(self.val)

    def __bool__(self):
        return self.val

    def __pos__(self):
        return UppaalBool(self.val)

    def __neg__(self):
        return UppaalBool(-self.val)

    def __add__(self, other):
        return self.apply_binary_op(other, "Add")

    def __sub__(self, other):
        return self.apply_binary_op(other, "Sub")

    def __mul__(self, other):
        return self.apply_binary_op(other, "Mult")

    def __truediv__(self, other):
        return self.apply_binary_op(other, "Div")

    def __mod__(self, other):
        return self.apply_binary_op(other, "Mod")

    def __lshift__(self, other):
        return self.apply_binary_op(other, "LShift")

    def __rshift__(self, other):
        return self.apply_binary_op(other, "RShift")

    def __and__(self, other):
        return self.apply_binary_op(other, "BitAnd")

    def __or__(self, other):
        return self.apply_binary_op(other, "BitOr")

    def __xor__(self, other):
        return self.apply_binary_op(other, "BitXor")

    def __invert__(self):
        return UppaalBool(~self.val)

    def __iadd__(self, other):
        res = self.apply_binary_op(other, "Add")
        self.val = res.val
        return self

    def __isub__(self, other):
        res = self.apply_binary_op(other, "Sub")
        self.val = res.val
        return self

    def __imul__(self, other):
        res = self.apply_binary_op(other, "Mult")
        self.val = res.val
        return self

    def __itruediv__(self, other):
        res = self.apply_binary_op(other, "Div")
        self.val = res.val
        return self

    def __imod__(self, other):
        res = self.apply_binary_op(other, "Mod")
        self.val = res.val
        return self

    def __ilshift__(self, other):
        res = self.apply_binary_op(other, "LShift")
        self.val = res.val
        return self

    def __irshift__(self, other):
        res = self.apply_binary_op(other, "RShift")
        self.val = res.val
        return self

    def __iand__(self, other):
        res = self.apply_binary_op(other, "BitAnd")
        self.val = res.val
        return self

    def __ior__(self, other):
        res = self.apply_binary_op(other, "BitOr")
        self.val = res.val
        return self

    def __ixor__(self, other):
        res = self.apply_binary_op(other, "BitXor")
        self.val = res.val
        return self

    def __lt__(self, other):
        return self.apply_binary_op(other, "LessThan")

    def __le__(self, other):
        return self.apply_binary_op(other, "LessEqual")

    def __eq__(self, other):
        return self.apply_binary_op(other, "Equal")

    def __ne__(self, other):
        return self.apply_binary_op(other, "NotEqual")

    def __gt__(self, other):
        return self.apply_binary_op(other, "GreaterThan")

    def __ge__(self, other):
        return self.apply_binary_op(other, "GreaterEqual")

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
        return f'{self.val}'
