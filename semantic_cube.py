class SemanticCube:
    def __init__(self):
        self.types = ['int', 'float', 'bool']
        self.operations = ['+', '-', '*', '/', '&&', '||', '==', '!=', '>', '<', '>=', '<=', '=']
        self.cube = self._create_cube()

    def _create_cube(self):
        cube = {}
        for op in self.operations:
            cube[op] = {}
            for type1 in self.types:
                cube[op][type1] = {}
                for type2 in self.types:
                    # Definir las reglas del cubo semántico aquí
                    if op in ['+', '-', '*', '/']:
                        if type1 == 'int' and type2 == 'int':
                            cube[op][type1][type2] = 'int'
                        elif type1 == 'float' or type2 == 'float':
                            cube[op][type1][type2] = 'float'
                        else:
                            cube[op][type1][type2] = 'error'
                    elif op in ['&&', '||']:
                        if type1 == 'bool' and type2 == 'bool':
                            cube[op][type1][type2] = 'bool'
                        else:
                            cube[op][type1][type2] = 'error'
                    elif op in ['==', '!=', '>', '<', '>=', '<=']:
                        if type1 == type2:
                            cube[op][type1][type2] = 'bool'
                        else:
                            cube[op][type1][type2] = 'error'

                    elif op == '=':
                        if type1 == type2:
                            cube[op][type1][type2] = type1
                        elif type1 == 'float' and type2 == 'int':
                            cube[op][type1][type2] = type1
                        elif type1 == 'float' and type2 == 'bool':
                            cube[op][type1][type2] = type2
                            
                        elif type1 == 'int' and type2 == 'bool':
                            cube[op][type1][type2] = type2
                        else:
                            cube[op][type1][type2] = 'error'
        return cube

    def get_result_type(self, op, type1, type2):
        return self.cube.get(op, {}).get(type1, {}).get(type2, 'error')
    