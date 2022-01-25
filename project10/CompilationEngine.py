import sys


class CompilationEngine:
    def __init__(self, token_xml):
        self.token_file = open(token_xml)


if __name__ == "__main__":
    comp_engine = CompilationEngine(sys.argv[1])