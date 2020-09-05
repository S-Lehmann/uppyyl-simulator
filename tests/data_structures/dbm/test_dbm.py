import pprint

import numpy as np
import pytest

from uppyyl_simulator.backend.data_structures.dbm.dbm import DBMEntry, DBMConstraint, Interval, DBM, \
    switch_relation

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False

###########
# General #
###########
test_switch_relation_data = [
    (">", "<"),
    (">=", "<="),
    ("<", ">"),
    ("<=", ">="),
]


@pytest.mark.parametrize(
    "rel,expected", test_switch_relation_data,
    ids=list(map(lambda data: f'switch({data[0]}) = {data[1]}', test_switch_relation_data)))
def test_switch_relation(rel, expected):
    assert switch_relation(rel) == expected


def test_switch_relation_fail():
    with pytest.raises(Exception):
        switch_relation("-")


#############
# DBM Entry #
#############
test_dbm_entry_add_data = [
    (DBMEntry(5, "<="), DBMEntry(3, "<="), DBMEntry(val=8, rel="<=")),
    (DBMEntry(5, "<="), DBMEntry(3, "<"), DBMEntry(val=8, rel="<")),
    (DBMEntry(5, "<"), DBMEntry(3, "<="), DBMEntry(val=8, rel="<")),
    (DBMEntry(5, "<"), DBMEntry(3, "<"), DBMEntry(val=8, rel="<")),
    (DBMEntry(-5, "<="), DBMEntry(3, "<="), DBMEntry(val=-2, rel="<=")),
]


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_entry_add_data,
    ids=list(map(lambda data: f'{data[0]} + {data[1]} = {data[2]}', test_dbm_entry_add_data)))
def test_dbm_entry_add(left, right, expected):
    assert (left + right) == expected


test_dbm_entry_lt_data = [
    (DBMEntry(5, "<="), DBMEntry(5, "<="), False),
    (DBMEntry(5, "<="), DBMEntry(5, "<"), False),
    (DBMEntry(5, "<"), DBMEntry(5, "<="), True),
    (DBMEntry(5, "<"), DBMEntry(5, "<"), False),
    (DBMEntry(5, "<="), DBMEntry(3, "<="), False),
    (DBMEntry(5, "<="), DBMEntry(3, "<"), False),
    (DBMEntry(5, "<"), DBMEntry(3, "<="), False),
    (DBMEntry(5, "<"), DBMEntry(3, "<"), False),
    (DBMEntry(3, "<="), DBMEntry(5, "<="), True),
    (DBMEntry(3, "<="), DBMEntry(5, "<"), True),
    (DBMEntry(3, "<"), DBMEntry(5, "<="), True),
    (DBMEntry(3, "<"), DBMEntry(5, "<"), True),
]


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_entry_lt_data,
    ids=list(map(lambda data: f'{data[0]} < {data[1]} = {data[2]}', test_dbm_entry_lt_data)))
def test_dbm_entry_lt(left, right, expected):
    assert (left < right) == expected


test_dbm_entry_le_data = [
    (DBMEntry(5, "<="), DBMEntry(5, "<="), True),
    (DBMEntry(5, "<="), DBMEntry(5, "<"), False),
    (DBMEntry(5, "<"), DBMEntry(5, "<="), True),
    (DBMEntry(5, "<"), DBMEntry(5, "<"), True),
    (DBMEntry(5, "<="), DBMEntry(3, "<="), False),
    (DBMEntry(5, "<="), DBMEntry(3, "<"), False),
    (DBMEntry(5, "<"), DBMEntry(3, "<="), False),
    (DBMEntry(5, "<"), DBMEntry(3, "<"), False),
    (DBMEntry(3, "<="), DBMEntry(5, "<="), True),
    (DBMEntry(3, "<="), DBMEntry(5, "<"), True),
    (DBMEntry(3, "<"), DBMEntry(5, "<="), True),
    (DBMEntry(3, "<"), DBMEntry(5, "<"), True),
]


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_entry_le_data,
    ids=list(map(lambda data: f'{data[0]} <= {data[1]} = {data[2]}', test_dbm_entry_le_data)))
def test_dbm_entry_le(left, right, expected):
    assert (left <= right) == expected


test_dbm_entry_gt_data = list(map(lambda data: (data[0], data[1], not data[2]), test_dbm_entry_le_data))


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_entry_gt_data,
    ids=list(map(lambda data: f'{data[0]} > {data[1]} = {data[2]}', test_dbm_entry_gt_data)))
