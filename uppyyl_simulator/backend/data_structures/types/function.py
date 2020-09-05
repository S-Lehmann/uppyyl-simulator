"""A function data type implementation for Uppaal."""

from uppyyl_simulator.backend.data_structures.types.base import UppaalType
from uppyyl_simulator.backend.data_structures.types.void import UppaalVoid


class UppaalFunction(UppaalType):
    """A Uppaal function data type."""

    def __init__(self, name, func_ast, return_clazz, c_evaluator):
        """Initializes UppaalFunction.

        Args:
            name: The function name.
            func_ast: The function ast (including parameters, body, etc.).
            return_clazz: The type (=class) of the return value.
            c_evaluator: The evaluator used for evaluation of the function ast.
        """
        self.name = name
        self.func_ast = func_ast
        self.c_evaluator = c_evaluator
        self.return_clazz = return_clazz

    def copy(self):
        """Copies the UppaalFunction instance.

        Returns:
            The copied UppaalFunction instance.
        """
        copy_obj = self.__class__(name=self.name, func_ast=self.func_ast, return_clazz=self.return_clazz,
                                  c_evaluator=self.c_evaluator)
        return copy_obj

    def __call__(self, arg_asts, state):
        state.new_local_scope()
        self.c_evaluator.initialize_parameters(param_asts=self.func_ast["params"], args=arg_asts, state=state)
        ret, do_return = self.c_evaluator.eval_ast(self.func_ast["body"],
                                                   state)  # Ignore second tuple entry, i.e., the "do_return" state
        state.remove_local_scope()

        res = self.return_clazz(ret) if (not issubclass(self.return_clazz, UppaalVoid)) else None
        return res

    def __str__(self):
        return f'Uppaal_function()'
