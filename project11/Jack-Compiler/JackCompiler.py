import sys
import os
from Tokenizer import Tokenizer
from CompilationEngine import CompilationEngine
from SymbolTable import SymbolTable
from VMWriter import VMWriter
from pprint import pprint


# Gathers jack file(s) from program_input parameter and returns a list of jack files to be tokenized
def retrieve_jack_files(program_input):
    jack_files = []

    if os.path.isdir(program_input):  # if program_input is a directory
        directory_path = os.path.dirname(program_input if program_input[-1] == "/" else program_input + "/")

        for file in os.listdir(program_input):
            if file.split('.')[-1] == 'jack':
                jack_files.append(f"{directory_path}/{file}")

    else:  # if program_input is a file
        jack_files.append(program_input)

    return jack_files


def run_jack_compiler(jack_files):
    for file in jack_files:
        tokenizer = Tokenizer(file)  # Instantiates new tokenizer object for each file
        symbol_table = SymbolTable()

        while tokenizer.has_more_tokens():
            tokenizer.advance()
            tokens = tokenizer.token_type()
            this = tokenizer.class_name
            i = 0
            while i < len(tokens):
                token_tuple = tokens[i]
                if token_tuple[0] in ['var', 'field', 'static']:  # Handles variable declarations
                    kind = token_tuple[0]
                    token_type = tokens[i + 1][0]
                    name = tokens[i + 2][0]
                    symbol_table.define(name, token_type, kind)
                    symbol_string = f"{kind} {name} defined {symbol_table.index_of(name)}"
                    i += 2
                    token = tokenizer.get_token_string(tokens[i], symbol_string)
                    tokenizer.write_to_xml(token)
                    i += 1
                    while tokens[i][0] == ",":
                        token = tokenizer.get_token_string(tokens[i])
                        tokenizer.write_to_xml(token)
                        i += 1

                        name = tokens[i][0]
                        symbol_table.define(name, token_type, kind)
                        symbol_string = f"{kind} {name} defined {symbol_table.index_of(name)}"
                        token = tokenizer.get_token_string(tokens[i], symbol_string)
                        tokenizer.write_to_xml(token)
                        i += 1

                elif token_tuple[0] in ['method', 'constructor', 'function']: # Handles subroutine declaration
                    symbol_table.start_subroutine()
                    for _ in range(2):  # writing subroutine keywords
                        token = tokenizer.get_token_string(tokens[i])
                        tokenizer.write_to_xml(token)
                        i += 1

                    token = tokenizer.get_token_string(tokens[i], f"subroutine {tokens[i][0]} defined")  # subroutine identifier
                    tokenizer.write_to_xml(token)
                    i += 1

                    token = tokenizer.get_token_string(tokens[i])  # Writing '('
                    tokenizer.write_to_xml(token)
                    i += 1

                    if token_tuple[0] in ['method']:
                        symbol_table.define('this', this, 'ARG')

                    while tokens[i][0] != ")":  # Handles the subroutine argument variable declarations
                        if tokens[i][0] == ',':
                            token = tokenizer.get_token_string(tokens[i])
                            tokenizer.write_to_xml(token)
                            i += 1

                        symbol_type = tokens[i][0]
                        name = tokens[i + 1][0]
                        symbol_table.define(name, symbol_type, 'ARG')
                        symbol_string = f"arg {name} defined {symbol_table.index_of(name)}"

                        i += 1
                        token = tokenizer.get_token_string(tokens[i], symbol_string)
                        tokenizer.write_to_xml(token)
                        i += 1

                elif token_tuple[0] == "class":  # Handles class declaration
                    token = tokenizer.get_token_string(token_tuple)
                    tokenizer.write_to_xml(token)
                    i += 1

                    token = tokenizer.get_token_string(tokens[i], f"class {tokens[i][0]} defined")
                    tokenizer.write_to_xml(token)
                    i += 1
                elif token_tuple[1] == "IDENTIFIER":  # Handles identifier uses
                    kind = symbol_table.kind_of(token_tuple[0])

                    if kind:  # symbol found in symbol table
                        index = symbol_table.index_of(token_tuple[0])
                        symbol_string = f"{kind.lower()} {token_tuple[0]} used {index} {symbol_table.type_of(token_tuple[0])}"
                    else:  # symbol not found -> subroutine name or class name
                        symbol_string = f"class {token_tuple[0]} used" if tokens[i + 1][0] != "(" else f"subroutine {token_tuple[0]} used"

                    token = tokenizer.get_token_string(token_tuple, symbol_string)
                    tokenizer.write_to_xml(token)
                    i += 1

                else:  # Handles non-identifier tokens
                    token = tokenizer.get_token_string(token_tuple)
                    tokenizer.write_to_xml(token)
                    i += 1

        tokenizer.close_xml_file()

        # Creates output .vm file
        vm_writer = VMWriter(tokenizer.xml_file_name)

        # Instantiates new compilation engine object for each file
        comp_engine = CompilationEngine(tokenizer.xml_file_name, vm_writer)

        while comp_engine.current_token != '</tokens>':
            comp_engine.advance_token(1)
            if comp_engine.regex_match('class'):
                comp_engine.compile_class()
        vm_writer.close()


if __name__ == "__main__":
    run_jack_compiler(retrieve_jack_files(sys.argv[1]))
