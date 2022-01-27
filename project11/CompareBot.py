import os
import sys


def compare_files(compare_head_dir, test_head_dir, tail_dir, extension):
    tail_dir = tail_dir if tail_dir[-1] == '/' else tail_dir + '/'
    test_path = f"{test_head_dir}/{tail_dir}"
    compare_path = f"{compare_head_dir}/{tail_dir}"

    for file in os.listdir(test_path):
        if file.split('.')[-1] == extension:
            print(f"Comparing {file}...")
            os.system(f'TextComparer.sh "{test_path + file}" "{compare_path + file}"')


if __name__ == "__main__":
    compare_directory = '/Users/Daniel/Desktop/nand2tetris/projects/10'
    test_directory = os.getcwd()
    compare_files(compare_directory, test_directory, sys.argv[1], sys.argv[2])