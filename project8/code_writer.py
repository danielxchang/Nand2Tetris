class CodeWriter:
    special_symbols = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT'
    }

    def __init__(self, file_name, file_path):
        self.file_path = file_path
        self.file_name = file_name
        self.current_file = None
        self.file = open(f"{self.file_path + '/' + self.file_name if self.file_path else self.file_name}.asm", mode='w')
        self.next_number = 0
        self.call_integer = 0
        self.call_stack = []
        self.count = 0

    def set_current_file(self, file_name):
        self.current_file = file_name

    def write_init(self):
        commands = [
            '@256',
            'D=A',
            '@SP',
            'M=D',
            '@LCL',
            'M=-A',
            '@ARG',
            'M=-A',
            '@THIS',
            'M=-A',
            '@THAT',
            'M=-A',
        ]
        # commands = [
        #     '@256',
        #     'D=A',
        #     '@SP',
        #     'M=D',
        #     '@300',
        #     'D=A',
        #     '@LCL',
        #     'M=D',
        #     '@400',
        #     'D=A',
        #     '@ARG',
        #     'M=D',
        #     '@3000',
        #     'D=A',
        #     '@THIS',
        #     'M=D',
        #     '@3010',
        #     'D=A',
        #     '@THAT',
        #     'M=D'
        # ]
        self.append_code(commands)
        self.write_call('Sys.init', 0)
        # self.call_stack.append('Sys.init')

    def append_code(self, commands):
        for command in commands:
            self.file.write(command + "\n")

    def write_comment(self, command):
        self.count += 1
        self.file.write(f"// {command.strip()}\n")

    def write_arithmetic(self, vm_command):
        commands = ['@SP']
        if vm_command == 'neg':
            commands.append('A=M-1')
            commands.append('M=-M')
        elif vm_command == 'not':
            commands.append('A=M-1')
            commands.append('M=!M')
        else:
            commands.append('AM=M-1')
            commands.append('D=M')
            commands.append('A=A-1')
            if vm_command == 'add':
                commands.append('D=D+M')
                commands.append('M=D')
            elif vm_command == 'sub':
                commands.append('D=M-D')
                commands.append('M=D')
            elif vm_command == 'and':
                commands.append('D=D&M')
                commands.append('M=D')
            elif vm_command == 'or':
                commands.append('D=D|M')
                commands.append('M=D')
            else:
                self.next_number += 1
                commands.append('D=M-D')
                if vm_command == 'eq':
                    commands.append(f'@EQTRUE{self.next_number}')
                    commands.append('D;JEQ')
                    commands.append('@SP')
                    commands.append('A=M-1')
                    commands.append('M=0')
                    commands.append(f'@ENDIF{self.next_number}')
                    commands.append('0;JMP')
                    commands.append(f'(EQTRUE{self.next_number})')
                    commands.append('@SP')
                    commands.append('A=M-1')
                    commands.append('M=-1')
                elif vm_command == 'gt':
                    commands.append(f'@GTTRUE{self.next_number}')
                    commands.append('D;JGT')
                    commands.append('@SP')
                    commands.append('A=M-1')
                    commands.append('M=0')
                    commands.append(f'@ENDIF{self.next_number}')
                    commands.append('0;JMP')
                    commands.append(f'(GTTRUE{self.next_number})')
                    commands.append('@SP')
                    commands.append('A=M-1')
                    commands.append('M=-1')
                else:
                    commands.append(f'@LTTRUE{self.next_number}')
                    commands.append('D;JLT')
                    commands.append('@SP')
                    commands.append('A=M-1')
                    commands.append('M=0')
                    commands.append(f'@ENDIF{self.next_number}')
                    commands.append('0;JMP')
                    commands.append(f'(LTTRUE{self.next_number})')
                    commands.append('@SP')
                    commands.append('A=M-1')
                    commands.append('M=-1')
                commands.append(f'(ENDIF{self.next_number})')

        self.append_code(commands)

    def write_push_pop(self, command, segment, index):
        commands = []
        if segment == 'constant':
            commands.append(f'@{index}')
            commands.append('D=A')
            commands.append('@SP')
            commands.append('A=M')
            commands.append('M=D')
            commands.append('@SP')
            commands.append('M=M+1')
        elif segment in self.special_symbols:
            special_symbol = self.special_symbols[segment]
            if command == 'pop':
                commands.append(f'@{index}')
                commands.append('D=A')
                commands.append(f'@{special_symbol}')
                commands.append('D=M+D')
                commands.append('@R13')
                commands.append('M=D')
                commands.append('@SP')
                commands.append('AM=M-1')
                commands.append('D=M')
                commands.append('@R13')
                commands.append('A=M')
                commands.append('M=D')
            elif command == 'push':
                commands.append(f'@{index}')
                commands.append('D=A')
                commands.append(f'@{special_symbol}')
                commands.append('A=M+D')
                commands.append('D=M')
                commands.append('@SP')
                commands.append('A=M')
                commands.append('M=D')
                commands.append('@SP')
                commands.append('M=M+1')
        elif segment == 'temp':
            if command == 'pop':
                commands.append(f'@{index}')
                commands.append('D=A')
                commands.append('@5')
                commands.append('D=A+D')
                commands.append('@R13')
                commands.append('M=D')
                commands.append('@SP')
                commands.append('AM=M-1')
                commands.append('D=M')
                commands.append('@R13')
                commands.append('A=M')
                commands.append('M=D')
            elif command == 'push':
                commands.append(f'@{index}')
                commands.append('D=A')
                commands.append('@5')
                commands.append('A=A+D')
                commands.append('D=M')
                commands.append('@SP')
                commands.append('A=M')
                commands.append('M=D')
                commands.append('@SP')
                commands.append('M=M+1')
        elif segment == 'pointer':
            self.next_number += 1
            if command == 'pop':
                commands.append(f'@{index}')
                commands.append('D=A')
                commands.append(f'@ACCESSTHIS{self.next_number}')
                commands.append('D;JEQ')
                commands.append('@SP')
                commands.append('AM=M-1')
                commands.append('D=M')
                commands.append('@THAT')
                commands.append('M=D')
                commands.append(f'@ENDPOINTER{self.next_number}')
                commands.append('0;JMP')
                commands.append(f'(ACCESSTHIS{self.next_number})')
                commands.append('@SP')
                commands.append('AM=M-1')
                commands.append('D=M')
                commands.append('@THIS')
                commands.append('M=D')
                commands.append(f'(ENDPOINTER{self.next_number})')
            elif command == 'push':
                commands.append(f'@{index}')
                commands.append('D=A')
                commands.append(f'@ACCESSTHIS{self.next_number}')
                commands.append('D;JEQ')
                commands.append('@THAT')
                commands.append('D=M')
                commands.append(f'@ENDPOINTER{self.next_number}')
                commands.append('0;JMP')
                commands.append(f'(ACCESSTHIS{self.next_number})')
                commands.append('@THIS')
                commands.append('D=M')
                commands.append(f'(ENDPOINTER{self.next_number})')
                commands.append('@SP')
                commands.append('A=M')
                commands.append('M=D')
                commands.append('@SP')
                commands.append('M=M+1')
        elif segment == "static":
            if command == 'pop':
                commands.append('@SP')
                commands.append('AM=M-1')
                commands.append('D=M')
                commands.append(f'@{self.current_file}.{index}')
                commands.append('M=D')
            elif command == 'push':
                commands.append(f'@{self.current_file}.{index}')
                commands.append('D=M')
                commands.append('@SP')
                commands.append('A=M')
                commands.append('M=D')
                commands.append('@SP')
                commands.append('M=M+1')

        self.append_code(commands)

    def write_label(self, label):
        if self.call_stack:
            label = f"{self.call_stack[-1]}${label}"
        commands = [f'({label})']
        self.append_code(commands)

    def write_go_to(self, label):
        if self.call_stack:
            label = f"{self.call_stack[-1]}${label}"
        commands = [
            f'@{label}',
            '0;JMP'
        ]
        self.append_code(commands)

    def write_if(self, label):
        if self.call_stack:
            label = f"{self.call_stack[-1]}${label}"
        commands = [
            '@SP',
            'AM=M-1',
            'D=M',
            f'@{label}',
            'D;JNE'
        ]
        self.append_code(commands)

    def write_function(self, function_name, num_vars):
        self.call_stack.append(function_name)
        commands = [
            f'({function_name})',
            f'@{num_vars}',
            'D=A',
            '@SP',
            'M=M+D',
            f'(NVARSLOOP:{function_name})',
            f'@ENDNVARSLOOP:{function_name}',
            'D;JEQ',
            'D=D-1',
            '@LCL',
            'A=M+D',
            'M=0',
            f'@NVARSLOOP:{function_name}',
            '0;JMP',
            f'(ENDNVARSLOOP:{function_name})'
        ]
        self.append_code(commands)

    def write_call(self, function_name, num_args):
        self.call_integer += 1
        return_label = f"{self.call_stack[-1] if self.call_stack else ''}$ret.{self.call_integer}"
        commands = [
            f'@{return_label}',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@LCL',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@ARG',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@THIS',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@THAT',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'MD=M+1',
            '@LCL',
            'M=D',
            '@5',
            'D=D-A',
            f'@{num_args}',
            'D=D-A',
            '@ARG',
            'M=D',
            f'@{function_name}',
            '0;JMP',
            f'({return_label})'
        ]
        self.append_code(commands)

    def write_return(self):
        commands = [
            '@LCL',
            'D=M',
            '@R13',
            'M=D',
            '@5',
            'A=D-A',
            'D=M',
            '@R14',
            'M=D',
            '@SP',
            'AM=M-1',
            'D=M',
            '@ARG',
            'A=M',
            'M=D',
            'D=A+1',
            '@SP',
            'M=D',
            '@R13',
            'A=M-1',
            'D=M',
            '@THAT',
            'M=D',
            '@2',
            'D=A',
            '@R13',
            'A=M-D',
            'D=M',
            '@THIS',
            'M=D',
            '@3',
            'D=A',
            '@R13',
            'A=M-D',
            'D=M',
            '@ARG',
            'M=D',
            '@4',
            'D=A',
            '@R13',
            'A=M-D',
            'D=M',
            '@LCL',
            'M=D',
            '@R14',
            'A=M',
            '0;JMP'
        ]
        self.append_code(commands)

    def close_file(self):
        self.file.close()

