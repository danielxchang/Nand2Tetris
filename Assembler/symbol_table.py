class SymbolTable:
    def __init__(self, lines):
        self.table = {}
        self.construct_initial_table()
        self.check_for_labels(lines)
        self.next_available_address = 16

    def construct_initial_table(self):
        predefined_symbols = ['SP', 'LCL', 'ARG', 'THIS', 'THAT']
        for i, symbol in enumerate(predefined_symbols):
            self.table[symbol] = i

        for i in range(16):
            self.table[f'R{i}'] = i

        self.table['SCREEN'] = 16384
        self.table['KBD'] = 24576

    def check_for_labels(self, commands):
        number_of_labels = 0
        for i, command in enumerate(commands):
            if command[0] == "(":
                self.table[command[1:-1]] = i - number_of_labels
                number_of_labels += 1

    def check_symbol(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if symbol not in self.table:
                self.table[symbol] = self.next_available_address
                self.next_available_address += 1
            return self.table[symbol]
