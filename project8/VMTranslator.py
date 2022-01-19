import sys
from parser import Parser
from code_writer import CodeWriter
import os


def translate(fpath):
    is_directory = os.path.isdir(fpath)
    vm_files = []
    if is_directory:
        file_path = fpath
        output_file_name = os.path.basename(fpath)
        files = os.listdir(fpath)
        for file in files:
            if file.split('.')[-1] == 'vm':
                vm_files.append(f"{fpath}/{file}")
        vm_files.sort()
    else:
        file_path = '/'.join(fpath.split('/')[:-1])
        output_file_name = os.path.basename(fpath).split('.')[0]
        vm_files.append(fpath)

    writer = CodeWriter(output_file_name, file_path)
    if is_directory:
        writer.write_init()
    while vm_files:
        if f"{file_path}/Sys.vm" in vm_files:
            vm_file = vm_files.pop(vm_files.index(f"{file_path}/Sys.vm"))
        elif f"{file_path}/Main.vm" in vm_files:
            vm_file = vm_files.pop(vm_files.index(f"{file_path}/Main.vm"))
        else:
            vm_file = vm_files.pop()

        parser = Parser(vm_file)
        writer.current_file = os.path.basename(vm_file).split(".")[0]
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
                    if command == "function":
                        writer.write_function(parser.arg1(cmd_type), parser.arg2())
                    elif command == "call":
                        writer.write_call(parser.arg1(cmd_type), parser.arg2())
                    else:
                        writer.write_return()
            parser.advance()
        parser.close_file()
    writer.close_file()


if __name__ == "__main__":
    fpath = sys.argv[1][:-1] if sys.argv[1][-1] == "/" else sys.argv[1]
    translate(fpath)
