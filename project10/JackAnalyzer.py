import sys
import os
from Tokenizer import Tokenizer


# Gathers jack file(s) from program_input parameter and returns a list of jack files to be tokenized
def retrieve_jack_files(program_input):
    jack_files = []

    if os.path.isdir(program_input):  # if program_input is a directory
        directory_path = os.path.dirname(program_input if program_input[-1] == "/" else program_input + "/")

        for file in os.listdir(program_input):
            if file.split('.')[-1] == 'jack':
                jack_files.append(f"{directory_path}/{file}")

    else: # if program_input is a file
        jack_files.append(program_input)

    return jack_files


def run_jack_analyzer(jack_files):
    for file in jack_files:
        tokenizer = Tokenizer(file)
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            tokens = tokenizer.token_type()
            for token_tuple in tokens:
                token = tokenizer.get_token_string(token_tuple)
                tokenizer.write_to_xml(token)
        tokenizer.close_xml_file()



if __name__ == "__main__":
    run_jack_analyzer(retrieve_jack_files(sys.argv[1]))