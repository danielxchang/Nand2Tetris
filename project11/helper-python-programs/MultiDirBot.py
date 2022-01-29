from CompareBot import compare_files
import sys
import os
from pprint import pprint


def run_tests(test_dir, file_extension):
    compare_directory = '/Users/Daniel/Desktop/nand2tetris/projects/11'
    test_dir = test_dir if test_dir.endswith('/') else test_dir + '/'
    base_path = os.getcwd()
    full_test_path = f"{base_path}/{test_dir}"
    directories = [f"{test_dir}{dir}" for dir in next(os.walk(full_test_path))[1] if not dir.startswith("__")]
    for test_dir in directories:
        print('*' * 100)
        print(test_dir.upper())
        compare_files(compare_directory, base_path, test_dir, file_extension)
        print("\n")

if __name__ == "__main__":
    run_tests(sys.argv[1], sys.argv[2])