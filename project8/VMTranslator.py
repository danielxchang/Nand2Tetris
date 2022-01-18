import sys
from parser import Parser
from code_writer import CodeWriter
import os


def translate(fpath):
    file_path = '/'.join(fpath.split('/')[:-1])
    if os.path.isdir(fpath):
        output_file_name = os.path.basename(fpath)
    else:
        output_file_name = os.path.basename(fpath).split('.')[0]

    writer = CodeWriter(output_file_name, file_path)
    parser = Parser(fpath)

    while parser.has_more_commands():
        if parser.current_command:
            cmd_type = parser.command_type()
            writer.write_comment(parser.current_command)
            command = parser.current_command.split()[0]
            if cmd_type == 'C_ARITHMETIC':
                writer.write_arithmetic(parser.current_command)
            elif cmd_type == 'C_PUSH':
                writer.write_push_pop(parser.current_command.split()[0], parser.arg1(cmd_type), parser.arg2())
            elif cmd_type == 'C_BRANCH':
                if command == 'label':
                    writer.write_label(parser.arg1(cmd_type))
                elif command == 'goto':
                    writer.write_go_to(parser.arg1(cmd_type))
                else:
                    writer.write_if(parser.arg1(cmd_type))
            else:
                pass
        parser.advance()
    parser.close_file()
    writer.close_file()


if __name__ == "__main__":
    fpath = sys.argv[1]
    translate(fpath)
