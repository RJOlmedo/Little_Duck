import os
import sys
import pytest

# Añade la carpeta raíz (un nivel arriba) al `sys.path`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from little_duck_pars import parser, ASTNode

def assert_ast_node(node, expected_type, expected_value=None, expected_children=None):
    assert node.type == expected_type
    assert node.value == expected_value
    if expected_children is not None:
        assert len(node.children) == len(expected_children)
        for child, expected_child in zip(node.children, expected_children):
            assert_ast_node(child, expected_child.type, expected_child.value, expected_child.children)

def test_basic_program():
    data = '''
    program ejemplo;
    var x : int;
    main {
        print("Hola Mundo");
    }
    end;
    '''
    result = parser.parse(data)

    expected_ast = ASTNode('Programa', [
        ASTNode('Vars', [
            ASTNode('ListaVars', [
                ASTNode('ID', value='x')
            ]),
            ASTNode('TYPE', value='int')
        ]),
        ASTNode('Funcoes', value='epsilon'),
        ASTNode('ID', value='main'),
        ASTNode('Body', [
            ASTNode('Statements', [
                ASTNode('Print', [
                    ASTNode('CTE', value='Hola Mundo')
                ]),
                ASTNode('Statements', value='epsilon')
            ])
        ]),
        ASTNode('ID', value='end')
    ])

    assert_ast_node(result, expected_ast.type, expected_ast.value, expected_ast.children)

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

    expected_ast = ASTNode('Programa', [
        ASTNode('Vars', [
            ASTNode('ListaVars', [
                ASTNode('ID', value='x')
            ]),
            ASTNode('TYPE', value='int')
        ]),
        ASTNode('Funcoes', [
            ASTNode('Funcion', [
                ASTNode('ID', value='ladrar'),
                ASTNode('Parametros', [
                    ASTNode('ID', value='x', children=[ASTNode('TYPE', value='int')])
                ]),
                ASTNode('Body', [
                    ASTNode('Statements', [
                        ASTNode('Print', [
                            ASTNode('CTE', value='Pancho dice Arrr')
                        ]),
                        ASTNode('Statements', value='epsilon')
                    ])
                ])
            ]),
            ASTNode('Funcoes', value='epsilon')
        ]),
        ASTNode('ID', value='main'),
        ASTNode('Body', [
            ASTNode('Statements', [
                ASTNode('F_Call', [
                    ASTNode('ID', value='ladrar'),
                    ASTNode('Expresiones', [
                        ASTNode('CTE', value=10)
                    ])
                ]),
                ASTNode('Statements', value='epsilon')
            ])
        ]),
        ASTNode('ID', value='end')
    ])

    assert_ast_node(result, expected_ast.type, expected_ast.value, expected_ast.children)

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

    expected_ast = ASTNode('Programa', [
        ASTNode('Vars', [
            ASTNode('ListaVars', [
                ASTNode('ID', value='x')
            ]),
            ASTNode('TYPE', value='int')
        ]),
        ASTNode('Funcoes', value='epsilon'),
        ASTNode('ID', value='main'),
        ASTNode('Body', [
            ASTNode('Statements', [
                ASTNode('CYCLE', [
                    ASTNode('Expresion', [
                        ASTNode('ID', value='x'),
                        ASTNode('Operator', value='<'),
                        ASTNode('CTE', value=10)
                    ]),
                    ASTNode('Body', [
                        ASTNode('Statements', [
                            ASTNode('Print', [
                                ASTNode('CTE', value='Esto es un While Loop')
                            ]),
                            ASTNode('Statements', value='epsilon')
                        ])
                    ])
                ]),
                ASTNode('Statements', [
                    ASTNode('CYCLE', [
                        ASTNode('Body', [
                            ASTNode('Statements', [
                                ASTNode('Print', [
                                    ASTNode('CTE', value='Esto es un do while')
                                ]),
                                ASTNode('Statements', value='epsilon')
                            ])
                        ]),
                        ASTNode('Expresion', [
                            ASTNode('ID', value='x'),
                            ASTNode('Operator', value='<'),
                            ASTNode('CTE', value=10)
                        ])
                    ]),
                    ASTNode('Statements', value='epsilon')
                ])
            ])
        ]),
        ASTNode('ID', value='end')
    ])

    assert_ast_node(result, expected_ast.type, expected_ast.value, expected_ast.children)

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
    end;
    '''
    result = parser.parse(data)

    expected_ast = ASTNode('Programa', [
        ASTNode('Vars', [
            ASTNode('ListaVars', [
                ASTNode('ID', value='x')
            ]),
            ASTNode('TYPE', value='int')
        ]),
        ASTNode('Funcoes', value='epsilon'),
        ASTNode('ID', value='main'),
        ASTNode('Body', [
            ASTNode('Statements', [
                ASTNode('CONDITION', [
                    ASTNode('Expresion', [
                        ASTNode('ID', value='x'),
                        ASTNode('Operator', value='!='),
                        ASTNode('CTE', value=5)
                    ]),
                    ASTNode('Body', [
                        ASTNode('Statements', [
                            ASTNode('Print', [
                                ASTNode('CTE', value='No da 5')
                            ]),
                            ASTNode('Statements', value='epsilon')
                        ])
                    ]),
                    ASTNode('Body', [
                        ASTNode('Statements', [
                            ASTNode('Print', [
                                ASTNode('CTE', value='Da 5')
                            ]),
                            ASTNode('Statements', value='epsilon')
                        ])
                    ])
                ]),
                ASTNode('Statements', value='epsilon')
            ])
        ]),
        ASTNode('ID', value='end')
    ])

    assert_ast_node(result, expected_ast.type, expected_ast.value, expected_ast.children)

if __name__ == '__main__':
    pytest.main([__file__])
