from pathlib import Path
from sys import argv
from algorithm.magic_square import Magic_Square

def parse_args(argv: list[str] = None) -> tuple[Path, bool]:
    """
    return:
    1. Path to your text file containing the magic square input
    2. whether to print the magic square or not
    valid arguments: (--file, -f), (--print, -p)
    """
    # default containers for return values
    file_path: Path = None
    print_command = False

    # check if list
    if not isinstance(argv, list):
        print("Please pass list of arguments (strings)")
    # check if list of strings
    if not all(isinstance(arg, str) for arg in argv):
        raise TypeError("Please pass list of arguments (all must be strings)")        
    
    # create iter object for the for loop
    # so we can use next() which can get the value of the next iteration
    argv_iter = iter(argv)

    for arg in argv_iter:
        # put commands without mandatory arg with continue and before ddoing next(iter, None) so it doesn't mess up the order
        if arg in ["--print", "-p"]:
            print_command = True
            continue

        # put commands with mandatory arg after doing next(iter, None) so it doesn't mess up the order
        # put None as default value if there's no next iteration
        value = next(argv_iter, None)

        if arg in ["--file", "-f"]:
            file = Path(value).resolve()
            if file.is_file() and file.suffix == '.txt':
                file_path = file

            else:
                print(f"{Log.fatal()} '{file.as_posix()}' is not a valid path to a text file")
                print("exiting...")
                exit(1)          
        else:
            print(f"{Log.fatal()} '{arg}' is not a valid argument")
            print("exiting...")
            exit(1)

    # if no custom file path is inputted, put the default test data file
    file_path = file_path if file_path else Path("./test_data/bad_data.txt").resolve()
    return file_path, print_command

if __name__ == "__main__":
    text_file_path, print_command = parse_args(argv[1:])
    magic = Magic_Square(text_file_path)

    if print_command:
        magic.print_magic_square()