from uppyyl_simulator.backend.data_structures.state.variable import UppaalVariable
from uppyyl_simulator.backend.data_structures.types.bool import UppaalBool
from uppyyl_simulator.backend.data_structures.types.int import UppaalInt


all_c_language_rules = [
    # "Declarations",
    "Declaration", "VariableDecls", "VariableIDInit", "VariableID", "Initialiser", "InitialiserArray",
    "TypeDecls", "Type", "Prefix", "BoundedIntType", "ScalarType", "StructType", "TypeId", "CustomType",
    "FieldDecl", "ArrayDecl",
    "Function", "Block", "Statement", "EmptyStatement", "ExprStatement",
    "ForLoop", "Iteration", "WhileLoop", "DoWhileLoop", "IfStatement", "ReturnStatement",
    # "Parameters",
    "Parameter", "System", "Process", "Instantiation", "ProgressDecl",
    "NonTypeId", "GanttDecl", "GanttDef", "GanttArgs", "GanttEntryElem", "GanttDeclSelect",
    "GanttExprList", "GantExprSingle", "GanttExprSelect", "GanttExpr", "GanttEntrySelect",
    "ChanPriority", "ChanExpr", "ChanDefault",
    "VariableIndex", "Variable", "Integer", "Double", "Boolean", "Number", "Value", "ID", "TypeID",
    "BracketExpr", "DerivativeExpr",
    "PostIncrAssignExpr", "PostDecrAssignExpr", "PreIncrAssignExpr", "PreDecrAssignExpr", "AssignExpr",
    "FuncCallExpr", "UnaryExpr", "BinaryExpr", "TernaryExpr", "Deadlock", "BasicExpression", "Expression",
    # "Arguments",
    "Assign", "Unary",
    # "Binary",
    "ForAll", "Exists", "Sum",
    "ReservedTypeKeywords", "ReservedQualKeywords", "ReservedExprKeywords", "ReservedStmtKeywords",
    "ReservedOtherKeywords", "ReservedFutureKeywords", "ReservedNonTypeKeywords", "ReservedKeywords",

    "Invariant", "Invariants",
    # "Selects", "Updates",
    "Select", "Guard", "Guards", "Sync", "Update",

    "QBracketExpr", "QFuncCallExpr", "QUnaryExpr", "QBinaryExpr", "QTernaryExpr", "QDeadlock",
    "QForAll", "QExists", "QSum", "QBasicExpression", "QExpression",
    "Predicate",
    "PropAll", "PropExists", "PropLeadsTo", "PropPathQuant",
    "PropGlobally", "PropFinally", "PropUntil", "PropPathSpecQuant", "SupInf",
    "TimeBound", "Sim", "SimAcceptRuns",
    "ProbEstimate", "HypothesisTest", "ProbCompare", "ValueEstimate",
    "UppaalTCTLProp", "UppaalSMCProp", "UppaalProp",
    "Clock", "CONST", "PROB"
]

