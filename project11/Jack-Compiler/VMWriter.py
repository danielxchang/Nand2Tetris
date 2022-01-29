import sys


class VMWriter:
    arith_operators = {
        '+': 'add',
        '-': "sub",
        '*': "call Math.multiply 2",
        '/': "call Math.divide 2",
        '&amp;': 'and',
        '|': 'or',
        '&lt;': 'lt',
        '&gt;': 'gt',
        '=': 'eq'
    }

    unary_operators = {
        '-': "neg",
        '~': "not"
    }

    segments = {
        "var": "local",
        "arg": "argument",
        "constant": "constant",
        "pointer": "pointer",
        "static": "static",
        "temp": "temp",
        "field": "this",
        "that": "that"
    }

    def __init__(self, xml_file):
        self.vm_file = open(xml_file.replace("T.xml", ".vm"), 'w')

    def write_to_file(self, line):
        self.vm_file.write(line + "\n")

    def write_push(self, segment, index):
        self.write_to_file(f"push {self.segments[segment]} {index}")

    def write_pop(self, segment, index):
        self.write_to_file(f"pop {self.segments[segment]} {index}")

    def write_arithmetic(self, command):
        self.write_to_file(self.arith_operators[command])

    def write_unary(self, command):
        self.write_to_file(self.unary_operators[command])

    def write_label(self, label):
        self.write_to_file(f"label {label}")

    def write_goto(self, label):
        self.write_to_file(f"goto {label}")

    def write_if(self, label):
        self.write_to_file(f"if-goto {label}")

    def write_call(self, name, n_args):
        self.write_to_file(f"call {name} {n_args}")

    def write_function(self, name, n_locals):
        self.write_to_file(f"function {name} {n_locals}")

    def write_return(self):
        self.write_to_file("return")

    def close(self):
        self.vm_file.close()


if __name__ == "__main__":
    vm_writer = VMWriter(sys.argv[1])