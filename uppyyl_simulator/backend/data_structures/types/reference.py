"""A reference data type implementation for Uppaal."""

from uppyyl_simulator.backend.data_structures.types.base import UppaalType


class UppaalReference(UppaalType):
    """A Uppaal reference data type."""
    const = False

    def __init__(self, pointee_path):
        """Initializes UppaalReference.

        Args:
            pointee_path: The targeted pointee path (e.g., ["constant", "instances", "Inst1", "c", 1] for the variable
                          "c[1]" in the constant instance scope of "Inst1").
        """
        self.pointee_path = pointee_path
        self.pointee = None

    def get_raw_data(self):
        """Gets the raw data.

        Returns:
            The raw data.
        """
        if self.pointee is None:
            raise Exception("Cannot get raw data value from un-initialized reference.")
        return self.pointee.get_raw_data()

    def init_pointee(self, program_state):
        """Initializes the reference pointee using its path.

        Args:
            program_state: The program state dict on which the path should be resolved.
        """
        var = program_state
        for path_part in self.pointee_path:
            var = var[path_part]

        if isinstance(var, UppaalReference):
            self.pointee = var.pointee
        else:
            self.pointee = var

    def assign(self, other):
        """Assigns another value to the pointee variable.

        Args:
            other: The assigned value.
        """
        self.pointee.assign(other)

    def apply_binary_op(self, other, op):
        """Applies a binary operation to the pointee variable.

        Args:
            other: The assigned value.
            op: The string identifier of the binary operation.

        Returns:
            The resulting value of the binary operation.
        """
        return self.pointee.apply_binary_op(other, op)

    def copy(self):
        """Copies the UppaalReference instance.

        Returns:
            The copied UppaalReference instance.
        """
        copy_obj = self.__class__(pointee_path=self.pointee_path)
        return copy_obj

    def __int__(self):
        return int(self.pointee)

    def __bool__(self):
        return bool(self.pointee)

    def __neg__(self):
        return -self.pointee

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
        return ~self.pointee

    def __iadd__(self, other):
        self.apply_binary_op(other, "Add")
        return self.pointee

    def __isub__(self, other):
        self.apply_binary_op(other, "Sub")
        return self.pointee

    def __imul__(self, other):
        self.apply_binary_op(other, "Mult")
        return self.pointee

    def __itruediv__(self, other):
        self.apply_binary_op(other, "Div")
        return self.pointee

    def __imod__(self, other):
        self.apply_binary_op(other, "Mod")
        return self.pointee

    def __ilshift__(self, other):
        self.apply_binary_op(other, "LShift")
        return self.pointee

    def __irshift__(self, other):
        self.apply_binary_op(other, "RShift")
        return self.pointee

    def __iand__(self, other):
        self.apply_binary_op(other, "BitAnd")
        return self.pointee

    def __ior__(self, other):
        self.apply_binary_op(other, "BitOr")
        return self.pointee

    def __ixor__(self, other):
        self.apply_binary_op(other, "BitXor")
        return self.pointee

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