################
# Declarations #
################
test_declaration_data = {
    "void_decl": {
        "text": "void a;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'void'}},
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'a'}]},
        "pre": [],
        "res_state": {},
    },
    "clock_decl": {
        "text": "clock c;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'clock'}},
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'c'}]},
        "pre": [],
        "res_state": {},
    },
    "chan_decl": {
        "text": "chan ch;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'chan'}},
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'ch'}]},
        "pre": [],
        "res_state": {},
    },
    "int_decl": {
        "text": "int a;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": 0,
        },
    },
    "int_decl_with_init": {
        "text": "int a = 5;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': {'astType': 'Integer', 'val': 5},
                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": 5,
        },
    },
    "multiple_int_decl": {
        "text": "int a = 1, b, c = 2;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': {'astType': 'Integer', 'val': 1},
                'varName': 'a'
            }, {
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'b'
            }, {
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': {'astType': 'Integer', 'val': 2},
                'varName': 'c'}]},
        "pre": [],
        "res_state": {
            "a": 1,
            "b": 0,
            "c": 2
        },
    },
    "bounded_int_decl": {
        "text": "int[0,10] a;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {
                    'astType': 'BoundedIntType',
                    'lower': {'astType': 'Integer', 'val': 0},
                    'upper': {'astType': 'Integer', 'val': 10}}
            },
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": 0,
        },
    },
    "bounded_int_decl_with_init": {
        "text": "int[0,10] a = 5;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {
                    'astType': 'BoundedIntType',
                    'lower': {'astType': 'Integer', 'val': 0},
                    'upper': {'astType': 'Integer', 'val': 10}}
            },
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': {'astType': 'Integer', 'val': 5},
                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": 5,
        },
    },
    "scalar_decl": {
        "text": "scalar[3] a;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {
                    'astType': 'ScalarType',
                    'expr': {'astType': 'Integer', 'val': 3}}
            },
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'a'}]},
        "pre": [],
        "res_state": {},
    },
    "struct_decl": {
        "text": "struct{ int a; bool b[2]; } st;",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {
                    'astType': 'StructType',
                    'fields': [{
                        'astType': 'FieldDecl',
                        'type': {
                            'astType': 'Type',
                            'prefixes': [],
                            'typeId': {'astType': 'CustomType', 'type': 'int'}},
                        'varData': [{'arrayDecl': [], 'astType': 'VariableID', 'varName': 'a'}]
                    }, {
                        'astType': 'FieldDecl',
                        'type': {
                            'astType': 'Type',
                            'prefixes': [],
                            'typeId': {'astType': 'CustomType', 'type': 'bool'}},
                        'varData': [{
                            'arrayDecl': [{'astType': 'Integer', 'val': 2}],
                            'astType': 'VariableID',
                            'varName': 'b'}]}]}
            },
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'st'}]},
        "pre": [],
        "res_state": {
            "st": {"a": 0, "b": [False, False]},
        },
    },
    "struct_decl_with_init": {
        "text": "struct{ int a; bool b[2]; } st = {1, {true, false}};",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {
                    'astType': 'StructType',
                    'fields': [{
                        'astType': 'FieldDecl',
                        'type': {
                            'astType': 'Type',
                            'prefixes': [],
                            'typeId': {'astType': 'CustomType', 'type': 'int'}},
                        'varData': [{'arrayDecl': [], 'astType': 'VariableID', 'varName': 'a'}]
                    }, {
                        'astType': 'FieldDecl',
                        'type': {
                            'astType': 'Type',
                            'prefixes': [],
                            'typeId': {'astType': 'CustomType', 'type': 'bool'}},
                        'varData': [{
                            'arrayDecl': [{'astType': 'Integer', 'val': 2}],
                            'astType': 'VariableID',
                            'varName': 'b'}]}]}
            },
            'varData': [{
                'arrayDecl': [],
                'astType': 'VariableID',
                'initData': {
                    'astType': 'InitialiserArray',
                    'vals': [
                        {'astType': 'Integer', 'val': 1},
                        {'astType': 'InitialiserArray',
                         'vals': [{'astType': 'Boolean', 'val': True},
                                  {'astType': 'Boolean', 'val': False}]
                         }
                    ]},
                'varName': 'st'}]},
        "pre": [],
        "res_state": {
            "st": {"a": 1, "b": [True, False]},
        },
    },
    "array_1d_decl": {
        "text": "int a[1];",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': [{
                'arrayDecl': [{'astType': 'Integer', 'val': 1}],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": [0],
        },
    },
    "array_1d_decl_with_init": {
        "text": "int a[1] = {10};",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': [{
                'arrayDecl': [{'astType': 'Integer', 'val': 1}],
                'astType': 'VariableID',
                'initData': {
                    'astType': 'InitialiserArray',
                    'vals': [
                        {'astType': 'Integer', 'val': 10}
                    ]},
                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": [10],
        },
    },
    "array_2d_decl": {
        "text": "int a[2][2];",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': [{
                'arrayDecl': [
                    {'astType': 'Integer', 'val': 2},
                    {'astType': 'Integer', 'val': 2}
                ],
                'astType': 'VariableID',
                'initData': None,
                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": [[0, 0], [0, 0]],
        },
    },
    "array_2d_decl_with_init": {
        "text": "int a[2][2] = {{1,2},{3,4}};",
        "rule": "VariableDecls",
        "ast": {
            'astType': 'VariableDecls',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': [{
                'arrayDecl': [
                    {'astType': 'Integer', 'val': 2},
                    {'astType': 'Integer', 'val': 2}
                ],
                'astType': 'VariableID',
                'initData': {
                    'astType': 'InitialiserArray',
                    'vals': [{
                        'astType': 'InitialiserArray',
                        'vals': [{'astType': 'Integer', 'val': 1},
                                 {'astType': 'Integer', 'val': 2}]
                    }, {
                        'astType': 'InitialiserArray',
                        'vals': [{'astType': 'Integer', 'val': 3},
                                 {'astType': 'Integer', 'val': 4}]}]},

                'varName': 'a'}]},
        "pre": [],
        "res_state": {
            "a": [[1, 2], [3, 4]],
        },
    },
    "function_def": {
        "text": "int func() {}",
        "rule": "Function",
        "ast": {
            'astType': 'FunctionDef',
            'body': {'astType': 'StatementBlock', 'decls': [], 'stmts': []},
            'name': 'func',
            'params': [],
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}}},
        "pre": [],
        "res_state": {},
    },
    "function_def_with_arguments": {
        "text": "void func(int a, double b, bool c) {}",
        "rule": "Function",
        "ast": {
            'astType': 'FunctionDef',
            'body': {'astType': 'StatementBlock', 'decls': [], 'stmts': []},
            'name': 'func',
            'params': [{
                'isRef': None,
                'astType': 'Parameter',
                'type': {
                    'astType': 'Type',
                    'prefixes': [],
                    'typeId': {'astType': 'CustomType', 'type': 'int'}},
                'varData': {'arrayDecl': [], 'astType': 'VariableID', 'varName': 'a'}
            }, {
                'isRef': None,
                'astType': 'Parameter',
                'type': {
                    'astType': 'Type',
                    'prefixes': [],
                    'typeId': {'astType': 'CustomType', 'type': 'double'}},
                'varData': {'arrayDecl': [], 'astType': 'VariableID', 'varName': 'b'}
            }, {
                'isRef': None,
                'astType': 'Parameter',
                'type': {
                    'astType': 'Type',
                    'prefixes': [],
                    'typeId': {'astType': 'CustomType', 'type': 'bool'}},
                'varData': {'arrayDecl': [], 'astType': 'VariableID', 'varName': 'c'}}],
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'void'}}},
        "pre": [],
        "res_state": {},
    },
    "typedef": {  # TODO: Check if typedef creates new class in "constant" space
        "text": "typedef int val_t;",
        "rule": "TypeDecls",
        "ast": {
            'astType': 'TypeDecls',
            'names': [{'arrayDecl': [], 'astType': 'VariableID', 'varName': 'val_t'}],
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}}},
        "pre": [],
        "res_state": {},
    },
}

