import pickle

class VirtualMachine:
    def __init__(self, const_table):
        self.const_table = const_table
        self.memory = {}
        self.instruction_pointer = 0
        self.var_int = 0
        self.var_float = 100

        self.var_temp_int = 200
        self.var_temp_float = 300
        self.var_temp_bool = 400

        self.var_const_int = 500
        self.var_const_float = 600
        self.var_const_string = 700

    def initialize_memory(self):
        # Inicializar memoria para variables globales enteras
        for address in range(self.var_int, self.var_float):
            self.memory[address] = 0

        # Inicializar memoria para variables globales de punto flotante
        for address in range(self.var_float, self.var_temp_int):
            self.memory[address] = 0.0

        # Inicializar memoria para variables temporales enteras
        for address in range(self.var_temp_int, self.var_temp_float):
            self.memory[address] = 0

        # Inicializar memoria para variables temporales de punto flotante
        for address in range(self.var_temp_float, self.var_temp_bool):
            self.memory[address] = 0.0

        # Inicializar memoria para variables temporales booleanas
        for address in range(self.var_temp_bool, self.var_const_int):
            self.memory[address] = False

        # Inicializar memoria para constantes enteras
        for address in range(self.var_const_int, self.var_const_float):
            self.memory[address] = 0

        # Inicializar memoria para constantes de punto flotante
        for address in range(self.var_const_float, self.var_const_string):
            self.memory[address] = 0.0

        # Inicializar memoria para constantes de cadena
        for address in range(self.var_const_string, self.var_const_string + 50):
            self.memory[address] = ""

    def load_quadruples(self, quadruples):
        # Cargar cuádruplos en la máquina virtual
        self.quadruples = quadruples

    def execute(self):
        # Ejecutar los cuádruplos
        while self.instruction_pointer < len(self.quadruples):
            quad = self.quadruples[self.instruction_pointer]
            op = quad[0]
            left = quad[1]
            right = quad[2]
            result = quad[3]

            if op == '+':
                self.memory[result] = self.memory[left] + self.memory[right]
            elif op == '-':
                self.memory[result] = self.memory[left] - self.memory[right]
            elif op == '*':
                self.memory[result] = self.memory[left] * self.memory[right]
            elif op == '/':
                self.memory[result] = self.memory[left] / self.memory[right]
            elif op == '=':
                self.memory[result] = self.memory[left]
            elif op == '!=':
                self.memory[result] = self.memory[left] != self.memory[right]
            elif op == '>':
                self.memory[result] = self.memory[left] > self.memory[right]
            elif op == '<':
                self.memory[result] = self.memory[left] < self.memory[right]
            elif op == 'GOTO':
                self.instruction_pointer = result
                continue
            elif op == 'GOTOV':
                if self.memory[left]:
                    self.instruction_pointer = result
                    continue
            elif op == 'GOTOF':
                if not self.memory[left]:
                    self.instruction_pointer = result
                    continue
            elif op == 'print':
                if type(left) == str:
                    print(left)
                else:
                    print(self.memory[left])
            else:
                raise Exception(f"Unknown operator: {op}")

            self.instruction_pointer += 1

    def set_memory(self, address, value):
        # Establecer un valor en una dirección de memoria específica
        self.memory[address] = value

    def get_memory(self, address):
        # Obtener el valor de una dirección de memoria específica
        return self.memory.get(address, None)

# Cargar el diccionario desde el archivo pickle
with open('constant_table.pkl', 'rb') as pickle_file:
    constant_table = pickle.load(pickle_file)

# Cargar el diccionario desde el archivo pickle
with open('pila_cuadruplos.pkl', 'rb') as pickle_file:
    cuadruplos = pickle.load(pickle_file)

# Crear la máquina virtual e inicializar la memoria
vm = VirtualMachine(constant_table)

vm.initialize_memory()

# Configurar la memoria con las constantes cargadas
for address, value in constant_table.items():
    vm.set_memory(address, value)

# Cargar y ejecutar los cuádruplos
vm.load_quadruples(cuadruplos)

vm.execute()
