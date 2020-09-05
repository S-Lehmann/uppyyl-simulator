################
# Queries #
################

test_uppaal_query_data = {
    "all_globally": {
        "text": "A[] p",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropAll',
            'prop': {
                'astType': 'PropGlobally',
                'prop': {
                    'astType': 'Predicate',
                    'expr': {
                        'astType': 'Variable',
                        'name': 'p'}}}},
        "pre": [],
        "res_state": {},
    },
    "all_finally": {
        "text": "A<> p",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropAll',
            'prop': {
                'astType': 'PropFinally',
                'prop': {
                    'astType': 'Predicate',
                    'expr': {
                        'astType': 'Variable',
                        'name': 'p'}}}},
        "pre": [],
        "res_state": {},
    },
    "exists_globally": {
        "text": "E[] p",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropExists',
            'prop': {
                'astType': 'PropGlobally',
                'prop': {
                    'astType': 'Predicate',
                    'expr': {
                        'astType': 'Variable',
                        'name': 'p'}}}},
        "pre": [],
        "res_state": {},
    },
    "exists_finally": {
        "text": "E<> p",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropExists',
            'prop': {
                'astType': 'PropFinally',
                'prop': {
                    'astType': 'Predicate',
                    'expr': {
                        'astType': 'Variable',
                        'name': 'p'}}}},
        "pre": [],
        "res_state": {},
    },
    "leads_to": {
        "text": "p --> q",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropLeadsTo',
            'left': {
                'astType': 'Predicate',
                'expr': {'astType': 'Variable', 'name': 'p'}},
            'right': {
                'astType': 'Predicate',
                'expr': {'astType': 'Variable', 'name': 'q'}}},
        "pre": [],
        "res_state": {},
    },
    "complex_formula": {
        "text": "E<> (x>10 && pred || y<10)",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropExists',
            'prop': {
                'astType': 'PropFinally',
                'prop': {
                    'astType': 'Predicate',
                    'expr': {
                        'astType': 'BracketExpr',
                        'expr': {
                            'astType': 'BinaryExpr',
                            'left': {
                                'astType': 'BinaryExpr',
                                'left': {
                                    'astType': 'BinaryExpr',
                                    'left': {'astType': 'Variable', 'name': 'x'},
                                    'op': 'GreaterThan',
                                    'right': {'astType': 'Integer', 'val': 10}},
                                'op': 'LogAnd',
                                'right': {'astType': 'Variable', 'name': 'pred'}},
                            'op': 'LogOr',
                            'right': {
                                'astType': 'BinaryExpr',
                                'left': {'astType': 'Variable', 'name': 'y'},
                                'op': 'LessThan',
                                'right': {'astType': 'Integer', 'val': 10}}}}}}},
        "pre": [],
        "res_state": {},
    },
    "infimum_without_predicate": {
        "text": "inf: x,y",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropValBounds',
            'exprs': [{'astType': 'Variable', 'name': 'x'},
                      {'astType': 'Variable', 'name': 'y'}],
            'predicate': None,
            'type': 'inf'},
        "pre": [],
        "res_state": {},
    },
    "infimum_with_predicate": {
        "text": "inf{pred}: x,y",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropValBounds',
            'exprs': [{'astType': 'Variable', 'name': 'x'},
                      {'astType': 'Variable', 'name': 'y'}],
            'predicate': {
                'astType': 'Predicate',
                'expr': {
                    'astType': 'Variable', 'name': 'pred'}},
            'type': 'inf'},
        "pre": [],
        "res_state": {},
    },
    "supremum_without_predicate": {
        "text": "sup: x,y",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropValBounds',
            'exprs': [{'astType': 'Variable', 'name': 'x'},
                      {'astType': 'Variable', 'name': 'y'}],
            'predicate': None,
            'type': 'sup'},
        "pre": [],
        "res_state": {},
    },
    "supremum_with_predicate": {
        "text": "sup{pred}: x,y",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropValBounds',
            'exprs': [{'astType': 'Variable', 'name': 'x'},
                      {'astType': 'Variable', 'name': 'y'}],
            'predicate': {
                'astType': 'Predicate',
                'expr': {
                    'astType': 'Variable', 'name': 'pred'}},
            'type': 'sup'},
        "pre": [],
        "res_state": {},
    },
}

