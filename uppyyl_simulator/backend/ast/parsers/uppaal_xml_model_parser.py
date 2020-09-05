"""The parsers for transformation of Uppaal XML models to system objects, and vice versa."""

from collections import OrderedDict
from copy import deepcopy

from lxml import etree

import uppyyl_simulator.backend.models.ta.nta as nta
from uppyyl_simulator.backend.data_structures.ast.ast_code_element import (
    apply_func_to_ast
)
from uppyyl_simulator.backend.helper.helper import (
    unique_id
)
from uppyyl_simulator.backend.models.base.query import (
    Query
)
from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import (
    UppaalCLanguageParser
)
from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import (
    UppaalCLanguageSemantics
)


######################
# Uppaal XML to dict #
######################
def uppaal_xml_to_dict(system_xml_str):
    """Transforms the XML description of a Uppaal system into a data dictionary.

    Args:
        system_xml_str: The Uppaal system XML string.

    Returns:
        The data dictionary of Uppaal system data.
    """
    system = OrderedDict()

    system_xml_str = system_xml_str.encode('utf-8')
    nta_element = etree.fromstring(system_xml_str)

    # Parse global declaration
    global_declaration_element = nta_element.find("declaration")
    if global_declaration_element is not None:
        system["global_declaration"] = global_declaration_element.text
    else:
        system["global_declaration"] = ""

    # Parse system declaration
    system_declaration_element = nta_element.find("system")
    if global_declaration_element is not None:
        system["system_declaration"] = system_declaration_element.text
    else:
        system["system_declaration"] = ""

    ###################
    # Parse templates #
    ###################
    system["templates"] = []
    template_elements = nta_element.findall("template")
    for template_element in template_elements:
        template = OrderedDict()

        template["id"] = unique_id("tmpl")

        # Parse template name
        template_name_element = template_element.find("name")
        if template_name_element is not None:
            template["name"] = template_name_element.text
        else:
            template["name"] = ""

        # Parse template parameters
        template_parameters_element = template_element.find("parameter")
        if template_parameters_element is not None:
            template["parameters"] = template_parameters_element.text
        else:
            template["parameters"] = ""

        # Parse local template declaration
        template_declaration_element = template_element.find("declaration")
        if template_declaration_element is not None:
            template["declaration"] = template_declaration_element.text
        else:
            template["declaration"] = ""

        ###################
        # Parse locations #
        ###################
        template["locations"] = []
        location_elements = template_element.findall("location")
        for location_element in location_elements:
            location = OrderedDict()
            location["id"] = location_element.attrib["id"]
            location["pos"] = {
                "x": int(location_element.attrib["x"]),
                "y": int(location_element.attrib["y"])
            }

            # Parse location name
            location["name"] = None
            location["name_label"] = None
            location_name_element = location_element.find("name")
            if location_name_element is not None:
                label = OrderedDict()
                label["id"] = unique_id("label")
                label["pos"] = {
                    "x": int(location_name_element.attrib["x"]),
                    "y": int(location_name_element.attrib["y"])
                }
                location["name"] = location_name_element.text
                location["name_label"] = label

            # Parse urgent / committed
            urgent_element = location_element.find("urgent")
            location["urgent"] = (urgent_element is not None)

            committed_element = location_element.find("committed")
            location["committed"] = (committed_element is not None)

            # Parse location labels
            location["invariant"] = None
            location["invariant_label"] = None
            label_elements = location_element.findall("label")
            for label_element in label_elements:
                label = OrderedDict()
                label["id"] = unique_id("label")
                label["pos"] = {
                    "x": int(label_element.attrib["x"]),
                    "y": int(label_element.attrib["y"])
                }

                if label_element.attrib["kind"] == "invariant":
                    location["invariant"] = label_element.text
                    location["invariant_label"] = label

            template["locations"].append(location)

        # Parse initial location
        init_location_element = template_element.find("init")
        if init_location_element is not None:
            template["init_loc_id"] = init_location_element.attrib["ref"]

        ###############
        # Parse edges #
        ###############
        template["edges"] = []  # OrderedDict()
        edge_elements = template_element.findall("transition")
        for edge_element in edge_elements:
            edge = OrderedDict()
            edge["id"] = unique_id("edge")

            # Parse edge source location
            edge_source_element = edge_element.find("source")
            if edge_source_element is not None:
                edge["source_loc_id"] = edge_source_element.attrib["ref"]

            # Parse edge target location
            edge_target_element = edge_element.find("target")
            if edge_target_element is not None:
                edge["target_loc_id"] = edge_target_element.attrib["ref"]

            # Parse edge labels
            edge["guard"] = None
            edge["guard_label"] = None
            edge["update"] = None
            edge["update_label"] = None
            edge["synchronisation"] = None
            edge["sync_label"] = None
            edge["select"] = None
            edge["select_label"] = None
            label_elements = edge_element.findall("label")
            for label_element in label_elements:
                label = OrderedDict()
                label["id"] = unique_id("label")
                label["pos"] = {
                    "x": int(label_element.attrib["x"]),
                    "y": int(label_element.attrib["y"])
                }

                if label_element.attrib["kind"] == "guard":
                    edge["guard"] = label_element.text
                    edge["guard_label"] = label
                elif label_element.attrib["kind"] == "assignment":
                    edge["update"] = label_element.text
                    edge["update_label"] = label
                elif label_element.attrib["kind"] == "synchronisation":
                    edge["synchronisation"] = label_element.text
                    edge["sync_label"] = label
                elif label_element.attrib["kind"] == "select":
                    edge["select"] = label_element.text
                    edge["select_label"] = label

            # Parse edge nails
            edge["nails"] = []
            nail_elements = edge_element.findall("nail")
            for nail_element in nail_elements:
                nail = OrderedDict()
                nail["id"] = unique_id("nail")
                nail["pos"] = {
                    "x": int(nail_element.attrib["x"]),
                    "y": int(nail_element.attrib["y"])
                }
                edge["nails"].append(nail)

            template["edges"].append(edge)

        system["templates"].append(template)

    #################
    # Parse queries #
    #################
    system["queries"] = []
    root_query_element = nta_element.find("queries")
    if root_query_element is not None:
        query_elements = root_query_element.findall("query")
        for query_element in query_elements:
            query = OrderedDict()
            query["id"] = None

            formula_element = query_element.find("formula")
            if formula_element is not None:
                query["formula"] = formula_element.text.strip()

            comment_element = query_element.find("comment")
            if comment_element is not None:
                query["comment"] = comment_element.text.strip()

            system["queries"].append(query)

    # print(json.dumps(system, indent=2))
    return system


