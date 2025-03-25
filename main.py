from base_lexem import tableOfSymb
from PolizToIlConverter import PolizToIlConverter
from My_Parser import Parser
from compile_il import compile_il
from compile_il import run
import os

prosfix_file_name = 'prosfixFile'
il_file_name = 'ilFile'

table_of_symb = tableOfSymb
parser = Parser(table_of_symb)

print('\nCode analysis and, if present, errors\n')
parser.parse_program()
if parser.status == 'unwork':
    print('The program is not compiled')
else:
    print('\nPOLIZ code:\n')
    print('Defined variables')
    print('index\ttype')
    i = 0
    for id in parser.defined_variables:
        print(f'{i}\t{id}')
        i += 1

    print('\nProgram code in postfix notation (POLIZ)')
    print('№\tpostfixCode')
    print('-\t-----------')
    i = 0
    for line in parser.poliz:
        print(f'{i}\t({line[0]}, {line[1]})')
        i += 1


    print('Result of converting POLIZ code to CLR: \n')
    parser.save_postfix_code(f'{os.getcwd()}\\{prosfix_file_name}')
    converter = PolizToIlConverter(parser.defined_variables, parser.poliz)
    converter.convert()
    print(converter.il_code)
    
    print('Running the program: \n')
    converter.save_il_file(f'{os.getcwd()}\\{il_file_name}')
    path_to_exe = compile_il(f'{os.getcwd()}\\{il_file_name}')
    print('Path to the compiled program: ' + path_to_exe)
    print(run(path_to_exe))
