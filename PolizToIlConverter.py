class PolizToIlConverter:
    def __init__(self, defined_variables, postfix_code):
        self.defined_variables = defined_variables  
        self.postfix_code = postfix_code 
        self.intenger_labels = 0
        self.il_code = []
        

    def get_type(self, var_name):
        for var, var_type in self.defined_variables:
            if var == var_name:
                return var_type
        return None

    def convert(self):
        il_code = []
        local_vars = {var: var_type for var, var_type in self.defined_variables}
        
        il_code.append('.assembly solve {}')
        il_code.append('.method public static void Main(){')
        il_code.append('.entrypoint')
        il_code.append('.locals init (')
        for i, (var, var_type) in enumerate(self.defined_variables):
            if i == len(self.defined_variables) - 1:
                il_code.append(f'float32 {var}')
            else:
                il_code.append(f'float32 {var},')
        il_code.append(')')

        self.il_code = self.analiz(il_code)
        self.il_code += 'ret\n}'
    
    def analiz(self, il_code):

        for index, (value, value_type) in enumerate(self.postfix_code):
            
            if value == '=':
                il_code.append(f"    stloc.{self.get_loc_index(value_type)}")
            
            if any(row[0] == value for row in self.defined_variables):
                if value_type == 'float':
                    il_code.append(f"    ldloc.{self.get_loc_index(value)}")
                elif value_type == 'int':
                    il_code.append(f"    ldloc.{self.get_loc_index(value)}")
            else:
                if value_type == 'float':
                    il_code.append(f"    ldc.r4 {value}")
                elif value_type == 'int':
                    il_code.append(f"    ldc.r4 {value}.0")

            

            if value_type == 'math_op':
                il_code.append(f"    {self.get_operation(value)}")
                
            elif value_type == 'rel_op': 
                if value == '>':
                    il_code.append("    cgt")  
                elif value == '<':
                    il_code.append("    clt")  
                elif value == '>=':
                    il_code.append("    clt")  
                    il_code.append("    ldc.i4.0")
                    il_code.append("    ceq")  
                elif value == '<=':
                    il_code.append("    cgt") 
                    il_code.append("    ldc.i4.0")
                    il_code.append("    ceq")  
                elif value == '==':
                    il_code.append("    ceq")  
                elif value == '!=':
                    il_code.append("    ceq")  
                    il_code.append("    ldc.i4.0")
                    il_code.append("    ceq")  

            elif value_type == 'jf':
                il_code.append(f"    brfalse.s {value}")
            
            elif value_type == 'jump':
                il_code.append(f"    br.s {value}")

            elif value_type == 'label':
                il_code.append(f"{value}:")
            
        return "\n".join(il_code)


    def get_new_label(self):
        self.label_array.append(f'm{len(self.label_array)}')

    def get_loc_index(self, var_name):
        """Возвращает индекс локальной переменной по имени."""
        return next((i for i, row in enumerate(self.defined_variables) if row[0] == var_name), -1)
    

    def get_operation(self, op_type):
        """Возвращает соответствующую операцию в IL для арифметических операций."""
        operations = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div'
        }
        return operations.get(op_type, 'nop')
    
    def save_il_file(self, fileName):
        fname = fileName + ".il"
        f = open(fname, 'w')
        for row in self.il_code:   
            f.write(row)
        f.close()

