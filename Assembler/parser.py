class Parser:
    def __init__(self, commands):
        self.commands = commands
        self.current_command = 0
        self.n = len(commands)

    def has_more_commands(self):
        return self.current_command < self.n

    def advance_command(self):
        self.current_command += 1

    def get_command_type(self):
        first_char = self.commands[self.current_command][0]
        if first_char == "@":
            return "A"
        elif first_char == "(":
            return "L"
        else:
            return "C"

    def get_symbol(self, command_type):
        if command_type == 'A':
            return self.commands[self.current_command][1:]
        else:
            return self.commands[self.current_command][1:-1]

    def parse_c_command(self):
        command = self.commands[self.current_command]
        if "=" in command:
            dest, rest = command.split("=")
        else:
            dest, rest = "null", command

        if ";" in rest:
            comp, jump = rest.split(";")
        else:
            comp, jump = rest, "null"
        return dest, comp, jump


if __name__ == "__main__":
    parser = Parser(['@2', 'D=A', '@3', 'D+A;JGT', '@0', 'M=D'])
    parser.advance_command()
    command_type = parser.get_command_type()
    if command_type != "C":  # A or L command
        symbol = parser.get_symbol(command_type)
        print(symbol)
    else:  # C command
        dest, comp, jump = parser.parse_c_command()
        print(dest, comp, jump)


