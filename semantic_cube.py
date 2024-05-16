# Definimos los tipos
INT = 'int'
FLOAT = 'float'
STRING = 'string'
BOOL = 'bool'

# Operadores
ADD = '+'
SUB = '-'
MUL = '*'
DIV = '/'
LT = '<'
GT = '>'
EQ = '=='
NE = '!='

# Cubo Semántico: dict de dict de dicts, donde las llaves son (tipo1, operador, tipo2) y el valor es el tipo resultante o None si no es válido
semantic_cube = {
    INT: {
        ADD: {INT: INT, FLOAT: FLOAT, STRING: None},
        SUB: {INT: INT, FLOAT: FLOAT, STRING: None},
        MUL: {INT: INT, FLOAT: FLOAT, STRING: None},
        DIV: {INT: FLOAT, FLOAT: FLOAT, STRING: None},
        LT: {INT: BOOL, FLOAT: BOOL, STRING: None},
        GT: {INT: BOOL, FLOAT: BOOL, STRING: None},
        EQ: {INT: BOOL, FLOAT: BOOL, STRING: None},
        NE: {INT: BOOL, FLOAT: BOOL, STRING: None},
    },
    FLOAT: {
        ADD: {INT: FLOAT, FLOAT: FLOAT, STRING: None},
        SUB: {INT: FLOAT, FLOAT: FLOAT, STRING: None},
        MUL: {INT: FLOAT, FLOAT: FLOAT, STRING: None},
        DIV: {INT: FLOAT, FLOAT: FLOAT, STRING: None},
        LT: {INT: BOOL, FLOAT: BOOL, STRING: None},
        GT: {INT: BOOL, FLOAT: BOOL, STRING: None},
        EQ: {INT: BOOL, FLOAT: BOOL, STRING: None},
        NE: {INT: BOOL, FLOAT: BOOL, STRING: None},
    },
    STRING: {
        ADD: {INT: None, FLOAT: None, STRING: STRING},
        SUB: {INT: None, FLOAT: None, STRING: None},
        MUL: {INT: None, FLOAT: None, STRING: None},
        DIV: {INT: None, FLOAT: None, STRING: None},
        LT: {INT: None, FLOAT: None, STRING: BOOL},
        GT: {INT: None, FLOAT: None, STRING: BOOL},
        EQ: {INT: None, FLOAT: None, STRING: BOOL},
        NE: {INT: None, FLOAT: None, STRING: BOOL},
    },
}

# Función para obtener el tipo resultante de una operación
def get_result_type(left_type, operator, right_type):
    return semantic_cube.get(left_type, {}).get(operator, {}).get(right_type, None)
