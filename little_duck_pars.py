import ply.yacc as yacc
from symbol_table import VariableTable
from little_duck_lex import tokens

variable_table = VariableTable()

# Define precedence and associativity of operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LT', 'GT', 'NE')
)

# Grammar rules
def p_program(p):
    'program : PROGRAM ID SEMICOLON a_vars a_funcs MAIN body END'
    pass

def p_a_vars(p):
    '''a_vars : empty
              | vars'''
    lista_variables = p[1]

    for var in lista_variables:
        nombre, tipo = var.split(':')
        variable_table.add_variable(nombre, tipo)

def p_a_funcs(p):
    '''a_funcs : empty
               | funcs b_funcs'''
    pass

def p_b_funcs(p):
    '''b_funcs : funcs b_funcs
                | funcs'''
    pass

#VARS MODULE 
def p_vars(p):
    '''vars : VAR ID COLON type SEMICOLON list_vars
    '''
    list_vars = p[6]
    p[0] = (f'{p[2]}:{p[4]}',*list_vars.split(','))

def p_list_vars(p):
    '''list_vars : empty
                 | ID COLON type SEMICOLON list_vars
    '''
    if len(p) > 2:
        if p[5] != None:
            p[0]=f'{p[1]}:{p[3]},{p[5]}'
        else:
             p[0]=f'{p[1]}:{p[3]}'

# def p_list_vars(p):
#     '''list_vars : ID  list_id COLON type SEMICOLON list_vars
#           | ID  list_id COLON type SEMICOLON
#     '''
#     variables_list = [p[1]]
#     print(variables_list)
#     if p[2] != None:
#         variables_list.extend(p[2].split(','))
    
#     for element in variables_list:
#         variable_table.add_variable(element,p[4])

#     if len(p) == 7:
#         if p[2] != None:
#             p[0]=[p[1], p[2], *p[6]]
#         else:
#             p[0]=[p[1], *p[6]]

#     else:
#         if p[2] != None:
#             vars_str = p[1]+','+p[2]
#             # Dividir el string por comas para obtener cada par nombre:tipo
#             pares = vars_str.split(',')
#             # Extraer solo los nombres (parte antes de los dos puntos) y guardarlos en una lista
#             vars_names = [par.split(':')[0] for par in pares]
#             p[0]=vars_names
#         else:
#             p[0]=[p[1]]

# def p_list_id(p):
#     '''list_id : COMMA ID list_id
#           | empty
#     '''

#     if len(p) == 4:
#         if p[3] != None:
#             p[0] = f'{p[2]},{p[3]}'
#         else:
#             p[0] = f'{p[2]}'

def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]

def p_body(p):
    'body : LBRACE list_statements RBRACE'
    pass

def p_list_statements(p):
    '''list_statements : statement body_rep
                       | empty
                       | statement'''
    pass

def p_statement(p):
    '''statement : assign
                 | condition
                 | cycle
                 | f_call
                 | print_stmt'''
    pass

def p_body_rep(p):
    '''body_rep : statement body_rep
                       | statement'''
    pass

def p_print_stmt(p):
    'print_stmt : PRINT LPAREN list_expresion RPAREN SEMICOLON'
    pass

def p_list_expresion(p):
    '''list_expresion : expresion addPrint
                    | expresion addPrint COMMA list_expresion
                    | CTE_STRING addPrintString
                    | CTE_STRING addPrintString COMMA list_expresion'''
    pass

def p_addPrint(p):
    '''addPrint : '''
    variable_table.add_print()

def p_addPrintString(p):
    '''addPrintString : '''
    variable_table.add_print(string = p[-1])

def p_assign(p):
    'assign : ID add_operand EQUALS add_operador expresion SEMICOLON'
    variable_table.add_assing()
    pass

def p_add_operand(p):
    '''add_operand : '''
    variable_table.add_operand(p[-1])

def p_add_operador(p):
    '''add_operador : '''
    variable_table.append_pila_operador(p[-1])

def p_cycle(p):
    'cycle : DO body WHILE LPAREN expresion RPAREN SEMICOLON'
    pass

def p_condition(p):
    'condition : IF LPAREN expresion RPAREN gotof body else_part SEMICOLON'
    variable_table.add_gotoFfill()

def p_gotof(p):
    '''gotof : '''
    variable_table.add_gotof()

def p_else_part(p):
    '''else_part : ELSE goto body
                 | empty'''
    pass

def p_goto(p):
    '''goto : '''
    variable_table.add_goto()

def p_expresion(p):
    '''expresion : exp comparar_exp exp
                | exp'''
    variable_table.add_expresion()

def p_comparar_exp(p):
    '''comparar_exp : LT
                    | GT
                    | NE'''
    variable_table.append_pila_operador(p[1])

def p_exp(p):
    '''exp : termino add_termino 
            | termino add_termino next_termino'''
    pass

def p_add_termino(p):
    '''add_termino : '''
    variable_table.add_termino()

def p_next_termino(p):
    '''next_termino : sum_rest exp '''
    pass

def p_sum_rest(p):
    '''sum_rest : PLUS
                | MINUS'''
    variable_table.append_pila_operador(p[1])
    pass

def p_termino(p):
    '''termino : factor add_factor next_factor
                | factor add_factor'''
    pass

def p_next_factor(p):
    '''next_factor : mult_div termino'''
    pass

def p_mult_div(p):
    '''mult_div : TIMES
                | DIVIDE'''
    variable_table.append_pila_operador(p[1])
    pass

def p_factor(p):
    '''factor : LPAREN expresion RPAREN
                | id_cte'''
            #   | sum_rest id_cte
            #   | id_cte
    pass

def p_add_factor(p):
    '''add_factor : '''
    variable_table.add_factor()

def p_id_cte(p):
    '''id_cte : ID push_var
              | cte push_const'''
    pass

def p_push_const(p):
    '''push_const : '''
    variable_table.add_operand(p[-1],True)

def p_push_var(p):
    '''push_var : '''
    variable_table.add_operand(p[-1])

def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''
    p[0]=p[1]

def p_funcs(p):
    'funcs : VOID ID LPAREN list_params RPAREN LBRACE var_no_var body RBRACE SEMICOLON'
    pass

def p_list_params(p):
    '''list_params : empty
                   | ID COLON type more_params'''
    pass

def p_more_params(p):
    '''more_params : empty
                   | COMMA ID COLON type more_params'''
    pass

def p_var_no_var(p):
    '''var_no_var : empty
                  | vars'''
    pass

def p_f_call(p):
    'f_call : ID LPAREN RPAREN SEMICOLON'
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Read code from a text file
with open('file.txt', 'r') as file:
    data = file.read()

# Test the parser
parser.parse(data, tracking=True)
print(variable_table.pila_operandos)
print(variable_table.pila_operadores)
print(variable_table.pila_tipos)
print(variable_table.pila_saltos)
print(variable_table.pila_cuadruplos)
