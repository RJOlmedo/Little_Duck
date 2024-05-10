import os
import sys
import pytest

# Añade la carpeta raíz (un nivel arriba) al `sys.path`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa el lexer correctamente ahora
from little_duck_pars import parser

# Prueba 1: Programa básico con declaración de variables y `main`
def test_basic_program():
    data = '''
    program ejemplo;
    var x : int;
    main {
        print("Soy Pancho");
    }
    end;
    '''
    result = parser.parse(data)
    assert result is not 'None', "Parsing failed for the basic program"

# Prueba 2: Programa con declaraciones de funciones y llamadas
def test_functions_and_calls():
    data = '''
    program ejemplo;
    var x : int;
    void ladrar(int x) {
        print("Pancho dice Arrr");
    }
    main {
        ladrar(10);
    }
    end;
    '''
    result = parser.parse(data)
    assert result is not 'None', "Parsing failed for program with functions and calls"

# Prueba 3: Ciclos `while` y `do-while`
def test_loops():
    data = '''
    program ejemplo;
    var x : int;
    main {
        while (x < 10) {
            print("Esto es un While Loop");
        }

        do {
            print("Esto es un do while");
        } while (x < 10);
    }
    end;
    '''
    result = parser.parse(data)
    assert result is not 'None', "Parsing failed for program with loops"

# Prueba 4: Estructuras condicionales
def test_conditionals():
    data = '''
    program ejemplo;
    var x : int;
    main {
        if (x != 5) {
            print("No da 5");
        } else {
            print("Da 5");
        }
    }
    end;
    '''
    result = parser.parse(data)
    assert result is not 'None', "Parsing failed for program with conditionals"

if __name__ == '__main__':
    pytest.main([__file__])