##############
# Statements #
##############
test_statement_data = {
    "for_loop": {
        "text": "for (i1=0; i1<10; i1++) {i2++;}",
        "rule": "ForLoop",
        "ast": {
            'after': {
                'astType': 'PostIncrAssignExpr',
                'expr': {'astType': 'Variable', 'name': 'i1'}},
            'astType': 'ForLoop',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'PostIncrAssignExpr',
                        'expr': {'astType': 'Variable', 'name': 'i2'}}}]},
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Integer', 'val': 10}},
            'init': {
                'astType': 'AssignExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'Assign',
                'right': {'astType': 'Integer', 'val': 0}}},
        "pre": [],
        "res_state": {
            "i1": 10,
            "i2": 17,
        },
    },
    "iteration": {
        "text": "for (i : int[0,9]) { arr_1d[i] = 10; }",
        "rule": "Iteration",
        "ast": {
            'astType': 'Iteration',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'AssignExpr',
                        'left': {
                            'astType': 'BinaryExpr',
                            'left': {'astType': 'Variable', 'name': 'arr_1d'},
                            'op': 'ArrayAccess',
                            'right': {'astType': 'Variable', 'name': 'i'}},
                        'op': 'Assign',
                        'right': {'astType': 'Integer', 'val': 10}}}]},
            'name': 'i',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {
                    'astType': 'BoundedIntType',
                    'lower': {'astType': 'Integer', 'val': 0},
                    'upper': {'astType': 'Integer', 'val': 9}}}},
        "pre": [],
        "res_state": {
            "arr_1d": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        },
    },
    "while_loop": {
        "text": "while (i1 < 10) { i1++; }",
        "rule": "WhileLoop",
        "ast": {
            'astType': 'WhileLoop',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'PostIncrAssignExpr',
                        'expr': {'astType': 'Variable', 'name': 'i1'}}}]},
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Integer', 'val': 10}}},
        "pre": [],
        "res_state": {
            "i1": 10,
        },
    },
    "do_while_loop": {
        "text": "do { i1++; } while(i1 < 10);",
        "rule": "DoWhileLoop",
        "ast": {
            'astType': 'DoWhileLoop',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'PostIncrAssignExpr',
                        'expr': {'astType': 'Variable', 'name': 'i1'}}}]},
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Integer', 'val': 10}}},
        "pre": [],
        "res_state": {
            "i1": 10,
        },
    },
    "conditional_without_else": {
        "text": "if (i1 < i2) {i3 = i1;}",
        "rule": "IfStatement",
        "ast": {
            'astType': 'IfStatement',
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Variable', 'name': 'i2'}},
            'elseBody': None,
            'thenBody': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'AssignExpr',
                        'left': {'astType': 'Variable', 'name': 'i3'},
                        'op': 'Assign',
                        'right': {'astType': 'Variable', 'name': 'i1'}}}]}},
        "pre": [],
        "res_state": {
            "i3": 5,
        },
    },
    "conditional_with_else": {
        "text": "if (i1 > i2) {i3 = i1;} else {i3 = i2;}",
        "rule": "IfStatement",
        "ast": {
            'astType': 'IfStatement',
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'GreaterThan',
                'right': {'astType': 'Variable', 'name': 'i2'}},
            'elseBody': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'AssignExpr',
                        'left': {'astType': 'Variable', 'name': 'i3'},
                        'op': 'Assign',
                        'right': {'astType': 'Variable', 'name': 'i2'}}}]},
            'thenBody': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'AssignExpr',
                        'left': {'astType': 'Variable', 'name': 'i3'},
                        'op': 'Assign',
                        'right': {'astType': 'Variable', 'name': 'i1'}}}]}},
        "pre": [],
        "res_state": {
            "i3": 7,
        },
    },
    "statement_block": {
        "text": "{int a; a=1;}",
        "rule": "Block",
        "ast": {
            'astType': 'StatementBlock',
            'decls': [{
                'astType': 'VariableDecls',
                'type': {
                    'astType': 'Type',
                    'prefixes': [],
                    'typeId': {'astType': 'CustomType', 'type': 'int'}},
                'varData': [{
                    'arrayDecl': [],
                    'astType': 'VariableID',
                    'initData': None,
                    'varName': 'a'}]}],
            'stmts': [{
                'astType': 'ExprStatement',
                'expr': {
                    'astType': 'AssignExpr',
                    'left': {'astType': 'Variable', 'name': 'a'},
                    'op': 'Assign',
                    'right': {'astType': 'Integer', 'val': 1}}}]
        },
        "pre": [],
        "res_state": {},
    },
    "empty_statement": {
        "text": ";",
        "rule": "EmptyStatement",
        "ast": {
            'astType': 'EmptyStatement'
        },
        "pre": [],
        "res_state": {},
    },
}

