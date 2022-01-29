import sys
import re
import os


class Tokenizer:
    special_symbols = {
        "<": '&lt;',
        ">": '&gt;',
        '"': '&quot;',
        "&": '&amp;',
    }

    keywords = [
        'class',
        'constructor',
        'function',
        'method',
        'field',
        'static',
        'var',
        'int',
        'char',
        'boolean',
        'void',
        'true',
        'false',
        'null',
        'this',
        'let',
        'do',
        'if',
        'else',
        'while',
        'return'
    ]
    symbols = [
        '{',
        '}',
        '(',
        ')',
        '[',
        ']',
        '.',
        ',',
        ';',
        '+',
        '-',
        '*',
        '/',
        '&',
        '|',
        '<',
        '>',
        '=',
        '~'
    ]
    lexical_categories = {
        'KEYWORD': 'keyword',
        'SYMBOL': 'symbol',
        'INT_CONST': 'integerConstant',
        'STRING_CONST': 'stringConstant',
        'IDENTIFIER': 'identifier'
    }

    def __init__(self, jack_file):
        self.tokens_line = []
        with open(jack_file) as file:
            for line in file.readlines():
                if not self.ignore_line(line.strip()):
                    formatted_line = line.split("//")[0].strip()
                    if formatted_line:

                        if self.tokens_line and self.tokens_line[-1][-1] == ",":
                            self.tokens_line[-1] += f" {formatted_line}"
                        else:
                            self.tokens_line.append(formatted_line)
        self.class_name = os.path.basename(jack_file).split('.')[0]
        self.xml_file_name = f"{jack_file.split('.')[0]}T.xml"
        self.xml_file = open(self.xml_file_name, 'w')
        self.write_to_xml("<tokens>")
        self.current_token = None

    @staticmethod
    def ignore_line(line):
        for symbol in ["//", "/*", "*"]:
            if line.startswith(symbol) or line == "\n":
                return True
        return False

    def has_more_tokens(self):
        return self.tokens_line

    def advance(self):
        self.current_token = self.tokens_line.pop(0)

    def token_type(self):
        elem = ""
        i = 0
        tokens = []
        while i < len(self.current_token):
            elem += self.current_token[i]  # Add another character to current elem string

            # Check if found a valid lexical element
            if elem.startswith(" "):
                elem = ""
            elif elem in self.keywords and \
                    (i == len(self.current_token) - 1 or
                     self.current_token[i + 1] in self.symbols or
                     self.current_token[i + 1] == " "):
                tokens.append((elem, "KEYWORD"))
                elem = ""
            elif elem in self.symbols:
                tokens.append((self.special_symbols[elem] if elem in self.special_symbols else elem, "SYMBOL"))
                elem = ""
            elif elem.isnumeric() and (i == len(self.current_token) - 1 or not self.current_token[i + 1].isnumeric()):
                tokens.append((elem, "INT_CONST"))
                elem = ""
            elif len(elem) >= 2 and self.current_token[i] == '"' and elem.startswith('"') and "\n" not in elem[1:] and '"' not in elem[1:-1]:
                tokens.append((elem, "STRING_CONST"))
                elem = ""
            elif re.search("^[a-zA-Z_]\w*$", elem) and (i == len(self.current_token) - 1 or not re.search("\w", self.current_token[i + 1])):
                tokens.append((elem, "IDENTIFIER"))
                elem = ""

            i += 1
        return tokens

    def get_token_string(self, token_tuple, symbol_string=None):
        elem, cat = token_tuple[0], self.lexical_categories[token_tuple[1]]
        return f"<{cat}> {elem} </{cat}>" if not symbol_string else f"<{cat}> {symbol_string} </{cat}>"

    def write_to_xml(self, token):
        self.xml_file.write(token + "\n")

    def close_xml_file(self):
        self.xml_file.write("</tokens>")
        self.xml_file.close()


if __name__ == "__main__":
    tokenizer = Tokenizer(sys.argv[1])
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        tokens = tokenizer.token_type()
        for token_pair in tokens:
            token = tokenizer.get_token_string(token_pair)
            tokenizer.write_to_xml(token)
    tokenizer.close_xml_file()
