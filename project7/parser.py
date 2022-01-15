class Parser:
    arith_logic_commands = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']

    def __init__(self, file_name):
        self.file = open(file_name, 'r')
        self.current_command = None
        self.advance()

    def has_more_commands(self):
        return bool(self.current_command)

    def advance(self):
        self.current_command = self.file.readline().strip()
        while self.current_command and (self.current_command == '\n' or self.current_command[0] == '/'):
            self.current_command = self.file.readline()
        return self.current_command.split("/")[0].strip()

    def close_file(self):
        self.file.close()

    def command_type(self):
        if self.current_command in self.arith_logic_commands:
            return 'C_ARITHMETIC'
        else:
            return 'C_PUSH'

    def arg1(self, cmd_type):
        if cmd_type == 'C_ARITHMETIC':
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self):
        return self.current_command.split()[2]