test_return_statement_data = {
    "for_loop_return": {
        "text": "for (i1=0; i1<10; i1++) {return;}",
        "rule": "ForLoop",
        "ast": {
            'after': {
                'astType': 'PostIncrAssignExpr',
                'expr': {'astType': 'Variable', 'name': 'i1'}},
            'astType': 'ForLoop',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ReturnStatement',
                    'expr': None}]},
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Integer', 'val': 10}},
            'init': {
                'astType': 'AssignExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'Assign',
                'right': {'astType': 'Integer', 'val': 0}}},
        "pre": [],
        "res_state": {
            "i1": 0,
            "i2": 7,
        },
        "return_val": None,
    },
    "iteration_return": {
        "text": "for (i : int[0,9]) { return; }",
        "rule": "Iteration",
        "ast": {
            'astType': 'Iteration',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ReturnStatement',
                    'expr': None}]},
            'name': 'i',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {
                    'astType': 'BoundedIntType',
                    'lower': {'astType': 'Integer', 'val': 0},
                    'upper': {'astType': 'Integer', 'val': 9}}}},
        "pre": [],
        "res_state": {
            "arr_1d": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        },
        "return_val": None,
    },
    "while_loop_return": {
        "text": "while (i1 < 10) { return; }",
        "rule": "WhileLoop",
        "ast": {
            'astType': 'WhileLoop',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ReturnStatement',
                    'expr': None}]},
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Integer', 'val': 10}}},
        "pre": [],
        "res_state": {
            "i1": 5,
        },
        "return_val": None,
    },
    "do_while_loop_return": {
        "text": "do { return; } while(i1 < 10);",
        "rule": "DoWhileLoop",
        "ast": {
            'astType': 'DoWhileLoop',
            'body': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ReturnStatement',
                    'expr': None}]},
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Integer', 'val': 10}}},
        "pre": [],
        "res_state": {
            "i1": 5,
        },
        "return_val": None,
    },
    "conditional_without_else_return": {
        "text": "if (i1 < i2) {return;}",
        "rule": "IfStatement",
        "ast": {
            'astType': 'IfStatement',
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'LessThan',
                'right': {'astType': 'Variable', 'name': 'i2'}},
            'elseBody': None,
            'thenBody': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ReturnStatement',
                    'expr': None}]}},
        "pre": [],
        "res_state": {},
        "return_val": None,
    },
    "conditional_with_else_return": {
        "text": "if (i1 > i2) {i3 = i1;} else {return;}",
        "rule": "IfStatement",
        "ast": {
            'astType': 'IfStatement',
            'cond': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'GreaterThan',
                'right': {'astType': 'Variable', 'name': 'i2'}},
            'elseBody': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ReturnStatement',
                    'expr': None}]},
            'thenBody': {
                'astType': 'StatementBlock',
                'decls': [],
                'stmts': [{
                    'astType': 'ExprStatement',
                    'expr': {
                        'astType': 'AssignExpr',
                        'left': {'astType': 'Variable', 'name': 'i3'},
                        'op': 'Assign',
                        'right': {'astType': 'Variable', 'name': 'i1'}}}]}},
        "pre": [],
        "res_state": {
            "i3": 9,
        },
        "return_val": None,
    },
    "return": {
        "text": "return i1+i2;",
        "rule": "ReturnStatement",
        "ast": {
            'astType': 'ReturnStatement',
            'expr': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'i1'},
                'op': 'Add',
                'right': {'astType': 'Variable', 'name': 'i2'}}},
        "pre": [],
        "res_state": {
            "i3": 9,
        },
        "return_val": UppaalInt(12),
    },
}

