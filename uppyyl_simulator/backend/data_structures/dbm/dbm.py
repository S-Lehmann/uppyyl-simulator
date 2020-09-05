"""A difference bound matrix (DBM) implementation."""

import random
import re

import numpy as np

from uppyyl_simulator.backend.models.graph.weighted_graph import WeightedGraph


##########
# Helper #
##########
def floyd_warshall(matrix):
    """Applies the Floyd-Warshall shortest paths algorithm to a DBM matrix.

    Args:
        matrix: The DBM matrix.

    Returns:
        The closed form of the DBM matrix.
    """
    for k in range(0, len(matrix)):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                if i != j:
                    new_entry = matrix[i][k] + matrix[k][j]
                    if new_entry < matrix[i][j]:
                        matrix[i][j] = new_entry
    return matrix


def switch_relation(rel):
    """Switches the relation string (e.g., turns "<" into ">", and "<=" into ">=")

    Args:
        rel: The relation string.

    Returns:
        The switched relation string.
    """
    if rel == '<':
        return '>'
    if rel == '<=':
        return '>='
    if rel == '>=':
        return '<='
    if rel == '>':
        return '<'
    else:
        raise Exception("Unknown relation type.")


#############
# DBM Entry #
#############
class DBMEntry:
    """A DBM entry."""

    def __init__(self, val, rel):
        """Initializes DBMEntry.

        Args:
            val: The value of the DBM entry.
            rel: The relation string of the DBM entry (i.e., "<" or "<=").
        """
        self.val = val
        self.rel = rel

    def __add__(self, other):
        rel = '<=' if (self.rel == '<=' and other.rel == '<=') else '<'
        return DBMEntry(self.val + other.val, rel)

    def __lt__(self, other):
        return ((self.val < other.val) or
                ((self.val == other.val) and self.rel == "<" and other.rel == "<="))

    def __le__(self, other):
        return ((self.val < other.val) or
                ((self.val == other.val) and (self.rel == "<" or other.rel == "<=")))

    def __eq__(self, other):
        if self.rel == other.rel and self.val == other.val:
            return True
        return False

    def __ne__(self, other):
        if self.rel != other.rel or self.val != other.val:
            return True
        return False

    def __gt__(self, other):
        return ((self.val > other.val) or
                ((self.val == other.val) and self.rel == "<=" and other.rel == "<"))

    def __ge__(self, other):
        return ((self.val > other.val) or
                ((self.val == other.val) and (self.rel == "<=" or other.rel == "<")))

    def copy(self):
        """Copies the DBMEntry instance.

        Returns:
            The copied DBMEntry instance.
        """
        copy_obj = DBMEntry(self.val, self.rel)
        return copy_obj

    def __repr__(self):
        return f'({self.val},{self.rel})'


##################
# DBM Constraint #
##################
class DBMConstraint:
    """A DBM constraint of the form "clock - clock2 (<|<=|>=|>) val"."""

    constr_pattern = re.compile(r"([\w.()\[\]]*)? *(?:[+-]* *([\w.()\[\]]*)? *)?(<=|>=|==|<|>) *([\w-]*)")

    def __init__(self, constr_text=None):
        """Initializes DBMConstraint.

        Args:
            constr_text: The text representation of a constraint "clock - clock2 (<|<=|>=|>) val".
        """
        self.clock1 = None
        self.clock2 = None
        self.rel = None
        self.val = None

        if constr_text:
            self.parse(constr_text)

    def parse(self, constr_text):
        """Parses the constraint text and extracts clock names, relation, and value.

        Args:
            constr_text: The text representation of a constraint "clock - clock2 (<|<=|>=|>) val".

        Returns:
            The constraint data.
        """
        res = self.constr_pattern.match(constr_text)

        if not res:
            raise Exception("DBM constraint \"{}\" cannot be parsed.".format(constr_text))

        self.clock1 = res.group(1)
        self.clock2 = "T0_REF" if (res.group(2) == "") else res.group(2)
        self.rel = res.group(3)
        self.val = int(res.group(4))

        if self.rel == ">" or self.rel == ">=":
            self.invert()

        return {"clock1": self.clock1, "clock2": self.clock2, "rel": self.rel, "val": self.val}

    def invert(self):
        """Inverts the DBMConstraint instance (e.g., turns "clock1 - clock2 <= val" into "clock2 - clock1 >= -val").

        Returns:
            None
        """
        clock_temp = self.clock1
        self.clock1 = self.clock2
        self.clock2 = clock_temp
        self.rel = switch_relation(self.rel)
        self.val = -self.val

    def copy(self):
        """Copies the DBMConstraint instance.

        Returns:
            The copied DBMConstraint instance.
        """
        copy_obj = DBMConstraint()

        copy_obj.clock1 = self.clock1
        copy_obj.clock2 = self.clock2
        copy_obj.rel = self.rel
        copy_obj.val = self.val

        return copy_obj

    def __repr__(self):
        return f"{self.clock1} - {self.clock2} {self.rel} {self.val}"


