"""A variable implementation for Uppaal."""
import collections

from uppyyl_simulator.backend.data_structures.types.base import UppaalType, BASE_BINARY_OPS


class UppaalVariable(collections.abc.MutableMapping):
    """A Uppaal variable."""

    def __init__(self, name, val=None, scope_path=None, var_path=None):
        self.val = val
        self.scope_path = None
        self.var_path = None
        self.name = name  # TODO: Remove name argument, as it is automatically set via "update_name_from_path()"

        self.update_path(scope_path=scope_path, var_path=var_path)
        self.update_name_from_path()

    def update_path(self, scope_path=None, var_path=None):
        """Updates the path of the variable, e.g., if base variable path changed.

        Args:
            scope_path: The list of scope path segments (e.g., ["constant", "instances", "Inst1"]).
            var_path: The list of variable path segments (e.g., ["c", "field1", 1]).
        """
        if scope_path is not None:
            self.scope_path = scope_path
        if var_path is not None:
            self.var_path = var_path
        if (self.scope_path is not None) and (self.var_path is not None) and hasattr(self.val, "update_paths"):
            self.val.update_paths(scope_path=self.scope_path, base_var_path=self.var_path)
        self.update_name_from_path()

    def update_name_from_path(self):
        """Updates the name of the variable based on the scope path and variable path.

        Returns:
            The new variable name.
        """
        if (self.scope_path is not None) and (self.var_path is not None):
            name = self.var_path[0]
            name += "".join(map(lambda s: f'[{s}]', self.var_path[1:]))
            if self.scope_path[1] == "instances":
                inst_name = self.scope_path[2]
                name = f'{inst_name}.{name}'
            self.name = name

        return self.name

    def get_raw_data(self):
        """Gets the raw data.

        Returns:
            The raw data.
        """
        return self.val.get_raw_data()

    def assign(self, other):
        """Assigns another value to this variable object.

        Args:
            other: The assigned value.
        """
        if isinstance(other, UppaalVariable):
            self.val = other.val.copy()
        elif isinstance(other, UppaalType):
            self.val = other.copy()
        elif hasattr(self.val, "assign"):
            self.val.assign(other)

    def apply_binary_op(self, other, op):
        """Applies a binary operation to the variable.

        Args:
            other: The assigned value.
            op: The string identifier of the binary operation.

        Returns:
            The resulting value of the binary operation.
        """
        op_func = BASE_BINARY_OPS[op]
        return op_func(self.val, other)

    def __setitem__(self, key, value):
        self.val[key] = value

    def __getitem__(self, key):
        return self.val[key]

    def __delitem__(self, key):
        del self.val[key]

    def __iter__(self):
        return iter(self.val)

    def __len__(self):
        return len(self.val)

    def copy(self):
        """Copies the UppaalVariable instance.

        Returns:
            The copied UppaalVariable instance.
        """
        copy_val = self.val.copy() if (self.val is not None) else None
        copy_obj = self.__class__(name=self.name, val=copy_val)
        return copy_obj

    def __int__(self):
        return int(self.val)

    def __bool__(self):
        return bool(self.val)

    def __pos__(self):
        return +self.val

    def __neg__(self):
        return -self.val

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
        return ~self.val

    def __iadd__(self, other):
        res = self.apply_binary_op(other, "Add")
        self.val = res
        return self

    def __isub__(self, other):
        res = self.apply_binary_op(other, "Sub")
        self.val = res
        return self

    def __imul__(self, other):
        res = self.apply_binary_op(other, "Mult")
        self.val = res
        return self

    def __itruediv__(self, other):
        res = self.apply_binary_op(other, "Div")
        self.val = res
        return self

    def __imod__(self, other):
        res = self.apply_binary_op(other, "Mod")
        self.val = res
        return self

    def __ilshift__(self, other):
        res = self.apply_binary_op(other, "LShift")
        self.val = res
        return self

    def __irshift__(self, other):
        res = self.apply_binary_op(other, "RShift")
        self.val = res
        return self

    def __iand__(self, other):
        res = self.apply_binary_op(other, "BitAnd")
        self.val = res
        return self

    def __ior__(self, other):
        res = self.apply_binary_op(other, "BitOr")
        self.val = res
        return self

    def __ixor__(self, other):
        res = self.apply_binary_op(other, "BitXor")
        self.val = res
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
        if self.val and hasattr(self.val, "_type_quantifier_info_string"):
            return getattr(self.val, "_type_quantifier_info_string")()
        else:
            return ""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'Uppaal_var{self._type_quantifier_info_string()}({self.val})'