###############
# Assignments #
###############
test_assign_data = {
    "assign": {
        "text": "i1=1",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'Assign',
            'right': {'astType': 'Integer', 'val': 1}},
        "val": UppaalInt(1),
        "res_state": {
            "i1": 1,
        },
    },
    "add_assign": {
        "text": "i1+=1",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'AddAssign',
            'right': {'astType': 'Integer', 'val': 1}},
        "val": UppaalInt(6),
        "res_state": {
            "i1": 6,
        },
    },
    "sub_assign": {
        "text": "i1-=1",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'SubAssign',
            'right': {'astType': 'Integer', 'val': 1}},
        "val": UppaalInt(4),
        "res_state": {
            "i1": 4,
        },
    },
    "mult_assign": {
        "text": "i1*=2",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'MultAssign',
            'right': {'astType': 'Integer', 'val': 2}},
        "val": UppaalInt(10),
        "res_state": {
            "i1": 10,
        },
    },
    "div_assign": {
        "text": "i1/=3",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'DivAssign',
            'right': {'astType': 'Integer', 'val': 3}},
        "val": UppaalInt(1),
        "res_state": {
            "i1": 1,
        },
    },
    "mod_assign": {
        "text": "i1%=3",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'ModAssign',
            'right': {'astType': 'Integer', 'val': 3}},
        "val": UppaalInt(2),
        "res_state": {
            "i1": 2,
        },
    },
    "l_shift_assign": {
        "text": "i1<<=2",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'LShiftAssign',
            'right': {'astType': 'Integer', 'val': 2}},
        "val": UppaalInt(20),
        "res_state": {
            "i1": 20,
        },
    },
    "r_shift_assign": {
        "text": "i1>>=2",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'RShiftAssign',
            'right': {'astType': 'Integer', 'val': 2}},
        "val": UppaalInt(1),
        "res_state": {
            "i1": 1,
        },
    },
    "bit_and_assign": {
        "text": "i1&=3",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'BitAndAssign',
            'right': {'astType': 'Integer', 'val': 3}},
        "val": UppaalInt(1),
        "res_state": {
            "i1": 1,
        },
    },
    "bit_or_assign": {
        "text": "i1|=3",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'BitOrAssign',
            'right': {'astType': 'Integer', 'val': 3}},
        "val": UppaalInt(7),
        "res_state": {
            "i1": 7,
        },
    },
    "bit_xor_assign": {
        "text": "i1^=3",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'BitXorAssign',
            'right': {'astType': 'Integer', 'val': 3}},
        "val": UppaalInt(6),
        "res_state": {
            "i1": 6,
        },
    },

    # Increment / Decrement
    "post_incr": {
        "text": "i1++",
        "rule": "Expression",
        "ast": {
            'astType': 'PostIncrAssignExpr',
            'expr': {'astType': 'Variable', 'name': 'i1'}},
        "val": UppaalInt(5),
        "res_state": {
            "i1": 6,
        },
    },
    "post_decr": {
        "text": "i1--",
        "rule": "Expression",
        "ast": {
            'astType': 'PostDecrAssignExpr',
            'expr': {'astType': 'Variable', 'name': 'i1'}},
        "val": UppaalInt(5),
        "res_state": {
            "i1": 4,
        },
    },
    "pre_incr": {
        "text": "++i1",
        "rule": "Expression",
        "ast": {
            'astType': 'PreIncrAssignExpr',
            'expr': {'astType': 'Variable', 'name': 'i1'}},
        "val": UppaalInt(6),
        "res_state": {
            "i1": 6,
        },
    },
    "pre_decr": {
        "text": "--i1",
        "rule": "Expression",
        "ast": {
            'astType': 'PreDecrAssignExpr',
            'expr': {'astType': 'Variable', 'name': 'i1'}},
        "val": UppaalInt(4),
        "res_state": {
            "i1": 4,
        },
    }
}

