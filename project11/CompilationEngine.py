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

    def __init__(self, token_xml):
        self.token_file = open(token_xml)
        self.output_file = open(token_xml.replace("T.", "."), 'w')
        self.current_token = None
        self.advance_token()

    def regex_match(self, token_type):
        if token_type in ['.', '*', '+', '[', ')', '|', '(']:
            token_type = f"\{token_type}"
        return re.search(f"> {token_type} <", self.current_token)

    def advance_token(self):
        self.current_token = self.token_file.readline().strip()

    def write_token(self, line):
        self.output_file.write(line + '\n')

    def compile_class(self):
        self.write_token("<class>")
        for _ in range(3):  # compiling "'class' className '{'"
            self.write_token(self.current_token)
            self.advance_token()
        while True in [bool(self.regex_match(kw)) for kw in ['static', 'field']]:
            self.compile_class_var_dec()

        while True in [bool(self.regex_match(kw)) for kw in ['constructor', 'function', 'method']]:
            self.compile_subroutine_dec()

        self.write_token(self.current_token)  # Compiling '}'
        self.write_token("</class>")

    def compile_class_var_dec(self):
        self.write_token("<classVarDec>")
        for _ in range(3):  # compiling "('static' | 'field') type varName
            self.write_token(self.current_token)
            self.advance_token()

        # Compiling "(',' varName)*"
        while self.regex_match(","):
            for _ in range(2):  # Compiles each "',' varName" pair
                self.write_token(self.current_token)
                self.advance_token()

        self.write_token(self.current_token)  # Compiling ';'
        self.advance_token()
        self.write_token("</classVarDec>")

    def compile_subroutine_dec(self):
        self.write_token("<subroutineDec>")
        for _ in range(4):  # compiling "('constructor' | 'function' | 'method') ('void' | <type>) <subroutineName> '('"
            self.write_token(self.current_token)
            self.advance_token()

        self.compile_parameter_list()
        self.write_token(self.current_token)  # Compiling ')'
        self.advance_token()
        self.compile_subroutine_body()
        self.write_token("</subroutineDec>")

    def compile_parameter_list(self):
        self.write_token("<parameterList>")
        if not self.regex_match(')'):
            for _ in range(2):
                self.write_token(self.current_token)
                self.advance_token()
            while self.regex_match(','):
                for _ in range(3):
                    self.write_token(self.current_token)
                    self.advance_token()
        self.write_token("</parameterList>")

    def compile_subroutine_body(self):
        self.write_token("<subroutineBody>")
        self.write_token(self.current_token)  # Compiling "'{'"
        self.advance_token()

        while self.regex_match('var'):
            self.compile_var_dec()
        self.compile_statements()
        self.write_token(self.current_token)  # Compiling '}'
        self.advance_token()
        self.write_token("</subroutineBody>")

    def compile_var_dec(self):
        self.write_token("<varDec>")
        for _ in range(3):  # compiling "'var' type varName"
            self.write_token(self.current_token)
            self.advance_token()

        # Compiling "(',' varName)*"
        while self.regex_match(","):
            for _ in range(2):  # Compiles each "',' varName" pair
                self.write_token(self.current_token)
                self.advance_token()

        self.write_token(self.current_token)  # Compiling ';'
        self.advance_token()
        self.write_token("</varDec>")

    def compile_statements(self):
        kw_functions = {'let': self.compile_let,
                        'if': self.compile_if,
                        'while': self.compile_while,
                        'do': self.compile_do,
                        'return': self.compile_return
                        }

        self.write_token("<statements>")
        while True:
            found_match = False
            for kw, fn in kw_functions.items():
                if self.regex_match(kw):
                    fn()
                    found_match = True
                    break
            if not found_match:
                break
        self.write_token("</statements>")

    def compile_let(self):
        self.write_token("<letStatement>")

        for _ in range(2):  # Compile 'let' varName
            self.write_token(self.current_token)
            self.advance_token()

        if self.regex_match('['):  # Compile ('[' expression ']')?
            self.write_token(self.current_token)
            self.advance_token()
            self.compile_expression()
            self.write_token(self.current_token)
            self.advance_token()

        self.write_token(self.current_token)  # Compile '='
        self.advance_token()
        self.compile_expression()
        self.write_token(self.current_token)  # Compile ';'
        self.advance_token()
        self.write_token("</letStatement>")

    def compile_if(self):
        self.write_token("<ifStatement>")

        for _ in range(2):  # Compile 'if' '('
            self.write_token(self.current_token)
            self.advance_token()

        self.compile_expression()

        for _ in range(2):  # Compile ')' '{'
            self.write_token(self.current_token)
            self.advance_token()

        self.compile_statements()
        self.write_token(self.current_token)  # Compile '}'
        self.advance_token()

        # Compile else block of if else statement if exists
        if self.regex_match('else'):
            for _ in range(2):  # Compile 'else' '{'
                self.write_token(self.current_token)
                self.advance_token()
            self.compile_statements()
            self.write_token(self.current_token)  # Compile '}'
            self.advance_token()

        self.write_token("</ifStatement>")

    def compile_while(self):
        self.write_token("<whileStatement>")

        for _ in range(2):  # Compile 'while' '('
            self.write_token(self.current_token)
            self.advance_token()

        self.compile_expression()

        for _ in range(2):  # Compile ')' '{'
            self.write_token(self.current_token)
            self.advance_token()

        self.compile_statements()
        self.write_token(self.current_token)
        self.advance_token()

        self.write_token("</whileStatement>")

    def compile_do(self):
        self.write_token("<doStatement>")
        for _ in range(2):
            self.write_token(self.current_token)  # Compile 'do' and first token of subroutine call
            self.advance_token()

        if self.regex_match('('):
            self.write_token(self.current_token)  # Compile '('
            self.advance_token()
        else:
            for _ in range(3):  # Compile '.' subroutineName '('
                self.write_token(self.current_token)
                self.advance_token()

        self.compile_expression_list()

        for _ in range(2):
            self.write_token(self.current_token)  # Compile ')' ';'
            self.advance_token()

        self.write_token("</doStatement>")

    def compile_return(self):
        self.write_token("<returnStatement>")
        self.write_token(self.current_token)  # Compile 'return'
        self.advance_token()
        if not self.regex_match(';'):  # Compile expression if exists
            self.compile_expression()
        self.write_token(self.current_token)  # Compile ';'
        self.advance_token()
        self.write_token("</returnStatement>")

    def compile_expression(self):
        self.write_token("<expression>")
        self.compile_term()
        while True in [bool(self.regex_match(op)) for op in self.operators]:
            self.write_token(self.current_token)  # Compiles 'op'
            self.advance_token()
            self.compile_term()
        self.write_token("</expression>")

    def compile_expression_list(self):
        self.write_token("<expressionList>")

        if not self.regex_match(')'):
            self.compile_expression()

            # Compiling "(',' expression)*"
            while self.regex_match(","):
                self.write_token(self.current_token)  # Compiles ','
                self.advance_token()
                self.compile_expression()

        self.write_token("</expressionList>")

    def compile_term(self):
        self.write_token("<term>")
        if self.current_token.startswith('<identifier>'):  # Compiles varName | varName'['expression']' | subroutineCall
            self.write_token(self.current_token)
            self.advance_token()

            paren_match = self.regex_match('(')
            dot_match = self.regex_match('.')
            arr_match = self.regex_match('[')
            if paren_match or dot_match or arr_match:
                self.write_token(self.current_token)
                self.advance_token()
                if arr_match:  # varName'['expression']'
                    self.compile_expression()
                    self.write_token(self.current_token)  # Compile ']'
                    self.advance_token()
                else:
                    if paren_match or dot_match:  # Compiles subroutineCall
                        if dot_match:  # if external subroutineCall
                            for _ in range(2):  # Compile subroutineName '('
                                self.write_token(self.current_token)
                                self.advance_token()

                        self.compile_expression_list()
                        self.write_token(self.current_token)  # Compile ')'
                        self.advance_token()
        elif self.regex_match('('):  # Compiles '(' expression ')'
            self.write_token(self.current_token)  # Compiles '('
            self.advance_token()
            self.compile_expression()
            self.write_token(self.current_token)  # Compiles ')'
            self.advance_token()
        elif self.regex_match('-') or self.regex_match('~'):  # Compiles unaryOp term
            self.write_token(self.current_token)  # Compiles 'unaryOp'
            self.advance_token()
            self.compile_term()
        else:  # Compiles integerConstant | stringConstant | keywordConstant
            self.write_token(self.current_token)
            self.advance_token()
        self.write_token("</term>")


if __name__ == "__main__":
    comp_engine = CompilationEngine(sys.argv[1])
    while comp_engine.current_token != '</tokens>':
        comp_engine.advance_token()
        if comp_engine.regex_match('class'):
            comp_engine.compile_class()