#########################
# Uppaal dict to system #
#########################
def uppaal_dict_to_system(system_data):
    """Transforms the data dictionary of a Uppaal system into a system object.

    Args:
        system_data: The Uppaal system data dictionary.

    Returns:
        The Uppaal system object.
    """

    system = nta.System()
    uppaal_c_parser = UppaalCLanguageParser(semantics=UppaalCLanguageSemantics())

    system.set_declaration(system_data["global_declaration"])
    system.set_system_declaration(system_data["system_declaration"])

    ###################
    # Parse templates #
    ###################
    for template_data in system_data["templates"]:
        id_ = template_data["id"] if ("id" in template_data) else None
        name = template_data["name"] if ("name" in template_data) else ""

        template = system.new_template(name, id_)

        if template_data["parameters"] != "":
            parameter_asts = uppaal_c_parser.parse(template_data["parameters"], rule_name='Parameters')
            for parameter_ast in parameter_asts:
                template.new_parameter(parameter_ast)

        template.set_declaration(template_data["declaration"])

        # Clock check function
        template_scope_clocks = system.declaration.clocks + template.declaration.clocks

        def get_clocks(ast, acc):  # TODO: Handle clocks among template parameters
            """Adds the ast to acc if it is a clock variable.

            Args:
                ast: The AST dict.
                acc: A list of values accumulated during search.

            Returns:
                The original AST dict.
            """
            if ast["astType"] == "Variable":
                if ast["name"] in template_scope_clocks:
                    acc.append(ast["name"])
            return ast

        ###################
        # Parse locations #
        ###################
        for location_data in template_data["locations"]:
            id_ = location_data["id"] if ("id" in location_data) else ""
            name = location_data["name"] if ("name" in location_data) else ""

            location = template.new_location(name, id_)
            location.view["self"] = {"pos": location_data["pos"].copy()}

            if location_data["name_label"]:
                location.view["name_label"] = location_data["name_label"].copy()

            if location_data["invariant"]:
                invariants = uppaal_c_parser.parse(location_data["invariant"], rule_name='Invariants')
                for inv in invariants:
                    location.new_invariant(inv)
            if location_data["invariant_label"]:
                location.view["invariant_label"] = location_data["invariant_label"].copy()

            if location_data["urgent"]:
                location.set_urgent(True)

            if location_data["committed"]:
                location.set_committed(True)

        # Parse initial location
        template.set_init_location_by_id(template_data["init_loc_id"])

        ###############
        # Parse edges #
        ###############
        for edge_data in template_data["edges"]:
            id_ = edge_data["id"] if ("id" in edge_data) else ""
            source_loc_id = edge_data["source_loc_id"]
            target_loc_id = edge_data["target_loc_id"]

            edge = template.new_edge_by_loc_ids(source_loc_id, target_loc_id, id_)

            # Add guards
            if edge_data["guard"]:
                guards = uppaal_c_parser.parse(edge_data["guard"], rule_name='Guards')
                for guard in guards:
                    if len(apply_func_to_ast(guard, get_clocks)[1]) > 0:
                        edge.new_clock_guard(guard)
                    else:
                        edge.new_variable_guard(guard)
            if edge_data["guard_label"]:
                edge.view["guard_label"] = edge_data["guard_label"].copy()

            # Add updates
            if edge_data["update"]:
                updates = uppaal_c_parser.parse(edge_data["update"], rule_name='Updates')
                for update in updates:
                    if len(apply_func_to_ast(update, get_clocks)[1]) > 0:
                        edge.new_reset(update)
                    else:
                        edge.new_update(update)
            if edge_data["update_label"]:
                edge.view["update_label"] = edge_data["update_label"].copy()

            # Add synchronization
            if edge_data["synchronisation"]:
                edge.set_sync(edge_data["synchronisation"])
            if edge_data["sync_label"]:
                edge.view["sync_label"] = edge_data["sync_label"].copy()

            # Add selects
            if edge_data["select"]:
                edge.new_select(edge_data["select"])
            if edge_data["select_label"]:
                edge.view["select_label"] = edge_data["select_label"].copy()

            edge.view["nails"] = deepcopy(edge_data["nails"])

    #################
    # Parse queries #
    #################
    for query_data in system_data["queries"]:
        formula = query_data["formula"]
        comment = query_data["comment"]
        query = Query(formula, comment)
        system.add_query(query)

    # # print(json.dumps(system, indent=2))
    return system


