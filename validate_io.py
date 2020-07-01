from pathlib import Path
import argparse

### SUB FUNCTIONS

# check existence of file given path object
def file_exists(path):
    return path.exists()

# check validity of file for file type
def file_is_valid(path):
    return True
    # TODO: add detailed validation of specific file types

### MAIN FUNCTION

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of file to validate", type=str)
    parser.add_argument("-e", "--extension", help="get file extension", action="store_true")
    args = parser.parse_args()

    path = Path(args.path)
    file_ext = path.suffix

    if not file_exists(path):
        print("Invalid: File does not exist")
    elif not file_ext:
        print("Invalid: File does not have extension")
    elif not file_is_valid(path):
        print("Invalid: File is not a valid " + file_ext)
    else:
        if args.extension:
            print(file_ext)
        else:
            print("Valid")

if __name__ == '__main__':
    main()