def test_dbm_entry_gt(left, right, expected):
    assert (left > right) == expected


test_dbm_entry_ge_data = list(map(lambda data: (data[0], data[1], not data[2]), test_dbm_entry_lt_data))


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_entry_ge_data,
    ids=list(map(lambda data: f'{data[0]} >= {data[1]} = {data[2]}', test_dbm_entry_ge_data)))
def test_dbm_entry_ge(left, right, expected):
    assert (left >= right) == expected


test_dbm_entry_eq_data = [
    (DBMEntry(5, "<="), DBMEntry(5, "<="), True),
    (DBMEntry(5, "<="), DBMEntry(5, "<"), False),
    (DBMEntry(5, "<"), DBMEntry(5, "<="), False),
    (DBMEntry(5, "<"), DBMEntry(5, "<"), True),
    (DBMEntry(5, "<="), DBMEntry(3, "<="), False),
    (DBMEntry(5, "<="), DBMEntry(3, "<"), False),
    (DBMEntry(5, "<"), DBMEntry(3, "<="), False),
    (DBMEntry(5, "<"), DBMEntry(3, "<"), False),
    (DBMEntry(3, "<="), DBMEntry(5, "<="), False),
    (DBMEntry(3, "<="), DBMEntry(5, "<"), False),
    (DBMEntry(3, "<"), DBMEntry(5, "<="), False),
    (DBMEntry(3, "<"), DBMEntry(5, "<"), False),
]


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_entry_eq_data,
    ids=list(map(lambda data: f'{data[0]} == {data[1]} = {data[2]}', test_dbm_entry_eq_data)))
def test_dbm_entry_eq(left, right, expected):
    assert (left == right) == expected


test_dbm_entry_neq_data = list(map(lambda data: (data[0], data[1], not data[2]), test_dbm_entry_eq_data))


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_entry_neq_data,
    ids=list(map(lambda data: f'{data[0]} == {data[1]} = {data[2]}', test_dbm_entry_neq_data)))
def test_dbm_entry_neq(left, right, expected):
    assert (left != right) == expected


def test_dbm_entry_copy():
    entry = DBMEntry(val=10, rel="<")
    entry_copy = entry.copy()
    assert entry is not entry_copy
    assert (entry.val, entry.rel) == (entry_copy.val, entry_copy.rel)


##################
# DBM Constraint #
##################
def test_dbm_constraint_init():
    constr = DBMConstraint(constr_text="t1 - t2 >= 5")
    assert (constr.clock1, constr.clock2, constr.rel, constr.val) == ("t2", "t1", "<=", -5)


def test_dbm_constraint_not_parsed():
    with pytest.raises(Exception):
        DBMConstraint(constr_text="t1 * t2 >= 5")


def test_dbm_constraint_copy():
    constr = DBMConstraint(constr_text="t1 - t2 <= 5")
    constr_copy = constr.copy()
    assert constr is not constr_copy
    assert ((constr.clock1, constr.clock2, constr.rel, constr.val)
            == (constr_copy.clock1, constr_copy.clock2, constr_copy.rel, constr_copy.val))


def test_dbm_constraint_str():
    constr = DBMConstraint(constr_text="t1 - t2 >= 5")
    assert isinstance(str(constr), str)


################
# DBM Interval #
################
def test_dbm_interval_init():
    interv = Interval("[", 0, 2, "]")
    assert (interv.lower_incl, interv.lower_val, interv.upper_val, interv.upper_incl) == (True, 0, 2, True)


# def test_dbm_interval_init_fail():
#     with pytest.raises(Exception):
#         Interval("[", 2, 0, "]")


test_dbm_interval_intersect_data = [
    (Interval("[", 0, 0, "]"), Interval("[", 0, 0, "]"), Interval("[", 0, 0, "]")),
    (Interval("[", 0, 4, "]"), Interval("[", 3, 6, "]"), Interval("[", 3, 4, "]")),
    (Interval("[", 3, 8, "]"), Interval("[", 1, 5, "]"), Interval("[", 3, 5, "]")),
]


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_interval_intersect_data,
    ids=list(map(lambda data: f'intersect({data[0]},{data[1]}) = {data[2]}', test_dbm_interval_intersect_data)))
def test_dbm_interval_intersect(left, right, expected):
    assert left.intersect(right) == expected


