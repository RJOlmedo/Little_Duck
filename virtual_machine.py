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
        # Initialize global int memory
        for address in range(self.var_int, self.var_float):
            self.memory[address] = 0

        # Initialize global float memory
        for address in range(self.var_float, self.var_temp_int):
            self.memory[address] = 0.0

        # Initialize temp int memory
        for address in range(self.var_temp_int, self.var_temp_float):
            self.memory[address] = 0

        # Initialize temp float memory
        for address in range(self.var_temp_float, self.var_temp_bool):
            self.memory[address] = 0.0

        # Initialize temp bool memory
        for address in range(self.var_temp_bool, self.var_const_int):
            self.memory[address] = False

        # Initialize const int memory
        for address in range(self.var_const_int, self.var_const_float):
            self.memory[address] = 0

        # Initialize const float memory
        for address in range(self.var_const_float, self.var_const_string):
            self.memory[address] = 0.0

        # Initialize const string memory
        for address in range(self.var_const_string, self.var_const_string + 50):
            self.memory[address] = ""


    def load_quadruples(self, quadruples):
        self.quadruples = quadruples

    def execute(self):
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
        self.memory[address] = value

    def get_memory(self, address):
        return self.memory.get(address, None)
    

# Loading the dictionary from the pickle file
with open('constant_table.pkl', 'rb') as pickle_file:
    constant_table = pickle.load(pickle_file)

# Loading the dictionary from the pickle file
with open('pila_cuadruplos.pkl', 'rb') as pickle_file:
    cuadruplos = pickle.load(pickle_file)


# Crear la máquina virtual e inicializar la memoria
vm = VirtualMachine(constant_table)


vm.initialize_memory()

for address, value in constant_table.items():
    vm.set_memory(address, value)

# Cargar y ejecutar los cuádruplos
# vm.load_quadruples_from_file('ovejota.txt')
vm.load_quadruples(cuadruplos)

vm.execute()