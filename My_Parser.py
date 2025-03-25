class Parser:
    def __init__(self, table_of_symb):
        self.table_of_symb = table_of_symb
        self.num_row = 1 
        self.len_table = len(table_of_symb)
        self.under_working_line_code = 1
        self.defined_variables = []
        self.status = 'work'
        self.poliz = []
        self.label_array = []
        self.is_val_float = False

    def generate_label(self):
        self.label_array.append((f'm{len(self.label_array)}', len(self.poliz)))
        return self.label_array[len(self.label_array) - 1][0]
    
    def fail(self, msg):
        print(msg)
        self.status = 'unwork'

    def parse_program(self):
        try:
            result = self.parse_statement()
            if result is not True:
                self.fail(f'Encountered invalid keyword {result} at line {self.under_working_line_code}')
        except Exception as e:
            print(f'Parser: Error: {e}')

    def get_symb(self):
        if self.num_row > self.len_table:
            self.fail('get_symb(): unexpected end of the program')
        self.under_working_line_code, lex, tok, _ = self.table_of_symb[self.num_row]
        self.num_row += 1
        return self.under_working_line_code, lex, tok
    
    def parse_statement(self):
        while self.num_row <= self.len_table:
            num_line, lex, tok = self.get_symb()
            if tok == 'id':
                
                result = self.parse_id()
                self.poliz.append(('=', lex))
                if result is 'no_assign':
                    return
                else:
                    print(f'Defined variable {lex}, as {tok} at line {num_line}')
                    
                    if  any(row[0] == lex for row in self.defined_variables):
                        if any(row[0] == lex and row[1] == 'int' for row in self.defined_variables) and self.is_val_float:
                            self.fail(f'Invalid value assigned to int: {lex}')
                    else:
                        if self.is_val_float:
                            self.defined_variables.append((lex, 'float'))
                            self.is_val_float = False
                        else:
                            self.defined_variables.append((lex, 'int'))

            elif (lex, tok) == ('if', 'keyword'):
                self.parse_if()
            elif (lex, tok) == ('else', 'keyword'):
                return 'else'
            elif (lex, tok) == ('end', 'keyword'):
                return 'end'
            else:
                self.fail(f'instruction mismatch: {lex}, {tok}')

        return True

    def parse_assign(self):
        num_line, lex, tok = self.get_symb()
        if lex != '=':
            return False
        
        return True

    def parse_id(self):
        if self.parse_assign():
            
            numLine, lex, tok = self.get_symb()
            if lex in ('+', '-', '*', '/'):
                self.fail(f'Extra operator |{lex}| at line {numLine}')
                numLine, lex, tok = self.get_symb()

            if lex == '(':
                if self.parse_par_op(numLine) is not True:
                    self.fail(f'Parenthesis not closing at line {numLine}')
            else:
                if tok == 'id' and lex in self.defined_variables is False:
                    self.fail(f'Undefined variable {lex} used at line {numLine}')

                if tok in ('int', 'float', 'id'):  # include arithmetic
                    if(tok == 'float'):
                        self.is_val_float = True
                        self.poliz.append((lex, 'float'))
                    elif tok == 'int':
                        self.poliz.append((lex, 'int'))
                    elif(any(row[0] == lex and row[1] == 'float' for row in self.defined_variables)):
                        self.is_val_float = True
                        self.poliz.append((lex, 'int'))

                    result = self.is_arithmetic_operations(numLine, True)
                    if result is True:
                        return True
                    if result is 'rel_op':
                        if self.is_arithmetic_operations(numLine):
                            return True
                    elif result == 'end_par':
                        self.fail(f'Extra parenthesis at line {numLine}')
        else:
            self.fail(f'Invalid symbol. Variable must be declared with correct grammar at line {numLine}')
            return 'no_assign'
        return True
            

    def is_arithmetic_operations(self, this_num_line, is_last_Id = False, bool = False):
        lastMathOp = False  
        
        while True:
            numLine, lex, tok = self.get_symb()
            if(numLine > this_num_line):
                if(lastMathOp == True):
                    self.fail(f'Syntax error, extra operator at the end of line {this_num_line}')
                else:
                    self.num_row -= 1
                    return True
            if lex == '(':
                lastMathOp = False
                if not self.parse_par_op(numLine):
                    self.fail(f"Parentheses don't close at line {numLine} => {lex}")
                continue
            elif is_last_Id == True and tok in ('id', 'int', 'float'):
                self.fail(f'No operation between variables at line {numLine}')
            elif tok == 'rel_op':
                return 'rel_op'
            elif lex == ')':
                return 'end_par'
            elif tok == 'id':
                if lex in self.defined_variables is False:
                    self.fail(f'Undefined variable {lex} used at line {numLine}')
                else:

                    if(any(row[0] == lex and row[1] == 'float' for row in self.defined_variables)):
                        self.is_val_float = True
                    
                    self.poliz.append((lex, 'float'))
                    if bool == True:
                        self.is_arithmetic_operations(this_num_line, True)
                    lastMathOp = False
                    return True
                
            elif tok in ('int', 'float'):
                
                if(tok == 'float'):
                    self.is_val_float = True
                    
                lastMathOp = False
                self.poliz.append((lex, tok))
                return  
            elif lex in ('+', '-', '*', '/'):
                if lex is '/':
                    numLine, lex, tok = self.get_symb()
                    if lex == '0':
                        self.fail(f'Division by 0 at line {numLine}')
                        self.num_row -= 1
                        continue
                
                self.is_arithmetic_operations(this_num_line, False)
                self.poliz.append((lex, 'math_op'))
                is_last_Id = False
                continue
            else:
                self.fail(f'Invalid symbol at line {numLine} |{lex}|')

    def is_bool(self, this_num_line):
        self.is_arithmetic_operations(this_num_line, bool = True)
        self.num_row -= 1
        numLine, lex, tok = self.get_symb()
        if tok == 'rel_op':
            if self.is_arithmetic_operations(this_num_line):
                print(f'Valid boolean expression found at line {this_num_line}')
                self.poliz.append((lex, 'rel_op'))

            return True
        return False
    
    def parse_par_op(self, this_num_line):
        return self.is_arithmetic_operations(this_num_line) == 'end_par'
    
    def parse_if(self):
        if_row_num = self.under_working_line_code
        if not self.is_bool(self.under_working_line_code):
            self.fail(f'Expression passed to if does not return boolean at line {if_row_num}')

        false_label = self.generate_label()
        end_label = self.generate_label()

        self.poliz.append((false_label, 'jf'))
        
          

        result = self.parse_statement()
            
        if result == 'else':
            print(f'Found else at line {self.under_working_line_code}')
            self.poliz.append((end_label, 'jump')) 
            self.poliz.append((false_label, 'label'))
            result = self.parse_statement()

        if result == 'end':
            print(f'Found end at line {self.under_working_line_code}')
            self.poliz.append((end_label, 'label'))  
            return True
        else:
            self.fail(f'End for if not found at line {if_row_num}')

    def save_postfix_code(self, fileName):
        fname = fileName + ".postfix"
        f = open(fname, 'w')
        header = ".target: Postfix Machine\n.version: 0.2\n"  
        f.write(header)
        
        f.write("\n" + ".vars"+ "(\n")
        for id in self.defined_variables:
            f.write(f"   {id}\n")
        f.write(")\n")
        
        f.write("\n" + ".labels"+ "(\n")
        for lbl in self.label_array:
            f.write(f"   {lbl[0]}\t{lbl[1]}\n")
        f.write(")\n")
        
        
        f.write("\n" + ".code"+ "(\n")
        for instr in self.poliz:
            f.write("   "+str(instr[0]).ljust(6)+str(instr[1]).ljust(6)+"\n")
        f.write(")\n")
        
        f.close()
        print(f"Postfix code saved to file {fname}")