test_dbm_interval_intersect_fail_data = [
    (Interval("[", 0, 2, "]"), Interval("[", 3, 5, "]")),
]


@pytest.mark.parametrize(
    "left,right", test_dbm_interval_intersect_fail_data,
    ids=list(map(lambda data: f'intersect({data[0]},{data[1]})', test_dbm_interval_intersect_fail_data)))
def test_dbm_interval_intersect_fail(left, right):
    with pytest.raises(Exception):
        left.intersect(right)


test_dbm_interval_is_empty_data = [
    (Interval("[", 0, 2, "]"), False),
    (Interval("[", 2, 2, "]"), False),
]


@pytest.mark.parametrize(
    "interv,expected", test_dbm_interval_is_empty_data,
    ids=list(map(lambda data: f'is_empty({data[0]}) = {data[1]}', test_dbm_interval_is_empty_data)))
def test_dbm_interval_is_empty(interv, expected):
    assert interv.is_empty() == expected


test_dbm_interval_get_random_data = [
    (Interval("[", 0, 2, "]")),
    (Interval("[", 2, 2, "]")),
]


@pytest.mark.parametrize(
    "interv", test_dbm_interval_get_random_data,
    ids=list(map(lambda data: f'get_random({data})', test_dbm_interval_get_random_data)))
def test_dbm_interval_get_random(interv):
    rand_val = interv.get_random()
    assert interv.lower_val <= rand_val <= interv.upper_val


test_dbm_interval_get_random_fail_data = [
    (Interval("(", 2, 3, ")")),
]


@pytest.mark.parametrize(
    "interv", test_dbm_interval_get_random_fail_data,
    ids=list(map(lambda data: f'get_random({data})', test_dbm_interval_get_random_fail_data)))
def test_dbm_interval_get_random_fail(interv):
    with pytest.raises(Exception):
        interv.get_random()


test_dbm_interval_eq_data = [
    (Interval("[", 0, 2, "]"), Interval("[", 0, 2, "]"), True),
    (Interval("[", 0, 2, "]"), Interval("[", 0, 3, "]"), False),
    (Interval("[", 0, 2, "]"), Interval("(", 0, 2, "]"), False),
]


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_interval_eq_data,
    ids=list(map(lambda data: f'{data[0]} == {data[1]} = {data[2]}', test_dbm_interval_eq_data)))
def test_dbm_interval_eq(left, right, expected):
    assert (left == right) == expected


test_dbm_interval_neq_data = list(map(lambda data: (data[0], data[1], not data[2]), test_dbm_interval_eq_data))


@pytest.mark.parametrize(
    "left,right,expected", test_dbm_interval_neq_data,
    ids=list(map(lambda data: f'{data[0]} == {data[1]} = {data[2]}', test_dbm_interval_neq_data)))
def test_dbm_interval_eq(left, right, expected):
    assert (left != right) == expected


#######
# DBM #
#######
@pytest.fixture
def dbm():
    dbm = DBM(clocks=["t1", "t2"], add_ref_clock=True, zero_init=True)
    dbm.matrix[0][1].val = -1
    dbm.matrix[0][2].val = -2
    dbm.matrix[1][0].val = 3
    dbm.matrix[2][0].val = 4
    return dbm


@pytest.fixture
def dbm2():
    dbm = DBM(clocks=["t1", "t2"], add_ref_clock=True, zero_init=True)
    dbm.matrix[0][1].val = -3
    dbm.matrix[0][2].val = -4
    dbm.matrix[1][0].val = 1
    dbm.matrix[2][0].val = 2
    return dbm


def test_dbm_zero_init():
    dbm = DBM(clocks=["t1", "t2"], add_ref_clock=True, zero_init=True)
    assert dbm.clocks == ["T0_REF", "t1", "t2"]
    assert dbm.matrix == [
        [DBMEntry(0, '<='), DBMEntry(0, '<='), DBMEntry(0, '<=')],
        [DBMEntry(0, '<='), DBMEntry(0, '<='), DBMEntry(0, '<=')],
        [DBMEntry(0, '<='), DBMEntry(0, '<='), DBMEntry(0, '<=')],
    ]