###############
# Expressions #
###############
test_expr_data = {
    # Atomic values
    "positive_int": {
        "text": "1",
        "rule": "Integer",
        "ast": {'astType': 'Integer', 'val': 1},
        "pre": [],
        "val": UppaalInt(1)
    },
    "negative_int": {
        "text": "-1",
        "rule": "Integer",
        "ast": {'astType': 'Integer', 'val': -1},
        "pre": [],
        "val": UppaalInt(-1)
    },
    "true_bool": {
        "text": "true",
        "rule": "Boolean",
        "ast": {'astType': 'Boolean', 'val': True},
        "pre": [],
        "val": UppaalBool(True)
    },
    "false_bool": {
        "text": "false",
        "rule": "Boolean",
        "ast": {'astType': 'Boolean', 'val': False},
        "pre": [],
        "val": UppaalBool(False)
    },

    # Simple Expressions
    "addition": {
        "text": "1 + 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 1},
            'op': 'Add',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(3),
    },
    "subtraction": {
        "text": "1 - 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 1},
            'op': 'Sub',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(-1),
    },
    "multiplication": {
        "text": "1 * 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 1},
            'op': 'Mult',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(2),
    },
    "division": {
        "text": "10 / 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 10},
            'op': 'Div',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(5),
    },
    "modulo": {
        "text": "10 % 3",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 10},
            'op': 'Mod',
            'right': {'astType': 'Integer', 'val': 3}},
        "pre": [],
        "val": UppaalInt(1),
    },
    "plus": {
        "text": "+i1",
        "rule": "Expression",
        "ast": {
            'astType': 'UnaryExpr',
            'expr': {'astType': 'Variable', 'name': 'i1'},
            'op': 'Plus'},
        "pre": [],
        "val": UppaalInt(5),
    },
    "minus": {
        "text": "-i1",
        "rule": "Expression",
        "ast": {
            'astType': 'UnaryExpr',
            'expr': {'astType': 'Variable', 'name': 'i1'},
            'op': 'Minus'},
        "pre": [],
        "val": UppaalInt(-5),
    },
    "log_not": {
        "text": "!true",
        "rule": "Expression",
        "ast": {
            'astType': 'UnaryExpr',
            'expr': {'astType': 'Boolean', 'val': True},
            'op': 'LogNot'},
        "pre": [],
        "val": UppaalBool(False),
    },
    "left_shift": {
        "text": "4 << 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'LShift',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(16),
    },
    "right_shift": {
        "text": "4 >> 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'RShift',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(1),
    },
    "log_and": {
        "text": "true && false",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Boolean', 'val': True},
            'op': 'LogAnd',
            'right': {'astType': 'Boolean', 'val': False}},
        "pre": [],
        "val": UppaalBool(False),
    },
    "log_or": {
        "text": "true || false",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Boolean', 'val': True},
            'op': 'LogOr',
            'right': {'astType': 'Boolean', 'val': False}},
        "pre": [],
        "val": UppaalBool(True),
    },
    "log_imply": {
        "text": "true imply false",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Boolean', 'val': True},
            'op': 'LogImply',
            'right': {'astType': 'Boolean', 'val': False}},
        "pre": [],
        "val": UppaalBool(False),
    },
    "bit_and": {
        "text": "6 & 3",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 6},
            'op': 'BitAnd',
            'right': {'astType': 'Integer', 'val': 3}},
        "pre": [],
        "val": UppaalInt(2),
    },
    "bit_or": {
        "text": "6 | 3",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 6},
            'op': 'BitOr',
            'right': {'astType': 'Integer', 'val': 3}},
        "pre": [],
        "val": UppaalInt(7),
    },
    "bit_xor": {
        "text": "6 ^ 3",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 6},
            'op': 'BitXor',
            'right': {'astType': 'Integer', 'val': 3}},
        "pre": [],
        "val": UppaalInt(5),
    },
    "minimum": {
        "text": "2 <? 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 2},
            'op': 'Minimum',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalInt(2),
    },
    "maximum": {
        "text": "2 >? 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 2},
            'op': 'Maximum',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalInt(4),
    },
    "greater_equal": {
        "text": "4 >= 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'GreaterEqual',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalBool(True),
    },
    "greater_than": {
        "text": "4 > 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'GreaterThan',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalBool(False),
    },
    "less_equal": {
        "text": "4 <= 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'LessEqual',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalBool(True),
    },
    "less_than": {
        "text": "4 < 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'LessThan',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalBool(False),
    },
    "equal": {
        "text": "4 == 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'Equal',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalBool(True),
    },
    "not_equal": {
        "text": "4 != 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 4},
            'op': 'NotEqual',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalBool(False),
    },

    # Precedence and Associativity
    "precedence_1": {
        "text": "1*2 + 3",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 1},
                'op': 'Mult',
                'right': {'astType': 'Integer', 'val': 2}},
            'op': 'Add',
            'right': {'astType': 'Integer', 'val': 3}},
        "pre": [],
        "val": UppaalInt(5)
    },
    "precedence_2": {
        "text": "3 + 1*2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {'astType': 'Integer', 'val': 3},
            'op': 'Add',
            'right': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 1},
                'op': 'Mult',
                'right': {'astType': 'Integer', 'val': 2}}},
        "pre": [],
        "val": UppaalInt(5)
    },
    "precedence_3": {
        "text": "1*2 + 3*4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 1},
                'op': 'Mult',
                'right': {'astType': 'Integer', 'val': 2}},
            'op': 'Add',
            'right': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 3},
                'op': 'Mult',
                'right': {'astType': 'Integer', 'val': 4}}},
        "pre": [],
        "val": UppaalInt(14)
    },
    "associativity_1": {
        "text": "1 + 2 + 3 + 4",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {
                'astType': 'BinaryExpr',
                'left': {
                    'astType': 'BinaryExpr',
                    'left': {'astType': 'Integer', 'val': 1},
                    'op': 'Add',
                    'right': {'astType': 'Integer', 'val': 2}},
                'op': 'Add',
                'right': {'astType': 'Integer', 'val': 3}},
            'op': 'Add',
            'right': {'astType': 'Integer', 'val': 4}},
        "pre": [],
        "val": UppaalInt(10)
    },
    "associativity_2": {
        "text": "i1 = i2 = i3 = 4",
        "rule": "Expression",
        "ast": {
            'astType': 'AssignExpr',
            'left': {'astType': 'Variable', 'name': 'i1'},
            'op': 'Assign',
            'right': {
                'astType': 'AssignExpr',
                'left': {'astType': 'Variable', 'name': 'i2'},
                'op': 'Assign',
                'right': {
                    'astType': 'AssignExpr',
                    'left': {'astType': 'Variable', 'name': 'i3'},
                    'op': 'Assign',
                    'right': {'astType': 'Integer', 'val': 4}}}},
        "pre": [],
        "val": UppaalInt(4)
    },

    # Dot access
    "dot_access_1": {
        "text": "1 + s.val1 + i1",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 1},
                'op': 'Add',
                'right': {
                    'astType': 'BinaryExpr',
                    'left': {'astType': 'Variable', 'name': 's'},
                    'op': 'Dot',
                    'right': {'astType': 'Variable', 'name': 'val1'}}},
            'op': 'Add',
            'right': {'astType': 'Variable', 'name': 'i1'}},
        "pre": [],
        "val": UppaalInt(16)
    },
    "dot_access_2": {
        "text": "1 + s.val2.subval1 + 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 1},
                'op': 'Add',
                'right': {
                    'astType': 'BinaryExpr',
                    'left': {
                        'astType': 'BinaryExpr',
                        'left': {'astType': 'Variable', 'name': 's'},
                        'op': 'Dot',
                        'right': {'astType': 'Variable', 'name': 'val2'}},
                    'op': 'Dot',
                    'right': {'astType': 'Variable', 'name': 'subval1'}}},
            'op': 'Add',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(23)
    },

    # Array access
    "array_access": {
        "text": "arr_2d[0][1]",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'arr_2d'},
                'op': 'ArrayAccess',
                'right': {'astType': 'Integer', 'val': 0}},
            'op': 'ArrayAccess',
            'right': {'astType': 'Integer', 'val': 1}},
        "pre": [],
        "val": UppaalVariable(name="arr_2d[0][1]", val=UppaalInt(2))
    },

    # Complex expressions
    "complex": {
        "text": "1*2 + 3*4%2 - 1 << 2",
        "rule": "Expression",
        "ast": {
            'astType': 'BinaryExpr',
            'left': {
                'astType': 'BinaryExpr',
                'left': {
                    'astType': 'BinaryExpr',
                    'left': {
                        'astType': 'BinaryExpr',
                        'left': {'astType': 'Integer', 'val': 1},
                        'op': 'Mult',
                        'right': {'astType': 'Integer', 'val': 2}},
                    'op': 'Add',
                    'right': {
                        'astType': 'BinaryExpr',
                        'left': {
                            'astType': 'BinaryExpr',
                            'left': {'astType': 'Integer', 'val': 3},
                            'op': 'Mult',
                            'right': {'astType': 'Integer', 'val': 4}},
                        'op': 'Mod',
                        'right': {'astType': 'Integer', 'val': 2}}},
                'op': 'Sub',
                'right': {'astType': 'Integer', 'val': 1}},
            'op': 'LShift',
            'right': {'astType': 'Integer', 'val': 2}},
        "pre": [],
        "val": UppaalInt(4)
    },

    # Ternary expressions
    "ternary_1": {
        "text": "b_true ? 1+2 : 2*3",
        "rule": "Expression",
        "ast": {
            'astType': 'TernaryExpr',
            'left': {'astType': 'Variable', 'name': 'b_true'},
            'middle': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 1},
                'op': 'Add',
                'right': {'astType': 'Integer', 'val': 2}},
            'op': 'Ternary',
            'right': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 2},
                'op': 'Mult',
                'right': {'astType': 'Integer', 'val': 3}}},
        "pre": [],
        "val": UppaalInt(3)
    },
    "ternary_2": {
        "text": "b_false ? 1+2 : 2*3",
        "rule": "Expression",
        "ast": {
            'astType': 'TernaryExpr',
            'left': {'astType': 'Variable', 'name': 'b_false'},
            'middle': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 1},
                'op': 'Add',
                'right': {'astType': 'Integer', 'val': 2}},
            'op': 'Ternary',
            'right': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Integer', 'val': 2},
                'op': 'Mult',
                'right': {'astType': 'Integer', 'val': 3}}},
        "pre": [],
        "val": UppaalInt(6)
    },

    # Function
    "function_call": {
        "text": "f()",
        "rule": "Expression",
        "ast": {
            'args': [],
            'astType': 'FuncCallExpr',
            'funcName': 'f'
        },
        "pre": [],
        "val": None
    },
}

