class CodeWriter:
    special_symbols = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT'
    }

    def __init__(self, file_name):
        self.file_path = file_name.split('.')[0]
        self.file = open(f"{self.file_path}.asm", mode='w')
        self.file_name = self.file_path.split('/')[-1]
        self.next_number = 0

    def append_code(self, commands):
        for command in commands:
            self.file.write(command + "\n")

    def write_comment(self, command):
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
                commands.append(f'@{self.file_name}.{index}')
                commands.append('M=D')
            elif command == 'push':
                commands.append(f'@{self.file_name}.{index}')
                commands.append('D=M')
                commands.append('@SP')
                commands.append('A=M')
                commands.append('M=D')
                commands.append('@SP')
                commands.append('M=M+1')

        self.append_code(commands)

    def close_file(self):
        self.file.close()

