class VariableTable:
    def __init__(self):
        self.variables = {}

    def add_variable(self, name, var_type):
        if name in self.variables:
            raise Exception(f"Variable '{name}' ya declarada.")
        self.variables[name] = var_type

    def get_variable(self, name):
        return self.variables.get(name, None)

    def __repr__(self):
        return f"VariableTable({self.variables})"

class FunctionDirectory:
    def __init__(self):
        self.functions = {}

    def add_function(self, name, return_type, params):
        if name in self.functions:
            raise Exception(f"Function '{name}' ya declarada.")
        self.functions[name] = {
            'return_type': return_type,
            'params': params,
            'variables': VariableTable()
        }

    def add_variable_to_function(self, function_name, var_name, var_type):
        if function_name not in self.functions:
            raise Exception(f"Function '{function_name}' no declarada.")
        self.functions[function_name]['variables'].add_variable(var_name, var_type)

    def get_function(self, name):
        return self.functions.get(name, None)

    def __repr__(self):
        return f"FunctionDirectory({self.functions})"