######################
# System Declaration #
######################
test_system_declaration_data = {
    "system_1": {
        "text": "system P, Q, R;",
        "rule": "System",
        "ast": {
            'astType': 'System',
            'processNames': [['P', 'Q', 'R']]},
    },
    "system_2": {
        "text": "system P, Q < R < S;",
        "rule": "System",
        "ast": {
            'astType': 'System',
            'processNames': [['P', 'Q'], ['R'], ['S']]},
    },
    "process": {
        "text": "Proc(1, 2+3)",
        "rule": "Process",
        "ast": {
            'args': [{'astType': 'Integer', 'val': 1},
                     {'astType': 'BinaryExpr',
                      'left': {'astType': 'Integer', 'val': 2},
                      'op': 'Add',
                      'right': {'astType': 'Integer', 'val': 3}}],
            'astType': 'Process',
            'name': 'Proc'},
    },
    "instantiation_1": {
        "text": "Inst1 = Tmpl(1, true);",
        "rule": "Instantiation",
        "ast": {
            'args': [{'astType': 'Integer', 'val': 1},
                     {'astType': 'Boolean', 'val': True}],
            'astType': 'Instantiation',
            'instanceName': 'Inst1',
            'params': None,
            'templateName': 'Tmpl'},
    },
    "instantiation_2": {
        "text": "Inst1(int &x, const int i) = Tmpl(x, i);",
        "rule": "Instantiation",
        "ast": {
            'args': [{'astType': 'Variable', 'name': 'x'},
                     {'astType': 'Variable', 'name': 'i'}],
            'astType': 'Instantiation',
            'instanceName': 'Inst1',
            'params': [{
                'isRef': '&',
                'astType': 'Parameter',
                'type': {'astType': 'Type',
                         'prefixes': [],
                         'typeId': {'astType': 'CustomType', 'type': 'int'}},
                'varData': {'arrayDecl': [],
                            'astType': 'VariableID',
                            'varName': 'x'}
            }, {
                'isRef': None,
                'astType': 'Parameter',
                'type': {'astType': 'Type',
                         'prefixes': ['const'],
                         'typeId': {'astType': 'CustomType', 'type': 'int'}},
                'varData': {'arrayDecl': [],
                            'astType': 'VariableID',
                            'varName': 'i'}}],
            'templateName': 'Tmpl'},
    },
    "parameters_1": {
        "text": "int &x",
        "rule": "Parameter",
        "ast": {
            'isRef': '&',
            'astType': 'Parameter',
            'type': {
                'astType': 'Type',
                'prefixes': [],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': {'arrayDecl': [], 'astType': 'VariableID', 'varName': 'x'}},
    },
    "parameters_2": {
        "text": "const int i",
        "rule": "Parameter",
        "ast": {
            'isRef': None,
            'astType': 'Parameter',
            'type': {
                'astType': 'Type',
                'prefixes': ['const'],
                'typeId': {'astType': 'CustomType', 'type': 'int'}},
            'varData': {'arrayDecl': [], 'astType': 'VariableID', 'varName': 'i'}},
    },
}