########################
# Uppaal XML to system #
########################
def uppaal_xml_to_system(system_xml_str):
    """Transforms the XML description of a Uppaal system into a system object.

    Args:
        system_xml_str: The Uppaal system XML string.

    Returns:
        The Uppaal system object.
    """
    system_data = uppaal_xml_to_dict(system_xml_str)
    system = uppaal_dict_to_system(system_data)
    return system


#########################
# Uppaal system to dict #
#########################
def uppaal_system_to_dict(system):
    """Transforms the Uppaal system object into a data dictionary.

    Args:
        system: The Uppaal system object.

    Returns:
        The data dictionary of Uppaal system data.
    """
    system_data = OrderedDict()

    # Parse global declaration
    system_data["global_declaration"] = system.declaration.text
    system_data["system_declaration"] = system.system_declaration.text

    ###################
    # Parse templates #
    ###################
    system_data["templates"] = []
    for template_id, template in system.templates.items():
        template_data = OrderedDict()

        # template["id"] = template_id
        # Parse template name
        template_data["name"] = template.name
        # Parse template parameters
        template_data["parameters"] = ", ".join(list(map(lambda p: p.text, template.parameters)))
        # Parse local template declaration
        template_data["declaration"] = template.declaration.text

        ###################
        # Parse locations #
        ###################
        template_data["locations"] = []
        for location_id, location in template.locations.items():
            location_data = OrderedDict()
            location_data["id"] = location_id
            location_data["pos"] = location.view["self"]["pos"].copy()

            # Parse location name
            location_data["name"] = location.name
            location_data["name_label"] = deepcopy(location.view["name_label"])

            # Parse urgent / committed
            location_data["urgent"] = location.urgent
            location_data["committed"] = location.committed

            # Parse location labels
            location_data["invariant"] = " && ".join(list(map(lambda inv: inv.text, location.invariants)))
            location_data["invariant_label"] = deepcopy(location.view["invariant_label"])

            template_data["locations"].append(location_data)

        # Parse initial location
        template_data["init_loc_id"] = template.init_loc.id

        ###############
        # Parse edges #
        ###############
        template_data["edges"] = []
        for edge_id, edge in template.edges.items():
            edge_data = OrderedDict()
            edge_data["id"] = edge_id

            edge_data["source_loc_id"] = edge.source.id
            edge_data["target_loc_id"] = edge.target.id

            # Parse edge labels
            edge_data["guard"] = " && ".join(list(map(lambda clock_grd: clock_grd.text, edge.clock_guards)) + list(
                map(lambda variable_grd: variable_grd.text, edge.variable_guards)))
            edge_data["guard_label"] = deepcopy(edge.view["guard_label"])
            edge_data["update"] = ",\n".join(
                list(map(lambda updt: updt.text, edge.updates)) + list(map(lambda rst: rst.text, edge.resets)))
            edge_data["update_label"] = deepcopy(edge.view["update_label"])
            edge_data["synchronisation"] = edge.sync.text if edge.sync else None
            edge_data["sync_label"] = deepcopy(edge.view["sync_label"])
            edge_data["select"] = ",\n".join(list(map(lambda sel: sel.text, edge.selects)))
            edge_data["select_label"] = deepcopy(edge.view["select_label"])

            # Parse edge nails
            edge_data["nails"] = deepcopy(edge.view["nails"])

            template_data["edges"].append(edge_data)

        system_data["templates"].append(template_data)

    #################
    # Parse queries #
    #################
    system_data["queries"] = []
    for query in system.queries:
        query_data = OrderedDict()
        # query["id"] = None
        query_data["formula"] = query.formula.text if query.formula else ""
        query_data["comment"] = query.comment

        system_data["queries"].append(query_data)

    # print(json.dumps(system, indent=2))
    return system_data