############
# Interval #
############
class Interval:
    """A value interval."""

    def __init__(self, lower_incl, lower_val, upper_val, upper_incl):
        """Initializes Interval.

        Args:
            lower_incl: Choose whether lower bound is included.
            lower_val: The lower bound value.
            upper_val: The upper bound value.
            upper_incl: Choose whether upper bound is included.
        """
        lower_incl = lower_incl == "[" or (lower_incl and isinstance(lower_incl, bool))
        upper_incl = upper_incl == "]" or (upper_incl and isinstance(upper_incl, bool))

        # TODO: Handle invalid intervals
        # if (upper_val < lower_val) or ((upper_val == lower_val) and (not lower_incl or not upper_incl)):
        #     raise Exception(f'Upper bound lies below lower bound.')

        self.lower_val = lower_val
        self.lower_incl = lower_incl
        self.upper_val = upper_val
        self.upper_incl = upper_incl

    def intersect(self, other):
        """Intersects the instance with another DBM interval.

        Args:
            other: The other DBM interval.

        Returns:
            None
        """
        if self.lower_val == other.lower_val:
            lower_val = self.lower_val
            lower_incl = self.lower_incl and other.lower_incl
        elif self.lower_val < other.lower_val:
            lower_val = other.lower_val
            lower_incl = other.lower_incl
        else:
            lower_val = self.lower_val
            lower_incl = self.lower_incl

        if self.upper_val == other.upper_val:
            upper_val = self.upper_val
            upper_incl = self.upper_incl and other.upper_incl
        elif self.upper_val > other.upper_val:
            upper_val = other.upper_val
            upper_incl = other.upper_incl
        else:
            upper_val = self.upper_val
            upper_incl = self.upper_incl

        if (upper_val < lower_val) or ((upper_val == lower_val) and (not lower_incl or not upper_incl)):
            raise Exception(f'Upper bound lies below lower bound.')

        self.lower_val = lower_val
        self.lower_incl = lower_incl
        self.upper_val = upper_val
        self.upper_incl = upper_incl

        return self

    def is_empty(self):
        """Checks if the DBM interval is empty.

        Returns:
            The emptiness checking result.
        """
        return ((self.upper_val < self.lower_val) or
                ((self.upper_val == self.lower_val) and
                 (not self.lower_incl or not self.upper_incl)))

    def get_random(self):
        """Provides a random integer value drawn from the interval.

        Returns:
            The random integer value.
        """
        lower_val = self.lower_val if self.lower_incl else self.lower_val + 1
        upper_val = self.upper_val if self.upper_incl else self.upper_val - 1
        if upper_val < lower_val:
            raise Exception(f'No integer lies in interval for random draw.')
        return random.randint(lower_val, upper_val)

    def __eq__(self, other):
        if (self.lower_val == other.lower_val and
                self.lower_incl == other.lower_incl and
                self.upper_val == other.upper_val and
                self.upper_incl == other.upper_incl):
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        obj_str = ""
        obj_str += "[" if self.lower_incl else "("
        obj_str += str(self.lower_val)
        obj_str += ", "
        obj_str += str(self.upper_val)
        obj_str += "]" if self.upper_incl else ")"

        return obj_str


