import sys
import re


class CompilationEngine:
    operators = [
        '+',
        '-',
        '*',
        '/',
        '&amp;',
        '|',
        '&lt;',
        '&gt;',
        '='
    ]

    def __init__(self, token_xml, vm_writer):
        self.token_file = open(token_xml)
        self.vm_writer = vm_writer
        self.current_token = None
        self.class_name = None
        self.line_count = 0
        self.advance_token(1)
        self.statements_tracker = {}

    def regex_match(self, token_type):
        if token_type in ['.', '*', '+', '[', ')', '|', '(']:
            token_type = f"\{token_type}"
        return re.search(f"> {token_type} <", self.current_token)

    def advance_token(self, steps):
        for _ in range(steps):
            self.line_count += 1
            self.current_token = self.token_file.readline().strip()

    def print_current(self):
        print(self.line_count, self.current_token)

    def compile_class(self):
        # compiling "'class' className '{'"
        self.advance_token(1)
        self.class_name = self.current_token.split()[2]
        self.advance_token(2)
        field_variables = 0
        static_variables = 0
        while self.current_token.split()[1] in ['static', 'field']:
            if self.current_token.split()[1] == "static":
                static_variables += self.compile_class_var_dec()
            else:
                field_variables += self.compile_class_var_dec()

        while True in [bool(self.regex_match(kw)) for kw in ['constructor', 'function', 'method']]:
            self.compile_subroutine_dec(field_variables)

        self.advance_token(1)  # Advancing past '}'

    def compile_class_var_dec(self):
        count = 1
        self.advance_token(1)

        # Advancing past "(',' varName)*"
        while self.regex_match(","):
            count += 1
            self.advance_token(2)

        self.advance_token(1)
        return count

    def compile_subroutine_dec(self, field_variables):
        self.statements_tracker['IF'] = -1
        self.statements_tracker['WHILE'] = -1

        subroutine_type = self.current_token.split()[1]

        # compiling "('constructor' | 'function' | 'method') ('void' | <type>) <subroutineName> '('"
        self.advance_token(1)

        # return_type = self.current_token.split()[1]
        self.advance_token(1)
        function_name = f"{self.class_name}.{self.current_token.split()[2]}"
        self.advance_token(2)

        self.compile_parameter_list(True, function_name)
        self.advance_token(1)  # Advance past ')'
        self.compile_subroutine_body(function_name, subroutine_type, field_variables)

    def compile_parameter_list(self, is_definition, f_name):
        n_args = 0
        if is_definition:  # When function declared
            while not self.regex_match(')'):
                n_args += 1
                self.advance_token(1)
                if self.regex_match(','):
                    self.advance_token(1)
        else:  # When called function
            while not self.regex_match(')'):
                n_args += 1
                self.vm_writer.write_push(self.current_token.split()[1], self.current_token.split()[4])
                self.advance_token(1)
                if self.regex_match(','):
                    self.advance_token(1)
            self.vm_writer.write_call(f_name, n_args)

    def compile_subroutine_body(self, subroutine_name, subroutine_type, n_field):
        self.advance_token(1)
        n_locals = 0
        while self.current_token.split()[1] == "var":
            n_locals += self.compile_var_dec()

        self.vm_writer.write_function(subroutine_name, n_locals)
        if subroutine_type == "constructor":
            self.vm_writer.write_push('constant', n_field)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('pointer', 0)
        elif subroutine_type == "method":
            self.vm_writer.write_push('arg', 0)
            self.vm_writer.write_pop('pointer', 0)

        self.compile_statements()
        self.advance_token(1)  # Advance past '}'

    def compile_var_dec(self):
        n_locals = 1

        # Advancing beyond variable declarations
        self.advance_token(1)

        while self.regex_match(","):
            self.advance_token(2)
            n_locals += 1
        self.advance_token(1)
        return n_locals

    def compile_statements(self):
        kw_functions = {'let': self.compile_let,
                        'if': self.compile_if,
                        'while': self.compile_while,
                        'do': self.compile_do,
                        'return': self.compile_return
                        }

        while True:
            found_match = False
            for kw, fn in kw_functions.items():
                if self.regex_match(kw):
                    fn()
                    found_match = True
                    break
            if not found_match:
                break

    def compile_let(self):
        self.advance_token(1)  # Advance past 'let'
        identifier_parts = self.current_token.split()[1:-1]
        segment = identifier_parts[0]
        var_name = identifier_parts[1]
        index = identifier_parts[3]

        self.advance_token(1)
        if self.regex_match("["):
            self.advance_token(1)
            self.compile_expression()
            self.vm_writer.write_push(segment, index)
            self.vm_writer.write_arithmetic('+')

            self.advance_token(2)

            self.compile_expression()
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)

            self.advance_token(1)
        else:
            self.advance_token(1)
            self.compile_expression()
            self.vm_writer.write_pop(segment, index)  # Compile '=': assign right side of '=' sign to left side
            self.advance_token(1)

    def compile_if(self):
        self.statements_tracker['IF'] += 1
        true_label = f"IF_TRUE{self.statements_tracker['IF']}"
        false_label = f"IF_FALSE{self.statements_tracker['IF']}"
        end_label = f"IF_END{self.statements_tracker['IF']}"
        self.advance_token(2) # Advancing beyond 'if' '('
        self.compile_expression()
        self.vm_writer.write_if(true_label)
        self.advance_token(2) # Advancing beyond ')' '{'
        self.vm_writer.write_goto(false_label)
        self.vm_writer.write_label(true_label)
        self.compile_statements()
        self.advance_token(1)  # Advancing beyond '}'

        # Compile else block of if else statement if exists
        if self.regex_match('else'):
            self.vm_writer.write_goto(end_label)
            self.advance_token(2)  # Advancing 'else' '{'
            self.vm_writer.write_label(false_label)
            self.compile_statements()
            self.advance_token(1)  # Advancing beyond '}'
            self.vm_writer.write_label(end_label)
        else:
            self.vm_writer.write_label(false_label)

    def compile_while(self):
        self.statements_tracker['WHILE'] += 1
        start_label = f"WHILE_EXP{self.statements_tracker['WHILE']}"
        end_label = f"WHILE_END{self.statements_tracker['WHILE']}"
        self.advance_token(2)  # Advancing past "while ("
        self.vm_writer.write_label(start_label)
        self.compile_expression()
        self.advance_token(2)  # Advancing past ')' '{'
        self.vm_writer.write_unary("~")
        self.vm_writer.write_if(end_label)
        self.compile_statements()
        self.vm_writer.write_goto(start_label)
        # self.print_current()
        self.vm_writer.write_label(end_label)
        self.advance_token(1)

    def compile_do(self):
        self.advance_token(1)  # Advance past 'do'

        # Compile first token of subroutine call
        category = self.current_token.split()[1]
        if category == 'class':
            command = self.current_token.split()[2]  # Appending class name to command
            self.advance_token(1)
            command = command + self.current_token.split()[1]  # Appending '.' to command
            self.advance_token(1)
        elif category in ['var', 'field']:
            var_parts = self.current_token.split()[1:-1]
            command = var_parts[-1]
            self.vm_writer.write_push(var_parts[0], var_parts[-2])

            self.advance_token(1)
            command = command + self.current_token.split()[1]  # Appending '.' to command
            self.advance_token(1)
        # elif category == 'field':
        #     command = f"{self.class_name}."
        #     self.vm_writer.write_push(category, 0)  # MAYBE DELETE OR CHANGE
        else:
            command = f"{self.class_name}."
            self.vm_writer.write_push('pointer', 0)  # MAYBE DELETE OR CHANGE

        command += self.current_token.split()[2]  # Appending subroutine name to command
        self.advance_token(2)
        n_expressions = self.compile_expression_list()
        if category in ['var', 'subroutine', 'field']:
            n_expressions += 1

        self.vm_writer.write_call(command, n_expressions)
        self.advance_token(2)

        self.vm_writer.write_pop('temp', 0)

    def compile_return(self):
        self.advance_token(1)
        if not self.regex_match(';'):  # Compile expression if exists
            if self.regex_match('this'):  # Returning this
                self.vm_writer.write_push("pointer", 0)
                self.advance_token(1)
            else:
                self.compile_expression()
        else:
            self.vm_writer.write_push("constant", 0)
        self.vm_writer.write_return()  # Compile 'return'
        self.advance_token(1)

    def compile_expression(self):
        self.compile_term()

        while True in [bool(self.regex_match(op)) for op in self.operators]:
            operator = self.current_token.split()[1]
            self.advance_token(1)
            self.compile_term()
            self.vm_writer.write_arithmetic(operator)

    def compile_expression_list(self):
        n_expressions = 0
        if not self.regex_match(')'):
            self.compile_expression()
            n_expressions += 1

            # Compiling "(',' expression)*"
            while self.regex_match(","):
                self.advance_token(1)
                self.compile_expression()
                n_expressions += 1
        return n_expressions

    def compile_term(self):
        if self.current_token.startswith('<identifier>'):  # Compiles varName | varName'['expression']' | subroutineCall
            token_parts = self.current_token.split()[1:-1]
            if token_parts[0] == "class":
                segment, class_name, use_type = token_parts
            else:
                segment = token_parts[0]
                var_name = token_parts[1]
                use_type = token_parts[2]
                index = token_parts[3] if len(token_parts) >= 4 else None
                class_name = token_parts[4] if len(token_parts) >= 5 else None
            self.advance_token(1)

            paren_match = self.regex_match('(')
            dot_match = self.regex_match('.')
            arr_match = self.regex_match('[')
            if paren_match or dot_match or arr_match:
                self.advance_token(1)
                if arr_match:  # varName'['expression']'
                    self.compile_expression()
                    self.vm_writer.write_push(segment, index)
                    self.vm_writer.write_arithmetic('+')
                    # self.vm_writer.write_pop("temp", 0)
                    self.vm_writer.write_pop("pointer", 1)
                    # self.vm_writer.write_push("temp", 0)
                    self.vm_writer.write_push("that", 0)
                    self.advance_token(1)
                    # self.print_current()
                else:
                    if paren_match or dot_match:  # Compiles subroutineCall
                        if dot_match:  # if external subroutineCall
                            f_name = f"{class_name}.{self.current_token.split()[2]}"
                            self.advance_token(2)
                        else:
                            f_name = var_name

                        if segment in ['var', 'subroutine', 'field']:
                            self.vm_writer.write_push(segment, index)
                            n_expressions = self.compile_expression_list()
                            n_expressions += 1
                        else:
                            n_expressions = self.compile_expression_list()

                        self.vm_writer.write_call(f_name, n_expressions)
                        self.advance_token(1)
            else:
                if use_type == "used":
                    self.vm_writer.write_push(segment, index)

        elif self.regex_match('('):  # Compiles '(' expression ')'
            self.advance_token(1)
            self.compile_expression()
            self.advance_token(1)
        elif self.regex_match('-') or self.regex_match('~'):  # Compiles unaryOp term
            unary_op = self.current_token.split()[1]
            self.advance_token(1)
            self.compile_term()
            self.vm_writer.write_unary(unary_op)
        elif self.current_token.startswith('<integerConstant>'):
            # self.print_current()
            self.vm_writer.write_push("constant", self.current_token.split()[1])
            self.advance_token(1)
        elif self.current_token.startswith('<stringConstant>'):
            string = self.current_token.split('"')[1]
            self.vm_writer.write_push("constant", len(string))
            self.vm_writer.write_call("String.new", 1)
            for i, char in enumerate(string):
                self.vm_writer.write_push("constant", ord(char))
                self.vm_writer.write_call("String.appendChar", 2)
            self.advance_token(1)
        elif self.regex_match('this'):
            self.vm_writer.write_push("pointer", 0)
            self.advance_token(1)
        else:  # Compiles keywordConstant
            keyword = self.current_token.split()[1]
            self.vm_writer.write_push("constant", 0)
            if keyword == "true":
                self.vm_writer.write_unary("~")
            self.advance_token(1)


if __name__ == "__main__":
    xml_file = sys.argv[1]
    vm_file = open(xml_file.replace("T.xml", ".vm"), 'w')
    comp_engine = CompilationEngine(xml_file, vm_file)
    while comp_engine.current_token != '</tokens>':
        comp_engine.advance_token()
        if comp_engine.regex_match('class'):
            comp_engine.compile_class()
    vm_file.close()
