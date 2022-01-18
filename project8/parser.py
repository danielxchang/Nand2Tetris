class Parser:
    command_types = {
        'C_ARITHMETIC': ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'],
        'C_PUSH': ['push', 'pop'],
        'C_BRANCH': ['label', 'goto', 'if-goto'],
        'C_FUNCTION': ['function', 'call', 'return']
    }

    def __init__(self, file_name):
        self.file = open(file_name, 'r')
        self.current_command = None
        self.advance()

    def has_more_commands(self):
        if self.current_command != "":
            return True
        else:
            pos = self.file.tell()
            if self.file.read():
                self.file.seek(pos)
                return True
            else:
                return False

    def advance(self):
        self.current_command = self.file.readline().strip()
        while self.current_command and (self.current_command == '\n' or self.current_command[0] == '/'):
            self.current_command = self.file.readline()
        return self.current_command.split("/")[0].strip()

    def close_file(self):
        self.file.close()

    def command_type(self):
        keyword = self.current_command.split()[0]
        for command_type, commands in self.command_types.items():
            if keyword in commands:
                return command_type

    def arg1(self, cmd_type):
        if cmd_type == 'C_ARITHMETIC':
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self):
        return self.current_command.split()[2]
