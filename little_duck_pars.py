from ply import yacc
from little_duck_lex import tokens

def p_programa(p):
    'Programa : PROGRAM ID SEMICOLON VARS FUNCS MAIN Body END SEMICOLON'
    pass

def p_vars(p):
    '''VARS : VAR ListaVars COLON TYPE SEMICOLON
            | epsilon'''
    pass

def p_lista_vars(p):
    '''ListaVars : ID COMMA ListaVars
                 | ID'''
    pass

def p_type(p):
    '''TYPE : INT
            | FLOAT
            | STRING'''
    pass

def p_funcs(p):
    '''FUNCS : Funcion FUNCS
             | epsilon'''
    pass

def p_funcion(p):
    'Funcion : TipoFunc ID LPAREN Parametros RPAREN COLON Body'
    pass

def p_tipofunc(p):
    '''TipoFunc : VOID
                | TYPE'''
    pass

def p_parametros(p):
    '''Parametros : ID COMMA Parametros
                  | ID COLON TYPE
                  | epsilon'''
    pass

def p_body(p):
    'Body : LBRACE Statements RBRACE'
    pass

def p_statements(p):
    '''Statements : Statement Statements
                  | epsilon'''
    pass

def p_statement(p):
    '''Statement : ASSIGNMENT
                 | CONDITION
                 | CYCLE
                 | F_Call
                 | Print'''
    pass

def p_assignment(p):
    'ASSIGNMENT : ID ASSIGN Expresion SEMICOLON'
    pass

def p_condition(p):
    '''CONDITION : IF LPAREN Expresion RPAREN Body
                 | IF LPAREN Expresion RPAREN Body ELSE Body'''
    pass

def p_cycle(p):
    '''CYCLE : WHILE LPAREN Expresion RPAREN Body SEMICOLON
             | DO Body WHILE LPAREN Expresion RPAREN SEMICOLON'''
    pass

def p_f_call(p):
    'F_Call : ID LPAREN Expresiones RPAREN SEMICOLON'
    pass

def p_expresiones(p):
    '''Expresiones : Expresion COMMA Expresiones
                   | Expresion
                   | epsilon'''
    pass

def p_print(p):
    'Print : PRINT LPAREN Expresiones RPAREN SEMICOLON'
    pass

def p_expresion(p):
    '''Expresion : Expresion NOTEQUALS Exp
                 | Expresion LESS Exp
                 | Expresion GREATER Exp
                 | Exp'''
    pass

def p_exp(p):
    '''Exp : Exp PLUS Term
           | Exp MINUS Term
           | Term'''
    pass

def p_term(p):
    '''Term : Term TIMES Factor
            | Term DIVIDE Factor
            | Factor'''
    pass

def p_factor(p):
    '''Factor : LPAREN Expresion RPAREN
              | PLUS Subfactor
              | MINUS Subfactor
              | Subfactor'''
    pass

def p_subfactor(p):
    '''Subfactor : CTE
                 | ID'''
    pass

def p_cte(p):
    '''CTE : CTE_FLOAT
           | CTE_INT
           | CTE_STRING'''
    pass

def p_epsilon(p):
    'epsilon :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(debug=True)

# Prueba del parser
if __name__ == '__main__':
    data = '''
    program ejemplo;
    var x : int;
    main {
        print("Hola Mundo");
    }
    end;
    '''
    result = parser.parse(data)
    print(result)
