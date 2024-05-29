import sys
import os
import pytest
from io import StringIO
from contextlib import redirect_stdout

# Añadir el directorio raíz del proyecto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from little_duck_pars import parser, variable_table

def parse_input(input_data):
    variable_table.__init__()  # Reiniciar la tabla de variables
    parser.parse(input_data)

def capture_output(function):
    f = StringIO()
    with redirect_stdout(f):
        function()
    return f.getvalue().strip()

def test_variable_declaration():
    data = '''    
    program PanchoProgram;
    var
      pancho_age: int;
      pancho_weight: float;
    main { }
    end'''
    
    parse_input(data)

    expected_operandos = "[]"
    expected_operadores = "[]"
    expected_tipos = "[]"
    expected_saltos = "[]"
    expected_cuadruplos = "[]"

    actual_operandos = capture_output(lambda: print(variable_table.pila_operandos))
    actual_operadores = capture_output(lambda: print(variable_table.pila_operadores))
    actual_tipos = capture_output(lambda: print(variable_table.pila_tipos))
    actual_saltos = capture_output(lambda: print(variable_table.pila_saltos))
    actual_cuadruplos = capture_output(lambda: print(variable_table.pila_cuadruplos))

    assert actual_operandos == expected_operandos
    assert actual_operadores == expected_operadores
    assert actual_tipos == expected_tipos
    assert actual_saltos == expected_saltos
    assert actual_cuadruplos == expected_cuadruplos


def test_arithmetic_operations():
    data = '''
    program PanchoProgram;
    var
      pancho_age: int;
      pancho_weight: float;
    main {
      pancho_age = 4 + 4;
      pancho_weight = pancho_age * 2.2;
    }
    end
    '''
    parse_input(data)

    expected_operandos = "[]"
    expected_operadores = "[]"
    expected_tipos = "[]"
    expected_saltos = "[]"
    expected_cuadruplos = "[['+', 501, 501, 200], ['=', 200, None, 0], ['*', 0, 601, 300], ['=', 300, None, 100]]"

    actual_operandos = capture_output(lambda: print(variable_table.pila_operandos))
    actual_operadores = capture_output(lambda: print(variable_table.pila_operadores))
    actual_tipos = capture_output(lambda: print(variable_table.pila_tipos))
    actual_saltos = capture_output(lambda: print(variable_table.pila_saltos))
    actual_cuadruplos = capture_output(lambda: print(variable_table.pila_cuadruplos))

    assert actual_operandos == expected_operandos
    assert actual_operadores == expected_operadores
    assert actual_tipos == expected_tipos
    assert actual_saltos == expected_saltos
    assert actual_cuadruplos == expected_cuadruplos

def test_if_statement():
    data = '''
    program MyProgram;
    var
        pancho_age: int;
        pancho_weight: float;

    main
    {
        pancho_age = 8;

        if (pancho_age > 10) {
            print("Viejo");
        }else{
            print("ar");
        };
    }

    end
    '''
    parse_input(data)

    expected_operandos = "[]"
    expected_operadores = "[]"
    expected_tipos = "[]"
    expected_saltos = "[]"
    expected_cuadruplos = "[['=', 501, None, 0], ['>', 0, 502, 401], ['GOTOF', 401, None, 5], ['print', 'Viejo', None, None], ['GOTO', None, None, 6], ['print', 'ar', None, None]]"

    actual_operandos = capture_output(lambda: print(variable_table.pila_operandos))
    actual_operadores = capture_output(lambda: print(variable_table.pila_operadores))
    actual_tipos = capture_output(lambda: print(variable_table.pila_tipos))
    actual_saltos = capture_output(lambda: print(variable_table.pila_saltos))
    actual_cuadruplos = capture_output(lambda: print(variable_table.pila_cuadruplos))

    assert actual_operandos == expected_operandos
    assert actual_operadores == expected_operadores
    assert actual_tipos == expected_tipos
    assert actual_saltos == expected_saltos
    assert actual_cuadruplos == expected_cuadruplos


def test_while_loop():
    data = '''
    program PanchoProgram;
    var
      pancho_age: int;
      pancho_weight: float;
      x: int;

    main {
        pancho_age = 8;
        x = 5;

        if (pancho_age > 10) {
            print("Viejo");
        }else{
            print("ar");
        };
      do {
        print("Pancho ladra");
        x = x - 1;
      } while (x > 0);
    }
    end
    '''
    parse_input(data)

    expected_operandos = "[]"
    expected_operadores = "[]"
    expected_tipos = "[]"
    expected_saltos = "[]"
    expected_cuadruplos = "[['=', 501, None, 0], ['=', 502, None, 1], ['>', 0, 503, 401], ['GOTOF', 401, None, 6], ['print', 'Viejo', None, None], ['GOTO', None, None, 7], ['print', 'ar', None, None], ['print', 'Pancho ladra', None, None], ['-', 1, 504, 200], ['=', 200, None, 1], ['>', 1, 505, 402], ['GOTOV', 402, None, 7]]"

    actual_operandos = capture_output(lambda: print(variable_table.pila_operandos))
    actual_operadores = capture_output(lambda: print(variable_table.pila_operadores))
    actual_tipos = capture_output(lambda: print(variable_table.pila_tipos))
    actual_saltos = capture_output(lambda: print(variable_table.pila_saltos))
    actual_cuadruplos = capture_output(lambda: print(variable_table.pila_cuadruplos))

    assert actual_operandos == expected_operandos
    assert actual_operadores == expected_operadores
    assert actual_tipos == expected_tipos
    assert actual_saltos == expected_saltos
    assert actual_cuadruplos == expected_cuadruplos