############################
# Difference Bounds Matrix #
############################
class DBM:
    """A difference bound matrix (DBM)."""

    def __init__(self, clocks, add_ref_clock=True, zero_init=False):
        """Initializes DBM.

        Args:
            clocks: A list of clock names based on which the DBM is created.
            add_ref_clock: Optionally adds the artificial reference clock "T0_REF" to the DBM.
            zero_init: Optionally initializes all DBM entries to 0 (e.g., as in Uppaal).
        """
        self.clocks = clocks.copy()  # ['T0_REF', 'T0_GLOBAL']
        if add_ref_clock:
            self.clocks.insert(0, "T0_REF")
        self.matrix = None
        self.init_matrix(zero_init=zero_init)

    def init_matrix(self, zero_init=False):
        """Initializes the value matrix.

        Args:
            zero_init: Optionally initializes all DBM entries to 0 (e.g., as in Uppaal).
        """
        clock_num = len(self.clocks)
        if zero_init:
            self.matrix = [[DBMEntry(0, '<=') for _ in range(clock_num)] for _ in range(clock_num)]
        else:
            self.matrix = [[DBMEntry(np.inf, '<') for _ in range(clock_num)] for _ in range(clock_num)]
            for i in range(clock_num):
                self.matrix[i][i] = DBMEntry(0, '<=')

    def get_interval(self, clock):
        """Provides the value interval for a given clock.

        Args:
            clock: The clock for which the interval is requested.

        Returns:
            The value interval.
        """
        clock_index = self.clocks.index(clock)

        lower = self.matrix[0][clock_index]
        upper = self.matrix[clock_index][0]

        lower_val = -lower.val
        lower_incl = lower.rel == "<="
        upper_val = upper.val
        upper_incl = upper.rel == "<="

        interval = Interval(lower_val=lower_val, lower_incl=lower_incl, upper_val=upper_val, upper_incl=upper_incl)

        return interval

    def make_graph(self):
        """Generates a graph representation of the DBM.

        Returns:
            The graph representation of the DBM.
        """
        graph = WeightedGraph()
        for clock in self.clocks:
            graph.new_node(clock)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if i != j:
                    graph.new_edge_by_node_names(source_name=self.clocks[j], target_name=self.clocks[i],
                                                 weight=self.matrix[i][j].val)

        return graph

    def transpose(self):
        """Transposes the DBM (i.e., swaps rows and columns (DBM^T))

        Returns:
            The transposed DBM.
        """
        for i in range(len(self.matrix)):
            for j in range(i + 1, len(self.matrix[0])):
                entry_temp = self.matrix[i][j]
                self.matrix[i][j] = self.matrix[j][i]
                self.matrix[j][i] = entry_temp
        return self

    def negate(self):
        """Inverts the DBM (i.e., multiplies all values with -1)

        Returns:
            The inverted DBM.
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                self.matrix[i][j].val *= -1
        return self

    def close(self):
        """Transforms the DBM into closed form.

        Returns:
            The DBM in closed form.
        """
        self.matrix = floyd_warshall(self.matrix)
        return self

    def canonicalize(self):
        """Synonym for "close" function.

        Returns:
            The DBM in closed form.
        """
        self.close()
        return self

    def is_empty(self):
        """Checks if the DBM is empty (i.e., for all intervals, the lower bound is smaller-equal the upper bound).

        Returns:
            The emptiness checking result.
        """
        for i in range(len(self.matrix)):
            # If upper < lower bound
            lo = self.matrix[0][i]
            up = self.matrix[i][0]
            if lo.val < -up.val or (up.val == -lo.val and (lo.rel == '<' or up.rel == '<')):
                return True
        return False

    def includes(self, other):
        """Checks if the DBM includes another DBM (i.e., it is a super region of the other DBM)

        Args:
            other: The other DBM.

        Returns:
            The inclusion checking result.
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if not other.matrix[i][j] <= self.matrix[i][j]:
                    return False
        return True

    def intersect(self, other):
        """Intersects the DBM with another DBM.

        Args:
            other: The other DBM.

        Returns:
            The intersected DBM.
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                self.matrix[i][j] = min(other.matrix[i][j], self.matrix[i][j])
        self.canonicalize()
        return self

    def satisfies(self, state):
        """Checks if the DBM satisfies a given value assignment (i.e., the value vector lies within the DBM)

        Args:
            state:

        Returns:
            The satisfaction checking result.
        """
        for var, val in state.items():
            clock_interval = self.get_interval(var)
            if (val < clock_interval.lower_val or
                    ((val == clock_interval.lower_val) and not clock_interval.lower_incl)):
                return False
            if (val > clock_interval.upper_val or
                    ((val == clock_interval.upper_val) and not clock_interval.upper_incl)):
                return False
        return True

    def delay_future(self):
        """Delays the DBM into the future by setting all upper clock bounds (DBM[i,0]) to infinity.

        Returns:
            The delayed DBM.
        """
        for i in range(1, len(self.matrix)):
            self.matrix[i][0] = DBMEntry(np.inf, '<')
        return self

    def delay_past(self):
        """Delays the DBM into the past by setting all lower clock bounds (DBM[0,i]) to 0.

        Returns:
            The delayed DBM.
        """
        for i in range(1, len(self.matrix[0])):
            self.matrix[0][i] = DBMEntry(0, '<=')
        return self

    def conjugate(self, constraint):
        """Conjugates the DBM with a constraint, restricting its region.

        Args:
            constraint: The constraint that should be applied to the DBM.

        Returns:
            The constrained DBM.
        """
        clock_1_index = self.clocks.index(constraint.clock1)
        clock_2_index = self.clocks.index(constraint.clock2)
        new_entry = DBMEntry(constraint.val, constraint.rel)
        curr_entry = self.matrix[clock_1_index][clock_2_index]
        if new_entry < curr_entry:
            self.matrix[clock_1_index][clock_2_index] = new_entry
        return self

    def reset(self, clock, val):
        """Resets a given clock of the DBM, adapting the differences to the remaining clocks.

        Args:
            clock: The clock that should be reset.
            val: The reset value.

        Returns:
            The DBM after reset.
        """
        clock_index = self.clocks.index(clock)
        for i in range(0, len(self.matrix)):
            self.matrix[i][clock_index] = DBMEntry(-val, '<=') + self.matrix[i][0]
        for j in range(0, len(self.matrix[0])):
            self.matrix[clock_index][j] = DBMEntry(val, '<=') + self.matrix[0][j]
        return self

    def copy_matrix(self):
        """Copies the value matrix of the DBM.

        Returns:
            The copied value matrix.
        """
        matrix = []
        for i in range(0, len(self.matrix)):
            row = []
            for j in range(0, len(self.matrix[0])):
                row.append(self.matrix[i][j].copy())
            matrix.append(row)
        return matrix

    def copy(self):
        """Copies the DBM instance.

        Returns:
            The copied DBM instance.
        """
        copy_obj = DBM(clocks=self.clocks, add_ref_clock=False)
        copy_obj.matrix = self.copy_matrix()
        return copy_obj

    def __repr__(self):
        # https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list?answertab=oldest#tab-top
        s = [[""] + self.clocks]
        s += [([self.clocks[i]] + [str(e) for e in row]) for i, row in enumerate(self.matrix)]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)

    def __eq__(self, other):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
