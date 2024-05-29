from semantic_cube import SemanticCube

class VariableTable:
    

    def __init__(self):
        self.table = {}
        self.semantic_cube = SemanticCube()
        self.var_int = 0
        self.var_float = 100

        self.var_temp_int = 200
        self.var_temp_float = 300
        self.var_temp_bool = 400

        self.var_const_int = 500
        self.var_const_float = 600
        self.var_const_string = 700

        self.pila_operadores = []
        self.pila_operandos = []
        self.pila_tipos = []
        self.pila_saltos = []
        self.pila_cuadruplos = []
        self.constant_table = {}


    def append_pila_operador(self, operator):
        self.pila_operadores.append(operator)


    def add_variable(self, name, var_type):
        if name in self.table:
            raise ValueError(f"Variable '{name}' already exists in the table.")
        self.table[name] = {'type': var_type, 'memory_address':0}
        self.add_memory_address(name)


    def get_variable(self, name):
        return self.table.get(name, None)
    
    def add_memory_address(self, name):

        if self.table[name]['type'] == 'int':
            memory_address = self.var_int
            self.var_int += 1
        elif self.table[name]['type'] == 'float':
            memory_address = self.var_float
            self.var_float += 1
        self.table[name]['memory_address'] = memory_address
    
    def print_table(self):
        for var_name, details in self.table.items():
            print(f"Variable: {var_name}, Type: {details['type']}")
    
    def add_operand(self, operand, is_cte = False):
        try:
            if is_cte:
                #append de la direccion de memoria del numero
                tipo = type(operand).__name__
                if tipo == 'int':
                    if operand not in self.constant_table:
                        self.var_const_int+= 1
                        self.constant_table[operand] = self.var_const_int

                    self.pila_operandos.append(self.constant_table[operand])
                    self.pila_tipos.append(tipo)

                elif tipo == 'float':
                    if operand not in self.constant_table:
                        self.var_const_float+= 1
                        self.constant_table[operand] = self.var_const_float
                    self.pila_operandos.append(self.constant_table[operand])
                    self.pila_tipos.append(tipo)
            else:
                #append de la direccion de memoria de la variable
                tipo = self.get_variable(operand)["type"]
                dir_memoria = self.get_variable(operand)['memory_address']
                self.pila_operandos.append(dir_memoria)
                self.pila_tipos.append(tipo)
        except:
            raise KeyError(f"Variable '{operand}' was not declared.")
    
    def add_factor(self):
        if self.pila_operadores:
            op = self.pila_operadores[-1]
            if op == '*' or op == '/':
                right_operand = self.pila_operandos.pop()
                left_operand = self.pila_operandos.pop()
                right_operand_tipo = self.pila_tipos.pop()
                left_operand_tipo = self.pila_tipos.pop()
                operator = self.pila_operadores.pop()

                res_tipo = self.semantic_cube.get_result_type(operator, left_operand_tipo, right_operand_tipo)

                if res_tipo == 'error':
                    raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")
                
                elif res_tipo == 'int':
                    res_address = self.var_temp_int
                    self.pila_operandos.append(res_address)
                    self.var_temp_int += 1
                    self.pila_tipos.append(res_tipo)
                    self.pila_cuadruplos.append([operator, left_operand, right_operand, res_address ])

                elif res_tipo == 'float':
                    res_address = self.var_temp_float
                    self.pila_operandos.append(res_address)
                    self.var_temp_float+= 1
                    self.pila_tipos.append(res_tipo)
                    self.pila_cuadruplos.append([operator, left_operand, right_operand, res_address ])

    def add_termino(self):
            if self.pila_operadores:
                op = self.pila_operadores[-1]
                if op == '+' or op == '-':
                    right_operand = self.pila_operandos.pop()
                    left_operand = self.pila_operandos.pop()
                    right_operand_tipo = self.pila_tipos.pop()
                    left_operand_tipo = self.pila_tipos.pop()
                    operator = self.pila_operadores.pop()

                    res_tipo = self.semantic_cube.get_result_type(operator, left_operand_tipo, right_operand_tipo)

                    if res_tipo == 'error':
                        raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")
                    
                    elif res_tipo == 'int':
                        res_address = self.var_temp_int
                        self.pila_operandos.append(res_address)
                        self.var_temp_int += 1
                        self.pila_tipos.append(res_tipo)
                        self.pila_cuadruplos.append([operator, left_operand, right_operand, res_address ])

                    elif res_tipo == 'float':
                        res_address = self.var_temp_float
                        self.pila_operandos.append(res_address)
                        self.var_temp_float+= 1
                        self.pila_tipos.append(res_tipo)
                        self.pila_cuadruplos.append([operator, left_operand, right_operand, res_address ])
    def add_expresion(self):
        if self.pila_operadores:
            op = self.pila_operadores[-1]
            if op == '>' or op == '<' or op == '!=':
                    right_operand = self.pila_operandos.pop()
                    left_operand = self.pila_operandos.pop()
                    right_operand_tipo = self.pila_tipos.pop()
                    left_operand_tipo = self.pila_tipos.pop()
                    operator = self.pila_operadores.pop()

                    res_tipo = self.semantic_cube.get_result_type(operator, left_operand_tipo, right_operand_tipo)

                    if res_tipo == 'bool':
                        self.var_temp_bool += 1
                        res_address = self.var_temp_bool
                        self.pila_operandos.append(res_address)
                        self.pila_tipos.append(res_tipo)
                        self.pila_cuadruplos.append([operator, left_operand, right_operand, res_address ])
                    
                    # elif res_tipo == 'int':
                    #     res_address = self.var_temp_int
                    #     self.pila_operandos.append(res_address)
                    #     self.var_temp_int += 1
                    #     self.pila_tipos.append(res_tipo)
                    #     self.pila_cuadruplos.append([operator, left_operand, right_operand, res_address ])

                    # elif res_tipo == 'float':
                    #     res_address = self.var_temp_float
                    #     self.pila_operandos.append(res_address)
                    #     self.var_temp_float+= 1
                    #     self.pila_tipos.append(res_tipo)
                    #     self.pila_cuadruplos.append([operator, left_operand, right_operand, res_address ])
                    else:
                        raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")


    def add_assing(self):
        if self.pila_operadores:
            op = self.pila_operadores[-1]
            if op == '=':
                right_operand = self.pila_operandos.pop()
                left_operand = self.pila_operandos.pop()
                right_operand_tipo = self.pila_tipos.pop()
                left_operand_tipo = self.pila_tipos.pop()
                operator = self.pila_operadores.pop()

                res_tipo = self.semantic_cube.get_result_type(operator, left_operand_tipo, right_operand_tipo)

                if res_tipo != 'error':
                    self.pila_cuadruplos.append([operator, right_operand, None, left_operand ])
                

                else:
                    raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")
                
    def add_print(self, string = []):
        if string == []:
            right_operand = self.pila_operandos.pop()
            right_operand_tipo = self.pila_tipos.pop()

            self.pila_cuadruplos.append(['print', right_operand, None, None ])
        else:
            self.pila_cuadruplos.append(['print', string, None, None ])
                
    
    def add_gotof(self):
        condition = self.pila_operandos.pop()
        condition_type = self.pila_tipos.pop()
        
        if condition_type != 'bool':
            raise ValueError("Condition for if statement must be a boolean")
        
        self.pila_cuadruplos.append(['GOTOF', condition, None, None])
        self.pila_saltos.append(len(self.pila_cuadruplos) - 1)

    def add_goto(self):
        self.pila_cuadruplos.append(['GOTO', None, None, None])
        false_jump = self.pila_saltos.pop()

        self.pila_saltos.append(len(self.pila_cuadruplos) - 1)
        self.pila_cuadruplos[false_jump][-1] = len(self.pila_cuadruplos)

    def add_gotoFfill(self):
        false_jump = self.pila_saltos.pop()
        self.pila_cuadruplos[false_jump][-1] = len(self.pila_cuadruplos)

    # def patch_else(self):
    #     end_jump = self.pila_saltos.pop()
    #     self.pila_cuadruplos[end_jump][-1] = len(self.pila_cuadruplos)

    # def patch_if(self):
    #     false_jump = self.pila_saltos.pop()
    #     self.pila_cuadruplos[false_jump][-1] = len(self.pila_cuadruplos)

    def start_while(self):
        # Guarda la posición del inicio del ciclo
        self.pila_saltos.append(len(self.pila_cuadruplos))

    def add_gotov_while(self):
        condition = self.pila_operandos.pop()
        condition_type = self.pila_tipos.pop()
        
        if condition_type != 'bool':
            raise ValueError("Condition for while statement must be a boolean")
        
        # Agrega el cuádruplo GOTOF para evaluar la condición del while
        direccion_salto = self.pila_saltos.pop()
        self.pila_cuadruplos.append(['GOTOV', condition, None, direccion_salto])
        