def test_dbm_inf_init():
    dbm = DBM(clocks=["t1", "t2"], add_ref_clock=True, zero_init=False)
    assert dbm.clocks == ["T0_REF", "t1", "t2"]
    assert dbm.matrix == [
        [DBMEntry(0, '<='), DBMEntry(np.inf, '<'), DBMEntry(np.inf, '<')],
        [DBMEntry(np.inf, '<'), DBMEntry(0, '<='), DBMEntry(np.inf, '<')],
        [DBMEntry(np.inf, '<'), DBMEntry(np.inf, '<'), DBMEntry(0, '<=')],
    ]


def test_dbm_get_interval(dbm):
    interv = dbm.get_interval("t1")
    assert (interv.lower_incl, interv.lower_val, interv.upper_val, interv.upper_incl) == (True, 1, 3, True)


def test_dbm_make_graph(dbm):
    graph = dbm.make_graph()
    assert len(graph.nodes) == 3
    assert len(graph.edges) == 6
    for source_node_id, source_node in graph.nodes.items():
        source_node_name = source_node.name
        for edge_id, edge in source_node.out_edges.items():
            target_node_name = edge.target.name
            source_index = dbm.clocks.index(source_node_name)
            target_index = dbm.clocks.index(target_node_name)
            assert dbm.matrix[target_index][source_index].val == edge.weight


def test_dbm_transpose(dbm):
    transposed_dbm = dbm.copy().transpose()
    for i in range(len(dbm.matrix)):
        for j in range(len(dbm.matrix[0])):
            assert transposed_dbm.matrix[i][j] == dbm.matrix[j][i]


def test_dbm_negate(dbm):
    negated_dbm = dbm.copy().negate()
    for i in range(len(dbm.matrix)):
        for j in range(len(dbm.matrix[0])):
            assert negated_dbm.matrix[i][j].val == -dbm.matrix[i][j].val


def test_dbm_close(dbm):
    dbm.close()
    assert dbm.matrix == [
        [DBMEntry(0, '<='), DBMEntry(-2, '<='), DBMEntry(-2, '<=')],
        [DBMEntry(3, '<='), DBMEntry(0, '<='), DBMEntry(0, '<=')],
        [DBMEntry(3, '<='), DBMEntry(0, '<='), DBMEntry(0, '<=')],
    ]


def test_dbm_canonicalize(dbm):
    dbm.canonicalize()
    assert dbm.matrix == [
        [DBMEntry(0, '<='), DBMEntry(-2, '<='), DBMEntry(-2, '<=')],
        [DBMEntry(3, '<='), DBMEntry(0, '<='), DBMEntry(0, '<=')],
        [DBMEntry(3, '<='), DBMEntry(0, '<='), DBMEntry(0, '<=')],
    ]


def test_dbm_is_empty_false(dbm):
    assert not dbm.is_empty()


def test_dbm_is_empty_true(dbm2):
    assert dbm2.is_empty()


def test_dbm_includes_true(dbm):
    assert dbm.includes(dbm)


def test_dbm_includes_false(dbm, dbm2):
    assert not dbm2.includes(dbm)


def test_dbm_intersect(dbm):
    assert dbm.intersect(dbm) == dbm


def test_dbm_satisfies_true(dbm):
    state = {"t1": 2, "t2": 2}
    assert dbm.satisfies(state)


def test_dbm_satisfies_false_1(dbm):
    state = {"t1": 5, "t2": 5}
    assert not dbm.satisfies(state)


def test_dbm_satisfies_false_2(dbm):
    state = {"t1": 0, "t2": 0}
    assert not dbm.satisfies(state)


def test_dbm_delay_future(dbm):
    dbm.delay_future()
    for i in range(1, len(dbm.matrix)):
        assert dbm.matrix[i][0] == DBMEntry(np.inf, '<')


def test_dbm_delay_past(dbm):
    dbm.delay_past()
    for j in range(1, len(dbm.matrix[0])):
        assert dbm.matrix[0][j] == DBMEntry(0, '<=')


def test_dbm_conjugate(dbm):
    constr = DBMConstraint("t1 <= 2")
    dbm.conjugate(constr)
    assert dbm.matrix[1][0].val == 2


def test_dbm_reset(dbm):
    dbm.reset(clock="t1", val=10)
    assert dbm.matrix[1][0].val == 10
    assert dbm.matrix[0][1].val == -10


def test_dbm_copy(dbm):
    dbm_copy = dbm.copy()
    assert dbm == dbm_copy


def test_dbm_str(dbm):
    assert isinstance(str(dbm), str)


def test_dbm_eq(dbm, dbm2):
    assert dbm != dbm2
