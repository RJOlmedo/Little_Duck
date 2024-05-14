from ply import yacc
from little_duck_lex import tokens

class ASTNode:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"ASTNode(type={self.type}, children={self.children}, value={self.value})"

def p_programa(p):
    'Programa : PROGRAM ID SEMICOLON VARS FUNCS MAIN Body END SEMICOLON'
    p[0] = ASTNode('Programa', [p[4], p[5], p[6], p[7]])

def p_vars(p):
    '''VARS : VAR ListaVars COLON TYPE SEMICOLON
            | epsilon'''
    if len(p) == 6:
        p[0] = ASTNode('VARS', [p[2], p[4]])
    else:
        p[0] = ASTNode('VARS', [], 'epsilon')

def p_lista_vars(p):
    '''ListaVars : ID COMMA ListaVars
                 | ID'''
    if len(p) == 4:
        p[0] = ASTNode('ListaVars', [ASTNode('ID', value=p[1]), p[3]])
    else:
        p[0] = ASTNode('ListaVars', [ASTNode('ID', value=p[1])])

def p_type(p):
    '''TYPE : INT
            | FLOAT
            | STRING'''
    p[0] = ASTNode('TYPE', value=p[1])

def p_funcs(p):
    '''FUNCS : Funcion FUNCS
             | epsilon'''
    if len(p) == 3:
        p[0] = ASTNode('FUNCS', [p[1], p[2]])
    else:
        p[0] = ASTNode('FUNCS', [], 'epsilon')

def p_funcion(p):
    'Funcion : TipoFunc ID LPAREN Parametros RPAREN COLON Body'
    p[0] = ASTNode('Funcion', [p[1], ASTNode('ID', value=p[2]), p[4], p[7]])

def p_tipofunc(p):
    '''TipoFunc : VOID
                | TYPE'''
    p[0] = ASTNode('TipoFunc', value=p[1])

def p_parametros(p):
    '''Parametros : ID COMMA Parametros
                  | ID COLON TYPE
                  | epsilon'''
    if len(p) == 4:
        p[0] = ASTNode('Parametros', [ASTNode('ID', value=p[1]), p[3]])
    elif len(p) == 2:
        p[0] = ASTNode('Parametros', [], 'epsilon')
    else:
        p[0] = ASTNode('Parametros', [ASTNode('ID', value=p[1]), p[3]])

def p_body(p):
    'Body : LBRACE Statements RBRACE'
    p[0] = ASTNode('Body', [p[2]])

def p_statements(p):
    '''Statements : Statement Statements
                  | epsilon'''
    if len(p) == 3:
        p[0] = ASTNode('Statements', [p[1], p[2]])
    else:
        p[0] = ASTNode('Statements', [], 'epsilon')

def p_statement(p):
    '''Statement : ASSIGNMENT
                 | CONDITION
                 | CYCLE
                 | F_Call
                 | Print'''
    p[0] = p[1]

def p_assignment(p):
    'ASSIGNMENT : ID ASSIGN Expresion SEMICOLON'
    p[0] = ASTNode('ASSIGNMENT', [ASTNode('ID', value=p[1]), p[3]])

def p_condition(p):
    '''CONDITION : IF LPAREN Expresion RPAREN Body
                 | IF LPAREN Expresion RPAREN Body ELSE Body'''
    if len(p) == 6:
        p[0] = ASTNode('CONDITION', [p[3], p[5]])
    else:
        p[0] = ASTNode('CONDITION', [p[3], p[5], p[7]])

def p_cycle(p):
    '''CYCLE : WHILE LPAREN Expresion RPAREN Body SEMICOLON
             | DO Body WHILE LPAREN Expresion RPAREN SEMICOLON'''
    if p[1] == 'while':
        p[0] = ASTNode('CYCLE', [p[3], p[5]])
    else:
        p[0] = ASTNode('CYCLE', [p[2], p[5]])

def p_f_call(p):
    'F_Call : ID LPAREN Expresiones RPAREN SEMICOLON'
    p[0] = ASTNode('F_Call', [ASTNode('ID', value=p[1]), p[3]])

def p_expresiones(p):
    '''Expresiones : Expresion COMMA Expresiones
                   | Expresion
                   | epsilon'''
    if len(p) == 4:
        p[0] = ASTNode('Expresiones', [p[1], p[3]])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ASTNode('Expresiones', [], 'epsilon')

def p_print(p):
    'Print : PRINT LPAREN Expresiones RPAREN SEMICOLON'
    p[0] = ASTNode('Print', [p[3]])

def p_expresion(p):
    '''Expresion : Expresion NOTEQUALS Exp
                 | Expresion LESS Exp
                 | Expresion GREATER Exp
                 | Exp'''
    if len(p) == 4:
        p[0] = ASTNode('Expresion', [p[1], ASTNode('Operator', value=p[2]), p[3]])
    else:
        p[0] = p[1]

def p_exp(p):
    '''Exp : Exp PLUS Term
           | Exp MINUS Term
           | Term'''
    if len(p) == 4:
        p[0] = ASTNode('Exp', [p[1], ASTNode('Operator', value=p[2]), p[3]])
    else:
        p[0] = p[1]

def p_term(p):
    '''Term : Term TIMES Factor
            | Term DIVIDE Factor
            | Factor'''
    if len(p) == 4:
        p[0] = ASTNode('Term', [p[1], ASTNode('Operator', value=p[2]), p[3]])
    else:
        p[0] = p[1]

def p_factor(p):
    '''Factor : LPAREN Expresion RPAREN
              | PLUS Subfactor
              | MINUS Subfactor
              | Subfactor'''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = ASTNode('Factor', [ASTNode('Unary', value=p[1]), p[2]])
    else:
        p[0] = p[1]

def p_subfactor(p):
    '''Subfactor : CTE
                 | ID'''
    p[0] = p[1]

def p_cte(p):
    '''CTE : CTE_FLOAT
           | CTE_INT
           | CTE_STRING'''
    p[0] = ASTNode('CTE', value=p[1])

def p_epsilon(p):
    'epsilon :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(debug=True)