######################
# Uppaal dict to XML #
######################
def uppaal_dict_to_xml(system_data):
    """Transforms the data dictionary of a Uppaal system into an XML description.

    Args:
        system_data: The Uppaal system data dictionary.

    Returns:
        The XML description ofh the Uppaal system.
    """
    etree.Element("root")

    nta_element = etree.Element("nta")

    # Parse global declaration
    global_declaration_element = etree.SubElement(nta_element, "declaration")
    global_declaration_element.text = system_data["global_declaration"]

    ###################
    # Parse templates #
    ###################
    for template_data in system_data["templates"]:
        template_element = etree.SubElement(nta_element, "template")

        template_name_element = etree.SubElement(template_element, "name")
        template_name_element.text = template_data["name"]

        template_parameters_element = etree.SubElement(template_element, "parameter")
        template_parameters_element.text = template_data["parameters"]

        template_declaration_element = etree.SubElement(template_element, "declaration")
        template_declaration_element.text = template_data["declaration"]

        ###################
        # Parse locations #
        ###################
        for location_data in template_data["locations"]:
            location_element = etree.SubElement(template_element, "location", id=location_data["id"],
                                                x=str(location_data["pos"]["x"]), y=str(location_data["pos"]["y"]))

            if location_data["name"] and location_data["name_label"]:
                location_name_element = etree.SubElement(location_element, "name",
                                                         x=str(location_data["name_label"]["pos"]["x"]),
                                                         y=str(location_data["name_label"]["pos"]["y"]))
                location_name_element.text = location_data["name"]

            if location_data["urgent"]:
                etree.SubElement(location_element, "urgent")

            if location_data["committed"]:
                etree.SubElement(location_element, "committed")

            if location_data["invariant"] and location_data["invariant_label"]:
                invariant_label_element = etree.SubElement(location_element, "label", kind="invariant",
                                                           x=str(location_data["invariant_label"]["pos"]["x"]),
                                                           y=str(location_data["invariant_label"]["pos"]["y"]))
                invariant_label_element.text = location_data["invariant"]

        # Parse initial location
        if template_data["init_loc_id"]:
            etree.SubElement(template_element, "init", ref=template_data["init_loc_id"])

        ###############
        # Parse edges #
        ###############
        for edge_data in template_data["edges"]:
            edge_element = etree.SubElement(template_element, "transition")

            etree.SubElement(edge_element, "source", ref=edge_data["source_loc_id"])
            etree.SubElement(edge_element, "target", ref=edge_data["target_loc_id"])

            # Guard
            if edge_data["guard"] and edge_data["guard_label"]:
                guard_label_element = etree.SubElement(edge_element, "label", kind="guard",
                                                       x=str(edge_data["guard_label"]["pos"]["x"]),
                                                       y=str(edge_data["guard_label"]["pos"]["y"]))
                guard_label_element.text = edge_data["guard"]

            # Update / Assignment
            if edge_data["update"] and edge_data["update_label"]:
                update_label_element = etree.SubElement(edge_element, "label", kind="assignment",
                                                        x=str(edge_data["update_label"]["pos"]["x"]),
                                                        y=str(edge_data["update_label"]["pos"]["y"]))
                update_label_element.text = edge_data["update"]

            # Synchronisation
            if edge_data["synchronisation"] and edge_data["sync_label"]:
                sync_label_element = etree.SubElement(edge_element, "label", kind="synchronisation",
                                                      x=str(edge_data["sync_label"]["pos"]["x"]),
                                                      y=str(edge_data["sync_label"]["pos"]["y"]))
                sync_label_element.text = edge_data["synchronisation"]

            # Select
            if edge_data["select"] and edge_data["select_label"]:
                select_label_element = etree.SubElement(edge_element, "label", kind="select",
                                                        x=str(edge_data["select_label"]["pos"]["x"]),
                                                        y=str(edge_data["select_label"]["pos"]["y"]))
                select_label_element.text = edge_data["select"]

            # Parse edge nails
            for nail_data in edge_data["nails"]:
                etree.SubElement(template_element, "nail", x=str(nail_data["pos"]["x"]), y=str(nail_data["pos"]["y"]))

    # Parse system declaration
    system_declaration_element = etree.SubElement(nta_element, "system")
    system_declaration_element.text = system_data["system_declaration"]

    #################
    # Parse queries #
    #################
    if "queries" in system_data:
        root_query_element = etree.SubElement(nta_element, "queries")
        for query_data in system_data["queries"]:
            query_element = etree.SubElement(root_query_element, "query")

            formula_element = etree.SubElement(query_element, "formula")
            formula_element.text = query_data["formula"]

            comment_element = etree.SubElement(query_element, "comment")
            comment_element.text = query_data["comment"]

    ##############################
    # Convert XML Tree to string #
    ##############################
    system_xml_str = etree.tostring(nta_element, encoding='utf-8', method='xml', xml_declaration=True,
                                    pretty_print=True)
    system_xml_str = system_xml_str.decode('utf-8')
    system_xml_str = system_xml_str.replace("encoding='utf8'", "encoding='utf-8'")
    return system_xml_str


########################
# Uppaal system to XML #
########################
def uppaal_system_to_xml(system):
    """Transforms the Uppaal system object into an XML description.

    Args:
        system: The Uppaal system object.

    Returns:
        The Uppaal system XML string.
    """
    system_data = uppaal_system_to_dict(system)
    system_xml_str = uppaal_dict_to_xml(system_data)
    return system_xml_str
