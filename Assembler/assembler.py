import sys
from parser import Parser
from code import Code
from symbol_table import SymbolTable
from pprint import pprint


def extract_lines(input_file):
    file = open(f"symbolic-files/{input_file}", 'r')
    return [line.split("/")[0].strip() for line in file.readlines() if line != "\n" and line[0] != '/']


def write_to_file(binary_commands, file_name):
    with open(f"binary-files/{file_name}.hack", "w") as file:
        file.writelines(binary_commands)


def assembler(input_file):
    lines = extract_lines(input_file)
    binary_commands = []
    parser = Parser(lines)
    symbol_table = SymbolTable(lines)
    code = Code()

    while parser.has_more_commands():
        command_type = parser.get_command_type()
        if command_type == "A":  # A command
            symbol = parser.get_symbol(command_type)
            address = symbol_table.check_symbol(symbol)
            binary_address = bin(int(address))[2:].zfill(15)
            binary_instruction = "0" + binary_address
        elif command_type == 'L':
            parser.advance_command()
            continue
        else:  # C command
            dest, comp, jump = parser.parse_c_command()
            binary_instruction = "111" + code.convert_comp(comp) + code.convert_dest(dest) + code.convert_jump(jump)
        binary_commands.append(binary_instruction + '\n')
        parser.advance_command()

    write_to_file(binary_commands, input_file.split('.')[0].split("/")[-1])


if __name__ == "__main__":
    symbolic_file = sys.argv[1]
    assembler(symbolic_file)