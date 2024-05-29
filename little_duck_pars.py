import ply.yacc as yacc
from symbol_table import VariableTable
from little_duck_lex import tokens
import pickle

variable_table = VariableTable()

# Definir precedencia y asociatividad de los operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LT', 'GT', 'NE')
)

# Reglas gramaticales
def p_program(p):
    'program : PROGRAM ID SEMICOLON a_vars a_funcs MAIN body END'
    pass

def p_a_vars(p):
    '''a_vars : empty
              | vars'''
    # Manejar la declaración de variables
    lista_variables = p[1]
    for var in lista_variables:
        nombre, tipo = var.split(':')
        variable_table.add_variable(nombre, tipo)

def p_a_funcs(p):
    '''a_funcs : empty
               | funcs b_funcs'''
    # Manejar la declaración de funciones
    pass

def p_b_funcs(p):
    '''b_funcs : funcs b_funcs
                | funcs'''
    # Manejar múltiples funciones
    pass

# Módulo de VARS
def p_vars(p):
    '''vars : VAR ID COLON type SEMICOLON list_vars'''
    # Manejar la declaración de variables
    list_vars = p[6]
    p[0] = (f'{p[2]}:{p[4]}', *list_vars.split(','))

def p_list_vars(p):
    '''list_vars : empty
                 | ID COLON type SEMICOLON list_vars'''
    # Manejar la lista de variables
    if len(p) > 2:
        if p[5] != None:
            p[0] = f'{p[1]}:{p[3]},{p[5]}'
        else:
            p[0] = f'{p[1]}:{p[3]}'

def p_type(p):
    '''type : INT
            | FLOAT'''
    # Manejar los tipos de datos
    p[0] = p[1]

def p_body(p):
    'body : LBRACE list_statements RBRACE'
    # Manejar el cuerpo de funciones o del programa principal
    pass

def p_list_statements(p):
    '''list_statements : statement body_rep
                       | empty
                       | statement'''
    # Manejar la lista de declaraciones
    pass

def p_statement(p):
    '''statement : assign
                 | condition
                 | cycle
                 | f_call
                 | print_stmt'''
    # Manejar una declaración (asignación, condición, ciclo, llamada a función, impresión)
    pass

def p_body_rep(p):
    '''body_rep : statement body_rep
                       | statement'''
    # Manejar declaraciones adicionales en el cuerpo
    pass

def p_print_stmt(p):
    'print_stmt : PRINT LPAREN list_expresion RPAREN SEMICOLON'
    # Manejar la declaración de impresión
    pass

def p_list_expresion(p):
    '''list_expresion : expresion addPrint
                    | expresion addPrint COMMA list_expresion
                    | CTE_STRING addPrintString
                    | CTE_STRING addPrintString COMMA list_expresion'''
    # Manejar la lista de expresiones en una impresión
    pass

def p_addPrint(p):
    '''addPrint : '''
    # Añadir la operación de impresión
    variable_table.add_print()

def p_addPrintString(p):
    '''addPrintString : '''
    # Añadir la operación de impresión de una cadena
    variable_table.add_print(string=p[-1])

def p_assign(p):
    'assign : ID add_operand EQUALS add_operador expresion SEMICOLON'
    # Manejar la asignación de valores a variables
    variable_table.add_assing()
    pass

def p_add_operand(p):
    '''add_operand : '''
    # Añadir un operando a la pila
    variable_table.add_operand(p[-1])

def p_add_operador(p):
    '''add_operador : '''
    # Añadir un operador a la pila
    variable_table.append_pila_operador(p[-1])

def p_cycle(p):
    'cycle : DO ciclo_start body WHILE LPAREN expresion RPAREN gotov SEMICOLON'
    # Manejar el ciclo do-while
    pass

def p_ciclo_start(p):
    '''ciclo_start : '''
    # Marcar el inicio del ciclo
    variable_table.start_while()

def p_gotov(p):
    '''gotov : '''
    # Añadir la instrucción de salto condicional para el ciclo
    variable_table.add_gotov_while()

def p_condition(p):
    'condition : IF LPAREN expresion RPAREN gotof body else_part SEMICOLON'
    # Manejar la declaración if-else
    variable_table.add_gotoFfill()

def p_gotof(p):
    '''gotof : '''
    # Añadir la instrucción de salto condicional para if
    variable_table.add_gotof()

