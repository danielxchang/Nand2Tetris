import sys
from parser import Parser
from code_writer import CodeWriter


def translate(input_file):
    parser = Parser(input_file)
    writer = CodeWriter(input_file)
    while parser.has_more_commands():
        cmd_type = parser.command_type()
        writer.write_comment(parser.current_command)
        if cmd_type == 'C_ARITHMETIC':
            writer.write_arithmetic(parser.current_command)
        else:
            writer.write_push_pop(parser.current_command.split()[0], parser.arg1(cmd_type), parser.arg2())
        parser.advance()
    parser.close_file()
    writer.close_file()


if __name__ == "__main__":
    input_file = sys.argv[1]
    translate(input_file)
