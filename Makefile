VERSION = 0.1
PYTHON  = python3.8

# Parser paths
GRAMMAR_BASE_PATH           	  = ./uppyyl_simulator/grammars
PARSER_BASE_PATH            	  = ./uppyyl_simulator/backend/ast/parsers/generated
UPPAAL_C_PARSER_GRAMMAR           = $(GRAMMAR_BASE_PATH)/uppaal_c_language.ebnf
UPPAAL_C_PARSER_CLASS             = $(PARSER_BASE_PATH)/uppaal_c_language_parser.py

init:
	pip install -r requirements.txt

run_test:
	$(PYTHON) -m pytest $(TEST) --verbose -s

run_all_tests:
	$(PYTHON) -m pytest ./tests --verbose -s

run_coverage:
	$(PYTHON) -m coverage run --source=./uppyyl_simulator -m pytest $(TEST) --verbose -s -vv
	$(PYTHON) -m coverage report -m

run_all_coverage:
	$(PYTHON) -m coverage run --source=./uppyyl_simulator -m pytest ./tests --verbose -s -vv
	$(PYTHON) -m coverage report -m

run_experiment:
	$(PYTHON) -m pytest $(EXPERIMENT) --verbose -s

run_all_experiments:
	$(PYTHON) -m pytest experiments --verbose -s

compile_all_parsers: $(UPPAAL_C_PARSER_CLASS)

$(UPPAAL_C_PARSER_CLASS): $(UPPAAL_C_PARSER_GRAMMAR)
	$(PYTHON) -m tatsu --generate-parser --name UppaalCLanguage -o "$@" "$<"

.PHONY: init run_test all_parsers
