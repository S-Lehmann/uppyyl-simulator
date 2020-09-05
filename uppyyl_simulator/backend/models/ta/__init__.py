"""This module provides all Uppaal (N)TA related classes."""

from .nta import System
from .ta import Template, Location, Edge

from .labels.assignment import Reset, Update
from .labels.invariant import Invariant
from .labels.parameter import Parameter
from .labels.guard import ClockGuard, VariableGuard
from .labels.sync import Synchronization
from .labels.select import Select
