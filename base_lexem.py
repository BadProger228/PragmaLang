# Token table for the language
tableOfLanguageTokens = {
    'if': 'keyword', 'else': 'keyword', 'end': 'keyword', 
    '=': 'assign_op', '.': 'dot', ' ': 'ws', '\t': 'ws', '\n': 'nl', ';': 'nl', 
    '-': 'add_op', '+': 'add_op', '*': 'mult_op', '/': 'mult_op', 
    '(': 'par_op', ')': 'par_op', '==': 'rel_op', '!=': 'rel_op', 
    '<=': 'rel_op', '>=': 'rel_op', '<': 'rel_op', '>': 'rel_op', '<>': 'rel_op'
}

# Table for determining types of variables and numbers
tableIdentFloatInt = {2: 'id', 6: 'float', 9: 'int'}

# State transition table for the automaton
stf = {
    (0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
    (0, 'Digit'): 4, (4, 'Digit'): 4, (4, 'dot'): 5, (4, 'other'): 9,
    (5, 'Digit'): 5, (5, 'other'): 6, (0, '='): 12, (11, 'other'): 102,
    (0, 'ws'): 0, (0, 'nl'): 13, (0, '+'): 14, (0, '-'): 14, (0, '*'): 14, 
    (0, '/'): 14, (0, '('): 14, (0, ')'): 14, (0, '<'): 20, (20, '='): 21,
    (20, '>'): 22, (20, 'other'): 23, (0, '>'): 30, (30, '='): 31, 
    (30, 'other'): 33, (0, '=='): 40, (0, '!='): 40, (0, 'other'): 101
}

# Initial values
initState = 0
F = {2, 6, 9, 12, 13, 14, 101, 102, 21, 22, 23, 31, 33, 40}
Fstar = {2, 6, 9, 23, 33}
Ferror = {101, 102}

# Tables for variables, constants, and symbols
tableOfVar = {}
tableOfConst = {}
tableOfSymb = {}

state = initState
sourceCode = ''
numLine = 1
numChar = -1
char = ''
lexeme = ''
FSucces = ('Lexer', True)

def lex():
    global state, char, lexeme, FSucces
    while numChar < lenCode:
        char = nextChar()
        classCh = classOfChar(char)
        state = nextState(state, classCh)
        
        if is_final(state): 
            processing()
            if state in Ferror:
                FSucces = ('Lexer', False)
                break
        elif state == 0:
            lexeme = ''
        else:
            lexeme += char

    if FSucces == ('Lexer', True):
        print('Lexer: Lexical analysis completed successfully')
    else:
        print('Lexer: Lexical analysis failed')  
    return FSucces

def processing():
    global state, lexeme, numLine, numChar, FSucces
    if state == 13:  # \n
        numLine += 1
        state = 0
    if state in (2, 6, 9):  # keyword, id, float, int
        token = getToken(state, lexeme) 
        if token != 'keyword':  # not a keyword
            index = indexVarConst(state, lexeme)
            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s} {index:<2d}')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, index)
        else:  # if keyword
            print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        numChar = putCharBack(numChar)  # put character back
        state = 0
    if state == 12:  # Assignment operator '='
        lexeme += char
        token = getToken(state, lexeme)
        print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = '' 
        state = 0
    if state == 14:  # Operators +, -, *, /
        lexeme += char
        token = getToken(state, lexeme)
        print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = '' 
        state = 0
    if state in (21, 22, 31, 40):  # Comparison operators
        lexeme += char
        token = getToken(state, lexeme)
        print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = '' 
        state = 0
    if state in (23, 33):  # Comparison operators with special characters
        token = getToken(state, lexeme)
        print(f'{numLine:<3d} {lexeme:<10s} {token:<10s}')
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = '' 
        numChar = putCharBack(numChar)  # put character back
        state = 0
    if state in (101, 102):  # ERROR
        FSucces = ('Lexer', False)
        fail()

def fail():
    print(numLine)
    if state == 101:
        print(f'Lexer: unexpected character {char} at line {numLine}')
    if state == 102:
        print(f'Lexer: expected character = at line {numLine}, but found {char}')

def is_final(state):
    return state in F

def nextState(state, classCh):
    try:
        return stf[(state, classCh)]
    except KeyError:
        return stf[(state, 'other')]

def nextChar():
    global numChar
    numChar += 1
    return sourceCode[numChar]

def putCharBack(numChar):
    return numChar - 1

def classOfChar(char):
    if char in '.':
        return "dot"
    elif char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        return "Letter"
    elif char in "0123456789":
        return "Digit"
    elif char in " ":
        return "ws"
    elif char in "\t":
        return "ws"
    elif char in ";":
        return "nl"
    elif char in "\n":
        return "nl"
    elif char in "*/+-=()<>" :
        return char
    return "other"

def getToken(state, lexeme):
    return tableOfLanguageTokens.get(lexeme, tableIdentFloatInt.get(state))

def indexVarConst(state, lexeme):
    indx = 0
    if state == 2:  # id
        indx = tableOfVar.get(lexeme)
        if indx is None:
            indx = len(tableOfVar) + 1
            tableOfVar[lexeme] = indx
    elif state in (6, 9):  # float, int
        indx = tableOfConst.get(lexeme)
        if indx is None:
            indx = len(tableOfConst) + 1
            tableOfConst[lexeme] = indx
    return indx


# Input data
f = open('test.ruby', 'r')
sourceCode = f.read() + ' '  # add space at the end to finish the lexeme
f.close()

lenCode = len(sourceCode) - 1

# Start lexical analysis
lex()