test_uppaal_smc_query_data = {
    "simulate": {
        "text": "simulate 10 [<= 20] {x,y}",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCSim',
            'obsVars': [{'astType': 'Variable', 'name': 'x'},
                        {'astType': 'Variable', 'name': 'y'}],
            'runCount': {'astType': 'Integer', 'val': 10},
            'timeBound': {
                'astType': 'PropTimeBound',
                'upperBound': {'astType': 'Integer', 'val': 20},
                'var': None}},
        "pre": [],
        "res_state": {},
    },
    "simulate_accept_runs": {
        "text": "simulate 10 [<= 20] {dummy} : 10 : (pred)",
        "rule": "UppaalProp",
        "ast": {
            'acceptBound': {'astType': 'Integer', 'val': 10},
            'astType': 'PropSMCSimAcceptRuns',
            'predicate': {
                'astType': 'Predicate',
                'expr': {
                    'astType': 'Variable', 'name': 'pred'}},
            'simulate': {
                'astType': 'PropSMCSim',
                'obsVars': [{'astType': 'Variable', 'name': 'dummy'}],
                'runCount': {'astType': 'Integer', 'val': 10},
                'timeBound': {
                    'astType': 'PropTimeBound',
                    'upperBound': {'astType': 'Integer', 'val': 20},
                    'var': None}}},
        "pre": [],
        "res_state": {},
    },
    "probability_estimation_finally": {
        "text": "Pr [<=20] (<> prop)",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCProbEstimate',
            'prop': {
                'astType': 'PropFinally',
                'prop': {
                    'astType': 'Predicate',
                    'expr': {'astType': 'Variable', 'name': 'prop'}}},
            'timeBound': {
                'astType': 'PropTimeBound',
                'upperBound': {'astType': 'Integer', 'val': 20},
                'var': None}},
        "pre": [],
        "res_state": {},
    },
    "probability_estimation_globally": {
        "text": "Pr [<=20] ([] prop)",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCProbEstimate',
            'prop': {
                'astType': 'PropGlobally',
                'prop': {
                    'astType': 'Predicate',
                    'expr': {'astType': 'Variable', 'name': 'prop'}}},
            'timeBound': {
                'astType': 'PropTimeBound',
                'upperBound': {'astType': 'Integer', 'val': 20},
                'var': None}},
        "pre": [],
        "res_state": {},
    },
    "probability_estimation_until": {
        "text": "Pr [<=20] (prop1 U prop2)",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCProbEstimate',
            'prop': {
                'astType': 'PropUntil',
                'left': {
                    'astType': 'Predicate',
                    'expr': {'astType': 'Variable', 'name': 'prop1'}},
                'right': {
                    'astType': 'Predicate',
                    'expr': {'astType': 'Variable', 'name': 'prop2'}}},
            'timeBound': {
                'astType': 'PropTimeBound',
                'upperBound': {'astType': 'Integer', 'val': 20},
                'var': None}},
        "pre": [],
        "res_state": {},
    },
    "hypothesis_test": {
        "text": "Pr [<=20] (<> prop) <= 0.6",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCHypothesisTest',
            'op': '<=',
            'probVal': {'astType': 'Double', 'val': 0.6},
            'prop': {
                'astType': 'PropSMCProbEstimate',
                'prop': {
                    'astType': 'PropFinally',
                    'prop': {
                        'astType': 'Predicate',
                        'expr': {'astType': 'Variable', 'name': 'prop'}}},
                'timeBound': {
                    'astType': 'PropTimeBound',
                    'upperBound': {'astType': 'Integer', 'val': 20},
                    'var': None}}},
        "pre": [],
        "res_state": {},
    },
    "probability_comparison": {
        "text": "Pr [<=20] (<> prop1) <= Pr [<=20] (<> prop2)",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCProbCompare',
            'left': {
                'astType': 'PropSMCProbEstimate',
                'prop': {
                    'astType': 'PropFinally',
                    'prop': {
                        'astType': 'Predicate',
                        'expr': {'astType': 'Variable', 'name': 'prop1'}}},
                'timeBound': {
                    'astType': 'PropTimeBound',
                    'upperBound': {'astType': 'Integer', 'val': 20},
                    'var': None}},
            'op': '<=',
            'right': {
                'astType': 'PropSMCProbEstimate',
                'prop': {
                    'astType': 'PropFinally',
                    'prop': {'astType': 'Predicate',
                             'expr': {'astType': 'Variable', 'name': 'prop2'}}},
                'timeBound': {
                    'astType': 'PropTimeBound',
                    'upperBound': {'astType': 'Integer', 'val': 20},
                    'var': None}}},
        "pre": [],
        "res_state": {},
    },
    "value_estimation_min": {
        "text": "E[<=20; 10] (min: x)",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCValueEstimate',
            'expr': {'astType': 'Variable', 'name': 'x'},
            'op': 'min',
            'runCount': {'astType': 'Integer', 'val': 10},
            'timeBound': {
                'astType': 'PropTimeBound',
                'upperBound': {'astType': 'Integer', 'val': 20},
                'var': None}},
        "pre": [],
        "res_state": {},
    },
    "value_estimation_max": {
        "text": "E[<=20; 10] (max: x+1)",
        "rule": "UppaalProp",
        "ast": {
            'astType': 'PropSMCValueEstimate',
            'expr': {
                'astType': 'BinaryExpr',
                'left': {'astType': 'Variable', 'name': 'x'},
                'op': 'Add',
                'right': {'astType': 'Integer', 'val': 1}},
            'op': 'max',
            'runCount': {'astType': 'Integer', 'val': 10},
            'timeBound': {
                'astType': 'PropTimeBound',
                'upperBound': {'astType': 'Integer', 'val': 20},
                'var': None}},
        "pre": [],
        "res_state": {},
    },
}
