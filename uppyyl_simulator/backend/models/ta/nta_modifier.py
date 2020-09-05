"""This module implements modifiers for Uppaal NTA systems."""

import copy

from uppyyl_simulator.backend.data_structures.ast.ast_code_element import (
    apply_func_to_ast
)


##################
# SystemModifier #
##################

class SystemModifier:
    """This class provides the modifiers for Uppaal NTA systems."""

    def __init__(self):
        """Initializes SystemModifier."""
        pass

    @staticmethod
    def move_sys_vars_to_global_decl(system):
        """Moves all variable declarations in the system declaration section to the global declaration.

        Args:
            system: The system object.

        Returns:
            None
        """

        instance_asts = system.system_declaration.ast.instances
        global_stmts = system.declaration.ast.decls
        for i in range(0, len(instance_asts)):
            instance_ast = instance_asts[i]
            if instance_ast.type_ == "VarDecl" or instance_ast.type_ == "TypeDef" or instance_ast.type_ == "FuncDef":
                global_stmts.append(instance_ast)
                instance_asts.splice(i, 1)
                i -= 1
        system.declaration.update_text()
        system.system_declaration.update_text()

    @staticmethod
    def convert_instances_to_templates(system, keep_original_templates=True):
        """Generate a template for each automata instance (optionally keep original templates).

        Args:
            system: The system object
            keep_original_templates: Defines whether the original templates should be kept or not

        Returns:

        """
        # Gather instance data from system declaration AST
        instance_data = []
        instance_asts = system.system_declaration.ast.instances
        for i in range(0, len(instance_asts)):
            instance_ast = instance_asts[i]
            if instance_ast.type_ == "TemplateInstance":
                instance_data.append(instance_ast)

        # Create templates based on instance data
        old_tmpls = []
        new_tmpls = []
        for i in range(0, len(instance_data)):
            single_inst_data = instance_data[i]
            inst_name = single_inst_data.instance_name
            tmpl_name = single_inst_data.template_name
            if not (tmpl_name in old_tmpls):
                old_tmpls.append(tmpl_name)

            new_tmpl = system.new_template(f'{inst_name}_tmpl')
            ref_tmpl = system.get_template(tmpl_name)
            new_tmpl.assign_from(ref_tmpl)
            system.templates[new_tmpl.id] = new_tmpl

            new_tmpls.append(new_tmpl)

            # Convert all variables defined in the local declaration to global ones
            system.convert_local_vars_to_global_vars(new_tmpl)

            # Replace all template argument variables with their respective input variables
            var_replacements = []
            for j in range(0, len(single_inst_data)):
                arg_input = single_inst_data.args[j]
                arg_name = new_tmpl.parameters[j].var_name
                var_replacements.append({
                    "select_func": (lambda name: (lambda ast: ast.type_ == 'Variable' and ast.name == name))(arg_name),
                    "adapt_func": (lambda inp: (lambda ast: copy.deepcopy(inp)))(arg_input)
                })

            new_tmpl.adapt_asts(var_replacements)

            # Remove all template arguments
            new_tmpl.parameters = []

            # Remove all inputs for template arguments
            single_inst_data.args = []

        # Adapt system declaration to instantiate from new templates
        for i in range(0, len(instance_asts)):
            instance_ast = instance_asts[i]
            if instance_ast.type_ == "TemplateInstance":
                instance_ast.template_name = f'{instance_ast.instance_name}_tmpl'

        system.move_sys_vars_to_global_decl()
        system.declaration.update_text()
        system.system_declaration.update_text()

        # # Convert all variables defined in the local declaration to global ones
        # for new_tmpl in new_tmpls:
        #     SystemModifier.convert_local_vars_to_global_vars(system, new_tmpl)

        if not keep_original_templates:
            for i in range(0, len(old_tmpls)):
                tmpl = system.get_template(old_tmpls[i])
                del system.templates[tmpl.id]

    @staticmethod
    def convert_local_vars_to_global_vars(system, tmpl):
        """Convert all local template variables to global ones (requires at most one instance per template).

        Args:
            system: The system object
            tmpl: The template from which all variables should be moved to the global declaration

        Returns:
            None
        """
        if isinstance(tmpl, str):
            tmpl = system.get_template(tmpl)

        # Extract variable declarations from local declaration text
        local_var_names = []
        local_type_names = []
        local_func_names = []
        stmts = tmpl.declaration.ast.decls
        for i in range(0, len(stmts)):
            stmt = stmts[i]
            if stmt.type_ == "VarDecl":
                for j in range(0, len(stmt.var_data)):
                    local_var_names.append(stmt.var_data[j].var_name)
            elif stmt.type_ == "FuncDef":
                local_func_names.append(stmt.func_name)
            elif stmt.type_ == "TypeDef":
                for j in range(0, len(stmt.type_names)):
                    local_type_names.append(stmt.type_names[j])

        # Copy local ast
        new_global_ast_part = copy.deepcopy(tmpl.declaration.ast)

        # Replace all locally defined variables, types and functions with their global counterparts
        def local_var_adapt_func(ast, _acc):
            """Helper function for variable name adaption."""
            if ast["astType"] == 'VariableID' and ast["varName"] == local_var_names[i]:
                ast["varName"] = f'{tmpl.name}_{local_var_names[i]}'
            return ast

        def local_func_adapt_func(ast, _acc):
            """Helper function for function name adaption."""
            if ast["astType"] == 'FuncDef' and ast["name"] == local_func_names[i]:
                ast["varName"] = f'{tmpl.name}_{local_func_names[i]}'
            return ast

        def local_type_adapt_func(ast, _acc):
            """Helper function for type name adaption."""
            if ast["astType"] == 'CustomType' and ast["type"] == local_type_names[i]:
                ast["type"] = f'{tmpl.name}_{local_type_names[i]}'
            return ast

        for i in range(0, len(local_var_names)):
            new_global_ast_part = apply_func_to_ast(ast=new_global_ast_part, func=local_var_adapt_func)
            new_global_ast_part = apply_func_to_ast(ast=new_global_ast_part, func=local_func_adapt_func)
            new_global_ast_part = apply_func_to_ast(ast=new_global_ast_part, func=local_type_adapt_func)

        # Insert new global AST part into global declaration ast
        new_stmts = new_global_ast_part.decls
        for i in range(0, len(new_stmts)):
            system.declaration.ast.decls.append(new_stmts[i])

        # Update variables inside model
        var_replacements = []
        for i in range(0, len(local_var_names)):
            old_name = local_var_names[i]
            new_name = f'{tmpl.name}_{old_name}'

            def model_var_adapt_func(name):
                """Helper function for name adaption."""
                def ast_func(ast):
                    """Helper function for name adaption."""
                    if ast["astType"] == 'Variable' and ast["varName"] == name:
                        ast.name = new_name
                    return ast

                return ast_func

            var_replacements.append(model_var_adapt_func)

        tmpl.adapt_asts(var_replacements)

        # Clear local declaration
        tmpl.declaration = None

        system.declaration.update_text()