def p_else_part(p):
    '''else_part : ELSE goto body
                 | empty'''
    # Manejar la parte else de una declaración if-else
    pass

def p_goto(p):
    '''goto : '''
    # Añadir una instrucción de salto incondicional
    variable_table.add_goto()

def p_expresion(p):
    '''expresion : exp comparar_exp exp
                | exp'''
    # Manejar la evaluación de una expresión
    variable_table.add_expresion()

def p_comparar_exp(p):
    '''comparar_exp : LT
                    | GT
                    | NE'''
    # Añadir un operador de comparación a la pila
    variable_table.append_pila_operador(p[1])

def p_exp(p):
    '''exp : termino add_termino 
           | termino add_termino next_termino'''
    # Manejar la evaluación de términos en una expresión
    pass

def p_add_termino(p):
    '''add_termino : '''
    # Añadir un término a la pila
    variable_table.add_termino()

def p_next_termino(p):
    '''next_termino : sum_rest exp '''
    # Manejar la evaluación de términos adicionales
    pass

def p_sum_rest(p):
    '''sum_rest : PLUS
                | MINUS'''
    # Añadir un operador de suma o resta a la pila
    variable_table.append_pila_operador(p[1])
    pass

def p_termino(p):
    '''termino : factor add_factor next_factor
               | factor add_factor'''
    # Manejar la evaluación de un término
    pass

def p_next_factor(p):
    '''next_factor : mult_div termino'''
    # Manejar la evaluación de factores adicionales
    pass

def p_mult_div(p):
    '''mult_div : TIMES
                | DIVIDE'''
    # Añadir un operador de multiplicación o división a la pila
    variable_table.append_pila_operador(p[1])
    pass

def p_factor(p):
    '''factor : LPAREN expresion RPAREN
              | id_cte'''
    # Manejar la evaluación de un factor
    pass

def p_add_factor(p):
    '''add_factor : '''
    # Añadir un factor a la pila
    variable_table.add_factor()

def p_id_cte(p):
    '''id_cte : ID push_var
              | cte push_const'''
    # Manejar identificadores y constantes
    pass

def p_push_const(p):
    '''push_const : '''
    # Añadir una constante a la pila
    variable_table.add_operand(p[-1], True)

def p_push_var(p):
    '''push_var : '''
    # Añadir una variable a la pila
    variable_table.add_operand(p[-1])

def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''
    # Manejar constantes enteras y de punto flotante
    p[0] = p[1]

def p_funcs(p):
    'funcs : VOID ID LPAREN list_params RPAREN LBRACE var_no_var body RBRACE SEMICOLON'
    # Manejar la declaración de funciones
    pass

def p_list_params(p):
    '''list_params : empty
                   | ID COLON type more_params'''
    # Manejar la lista de parámetros de una función
    pass

def p_more_params(p):
    '''more_params : empty
                   | COMMA ID COLON type more_params'''
    # Manejar parámetros adicionales en una función
    pass

def p_var_no_var(p):
    '''var_no_var : empty
                  | vars'''
    # Manejar variables locales en una función
    pass

def p_f_call(p):
    'f_call : ID LPAREN RPAREN SEMICOLON'
    # Manejar la llamada a una función
    pass

def p_empty(p):
    'empty :'
    # Regla para manejar producción vacía
    pass

def p_error(p):
    # Manejo de errores de sintaxis
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# Construir el parser
parser = yacc.yacc()

# Leer el código desde un archivo de texto
with open('file.txt', 'r') as file:
    data = file.read()

# Probar el parser
parser.parse(data, tracking=True)
print(variable_table.pila_operandos)
print(variable_table.pila_operadores)
print(variable_table.pila_tipos)
print(variable_table.pila_saltos)
print(variable_table.pila_cuadruplos)

# Guardar variable_table.pila_cuadruplos en un archivo pkl
with open('/home/ricardo/Desktop/Little_Duck/pila_cuadruplos.pkl', 'wb') as file:
    pickle.dump(variable_table.pila_cuadruplos, file)

# Guardar variable_table.constant_table en un archivo pkl
def invert_dict(d):
    return {v: k for k, v in d.items()}

constant_table = invert_dict(variable_table.constant_table)

# Guardar el diccionario en un archivo pickle
with open('constant_table.pkl', 'wb') as pickle_file:
    pickle.dump(constant_table, pickle_file)
