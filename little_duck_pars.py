import ply.yacc as yacc
from little_duck_lex import tokens

# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('nonassoc', 'LT', 'GT', 'EQ', 'NE'),
)

# Gramática y reglas de producción
def p_program(p):
    'program : PROGRAM ID SEMI vars funcs main END'
    p[0] = ('program', p[2], p[4], p[5], p[6])

def p_vars(p):
    '''vars : VAR var_declaration vars
            | empty'''
    if len(p) == 4:
        p[0] = ('vars', p[2], p[3])
    else:
        p[0] = None

def p_var_declaration(p):
    '''var_declaration : ID COLON type SEMI
                       | ID COLON type COMMA var_declaration'''
    if len(p) == 5:
        p[0] = ('var', p[1], p[3])
    else:
        p[0] = ('var', p[1], p[3], p[5])

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING'''
    p[0] = p[1]

def p_funcs(p):
    '''funcs : VOID ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE funcs
             | empty'''
    if len(p) == 10:
        p[0] = ('funcs', p[2], p[4], p[7], p[9])
    else:
        p[0] = None

def p_parameter_list(p):
    '''parameter_list : parameter COMMA parameter_list
                      | parameter
                      | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_parameter(p):
    'parameter : ID COLON type'
    p[0] = ('param', p[1], p[3])

def p_main(p):
    'main : MAIN LBRACE statement_list RBRACE'
    p[0] = ('main', p[3])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : assign
                 | condition
                 | cycle
                 | print_statement
                 | f_call'''
    p[0] = p[1]

def p_assign(p):
    'assign : ID ASSIGN expression SEMI'
    p[0] = ('assign', p[1], p[3])

def p_condition(p):
    'condition : IF LPAREN expression RPAREN LBRACE statement_list RBRACE else_part'
    p[0] = ('condition', p[3], p[6], p[8])

def p_else_part(p):
    '''else_part : ELSE LBRACE statement_list RBRACE
                 | empty'''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = None

def p_cycle(p):
    '''cycle : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE
             | DO LBRACE statement_list RBRACE WHILE LPAREN expression RPAREN SEMI'''
    if p[1] == 'while':
        p[0] = ('while', p[3], p[6])
    else:
        p[0] = ('do_while', p[3], p[7])

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMI'
    p[0] = ('print', p[3])

def p_f_call(p):
    '''f_call : ID LPAREN arg_list RPAREN SEMI
              | ID LPAREN RPAREN SEMI'''
    if len(p) == 6:
        p[0] = ('f_call', p[1], p[3])
    else:
        p[0] = ('f_call', p[1], [])

def p_arg_list(p):
    '''arg_list : expression COMMA arg_list
                | expression'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIV expression
                  | term'''
    if len(p) == 4:
        p[0] = ('binary_op', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''term : factor
            | factor LT factor
            | factor GT factor
            | factor EQ factor
            | factor NE factor'''
    if len(p) == 4:
        p[0] = ('comparison_op', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | ID
              | CTE_INT
              | CTE_FLOAT
              | CTE_STRING'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en token {p.type}, línea {p.lineno}, posición {p.lexpos}")
    else:
        print("Error de sintaxis en EOF")

# Construir el parser
parser = yacc.yacc()

# Prueba del parser
if __name__ == '__main__':
    data = '''
    program ejemplo;
    var x : int, y : float;
    main {
        print("Hola Mundo");
        if (x < 10) {
            print("Hola Mundo");
        }
    }
    end
    '''
    result = parser.parse(data)
    print(result)
