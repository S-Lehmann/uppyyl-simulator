"""The base classes for data type implementation for Uppaal."""

import abc
from enum import Enum
import typing


BASE_BINARY_OPS = {
    "Add": lambda x, y: x + y,
    "Sub": lambda x, y: x - y,
    "Mult": lambda x, y: x * y,
    "Div": lambda x, y: x / y,
    "Mod": lambda x, y: x % y,
    "LShift": lambda x, y: x << y,
    "RShift": lambda x, y: x >> y,
    "BitAnd": lambda x, y: x & y,
    "BitOr": lambda x, y: x | y,
    "BitXor": lambda x, y: x ^ y,

    "LessThan": lambda x, y: x < y,
    "LessEqual": lambda x, y: x <= y,
    "Equal": lambda x, y: x == y,
    "NotEqual": lambda x, y: x != y,
    "GreaterThan": lambda x, y: x > y,
    "GreaterEqual": lambda x, y: x >= y,
}


class TypeQualifier(Enum):
    """An enum of possible type qualifiers."""
    CONST = 1
    META = 2
    BROADCAST = 3
    URGENT = 4


class UppaalType(abc.ABC):
    """
    UppaalType
    """
    @abc.abstractmethod
    def copy(self):
        """Copies the UppaalType instance."""


class UppaalIterableMetatype(abc.ABCMeta, typing.Sized):
    """
    UppaalIterableMetatype
    """

    @abc.abstractmethod
    def class_iterator(cls):
        """Creates an iterator over the class.

        Returns:
            The iterator.
        """
        pass

    @abc.abstractmethod
    def length(cls):
        """Provides the amount of values yielded by the class iterator.

        Returns:
            The amount of values yielded by the class iterator.
        """
        pass

    def __iter__(cls):
        return cls.class_iterator()

    def __len__(cls):
        return cls.length()
