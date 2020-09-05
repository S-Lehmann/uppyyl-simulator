import pprint
import unittest

from uppyyl_simulator.backend.models.ta.ta import (
    Template, Location, Edge
)

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


#####################
# Template Creation #
#####################
class TestTemplateCreation(unittest.TestCase):
    def setUp(self):
        print("")

    def test_create_automaton(self):
        msg = f'Creating model ...'
        print(msg)
        tmpl = Template("A_Tmpl")

        self.assertEqual(tmpl.name, "A_Tmpl")


######################
# Template Functions #
######################
class TestTemplateFunctions(unittest.TestCase):
    def setUp(self):
        self.tmpl = Template("A_Tmpl")
        print("")

    def test_new_location(self):
        msg = f'Creating new location in template ...'
        print(msg)
        self.tmpl.new_location("Loc_A")

        loc_names = list(map(lambda l: l.name, self.tmpl.locations.values()))
        expected_loc_names = ["Loc_A"]
        self.assertEqual(loc_names, expected_loc_names)

    def test_add_location(self):
        msg = f'Adding existing location in template ...'
        print(msg)
        loc = Location("Loc_A")
        self.tmpl.add_location(loc)

        loc_names = list(map(lambda l: l.name, self.tmpl.locations.values()))
        expected_loc_names = ["Loc_A"]
        self.assertEqual(loc_names, expected_loc_names)

    def test_new_edge(self):
        msg = f'Creating new edge in template ...'
        print(msg)
        self.tmpl.new_location("Loc_A")
        self.tmpl.new_location("Loc_B")
        self.tmpl.new_edge_by_loc_names("Loc_A", "Loc_B")

        edge_names = list(map(lambda e: e.get_name(), self.tmpl.edges.values()))
        expected_edge_names = ["Loc_A->Loc_B"]
        self.assertEqual(edge_names, expected_edge_names)

    def test_add_edge(self):
        msg = f'Adding existing edge in template ...'
        print(msg)
        self.tmpl.new_location("Loc_A")
        self.tmpl.new_location("Loc_B")
        self.tmpl.new_edge_by_loc_names("Loc_A", "Loc_B")

        edge_names = list(map(lambda e: e.get_name(), self.tmpl.edges.values()))
        expected_edge_names = ["Loc_A->Loc_B"]
        self.assertEqual(edge_names, expected_edge_names)

    def test_new_parameter(self):
        msg = f'Creating new parameter in template ...'
        print(msg)
        self.tmpl.new_parameter("int x")
        self.assertEqual(self.tmpl.parameters[0].text, "int x")

    # def test_set_parameters(self):
    #     msg = f'Setting template parameters ...'
    #     print(msg)
    #     self.tmpl.set_parameters({"x": 10})
    #
    #     self.assertEqual(parameters, expected_parameters)

    # def test_create_instance(self):
    #     msg = f'Creating concrete instance of template ...'
    #     print(msg)
    #     self.tmpl.parameters = [
    #         {'isRef': '&',
    #          'type': {'astType': 'Type',
    #                   'prefixes': [],
    #                   'typeId': {'astType': 'CustomType', 'type': 'int'}},
    #          'varData': {'arrayDecl': [],
    #                      'astType': 'VariableID',
    #                      'varName': 'x'}},
    #         {'isRef': None,
    #          'type': {'astType': 'Type',
    #                   'prefixes': ['const'],
    #                   'typeId': {'astType': 'CustomType', 'type': 'int'}},
    #          'varData': {'arrayDecl': [],
    #                      'astType': 'VariableID',
    #                      'varName': 'i'}}
    #     ]
    #     args = [
    #         {'astType': 'Integer', 'val': 1},
    #         {'astType': 'BinaryExpr',
    #          'left': {'astType': 'Integer', 'val': 2},
    #          'op': 'Add',
    #          'right': {'astType': 'Integer', 'val': 3}}
    #     ]
    #     inst = self.tmpl.create_instance("Inst_A", args)
    #
    #     self.assertEqual(inst.name, "Inst_A")
    #     self.assertEqual(self.tmpl.locations, inst.locations)
    #     self.assertEqual(self.tmpl.edges, inst.edges)

    def test_copy(self):
        msg = f'Test copy'
        print(msg)

        src_tmpl = Template("Src_Tmpl")
        src_tmpl.new_location("Loc_A")
        src_tmpl.new_location("Loc_B")
        edge = src_tmpl.new_edge_by_loc_names("Loc_A", "Loc_B")
        edge.add_nail(pos={"x": 100, "y": 100})
        src_tmpl.clock_names = ["t1", "t2"]
        src_tmpl.parameters = []

        tmpl = src_tmpl.copy()

        self.assertEqual(tmpl.name, src_tmpl.name)
        self.assertEqual(len(tmpl.locations), len(src_tmpl.locations))

        for tmpl_loc, src_tmpl_loc in zip(tmpl.locations.values(), src_tmpl.locations.values()):
            self.assertEqual(tmpl_loc.id, src_tmpl_loc.id)
            self.assertEqual(tmpl_loc.name, src_tmpl_loc.name)
            for tmpl_loc_inv, src_tmpl_loc_inv in zip(tmpl_loc.invariants, src_tmpl_loc.invariants):
                self.assertEqual(tmpl_loc_inv.text, src_tmpl_loc_inv.text)
                self.assertEqual(tmpl_loc_inv.ast, src_tmpl_loc_inv.ast)

        for tmpl_edge, src_tmpl_edge in zip(tmpl.edges.values(), src_tmpl.edges.values()):
            self.assertEqual(tmpl_edge.id, src_tmpl_edge.id)
            for tmpl_edge_grd, src_tmpl_edge_grd in zip(tmpl_edge.clock_guards, src_tmpl_edge.clock_guards):
                self.assertEqual(tmpl_edge_grd.text, src_tmpl_edge_grd.text)
                self.assertEqual(tmpl_edge_grd.ast, src_tmpl_edge_grd.ast)
            for tmpl_edge_grd, src_tmpl_edge_grd in zip(tmpl_edge.variable_guards, src_tmpl_edge.variable_guards):
                self.assertEqual(tmpl_edge_grd.text, src_tmpl_edge_grd.text)
                self.assertEqual(tmpl_edge_grd.ast, src_tmpl_edge_grd.ast)
            for tmpl_edge_updt, src_tmpl_edge_updt in zip(tmpl_edge.updates, src_tmpl_edge.updates):
                self.assertEqual(tmpl_edge_updt.text, src_tmpl_edge_updt.text)
                self.assertEqual(tmpl_edge_updt.ast, src_tmpl_edge_updt.ast)
            for tmpl_edge_rst, src_tmpl_edge_rst in zip(tmpl_edge.resets, src_tmpl_edge.resets):
                self.assertEqual(tmpl_edge_rst.text, src_tmpl_edge_rst.text)
                self.assertEqual(tmpl_edge_rst.ast, src_tmpl_edge_rst.ast)
            for tmpl_edge_sel, src_tmpl_edge_sel in zip(tmpl_edge.selects, src_tmpl_edge.selects):
                self.assertEqual(tmpl_edge_sel.text, src_tmpl_edge_sel.text)
                self.assertEqual(tmpl_edge_sel.ast, src_tmpl_edge_sel.ast)
            if tmpl_edge.sync and src_tmpl_edge.sync:
                self.assertEqual(tmpl_edge.sync.text, src_tmpl_edge.sync.text)
                self.assertEqual(tmpl_edge.sync.ast, src_tmpl_edge.sync.ast)

    def test_str(self):
        res = str(self.tmpl)
        self.assertTrue(isinstance(res, str))


######################
# Location Functions #
######################
class TestLocationFunctions(unittest.TestCase):
    def setUp(self):
        self.loc = Location("A")
        print("")

    def test_set_whole_position(self):
        self.loc.view = {
            "self": {"pos": {"x": 0, "y": 0}},
            "name_label": {"pos": {"x": 20, "y": -20}, "id": None},
            "invariant_label": {"pos": {"x": 20, "y": 20}, "id": None}
        }
        self.loc.set_whole_position(pos={"x": 100, "y": 100})
        self.assertEqual(self.loc.view["self"]["pos"], {"x": 100, "y": 100})
        self.assertEqual(self.loc.view["name_label"]["pos"], {"x": 120, "y": 80})
        self.assertEqual(self.loc.view["invariant_label"]["pos"], {"x": 120, "y": 120})

    def test_set_urgent(self):
        self.loc.committed = True
        self.loc.set_urgent()
        self.assertTrue(self.loc.urgent)
        self.assertFalse(self.loc.committed)

    def test_set_committed(self):
        self.loc.urgent = True
        self.loc.set_committed()
        self.assertFalse(self.loc.urgent)
        self.assertTrue(self.loc.committed)

    def test_new_invariant(self):
        self.loc.new_invariant("t <= 10")
        self.assertEqual(self.loc.invariants[0].text, "t <= 10")

    def test_str(self):
        res = str(self.loc)
        self.assertTrue(isinstance(res, str))


##################
# Edge Functions #
##################
class TestEdgeFunctions(unittest.TestCase):
    def setUp(self):
        self.loc_A = Location("A")
        self.loc_B = Location("B")
        self.edge = Edge(source=self.loc_A, target=self.loc_B)
        print("")

    def test_add_nail(self):
        self.edge.add_nail(pos={"x": 100, "y": 100})
        self.assertEqual(list(self.edge.view["nails"].values())[0]["pos"], {"x": 100, "y": 100})

    def test_new_clock_guard(self):
        self.edge.new_clock_guard("t >= 10")
        self.assertEqual(self.edge.clock_guards[0].text, "t >= 10")

    def test_new_variable_guard(self):
        self.edge.new_variable_guard("cond")
        self.assertEqual(self.edge.variable_guards[0].text, "cond")

    def test_new_reset(self):
        self.edge.new_reset("t = 0")
        self.assertEqual(self.edge.resets[0].text, "t = 0")

    def test_new_update(self):
        self.edge.new_update("x = 0")
        self.assertEqual(self.edge.updates[0].text, "x = 0")

    def test_new_select(self):
        self.edge.new_select("x : int[0, 10]")
        self.assertEqual(self.edge.selects[0].text, "x : int[0, 10]")

    def test_set_sync(self):
        self.edge.set_sync("ch!")
        self.assertEqual(self.edge.sync.text, "ch!")

    def test_str(self):
        res = str(self.edge)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
