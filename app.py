from pathlib import Path
from sys import argv

from algorithm.magic_square import Magic_Square
from utils.message import Log

class Args:
    'class that handles parsing and validating arguments'

    def __init__(self, args: list[str]):
        # default None containers for return values
        self._raw_args = args
        self._validate_raw_args()

        # default None containers before parsing/cleaning for validation purposes
        self._args = {
            "file_path": None,
            "print_command": None,
            "size": None,
        }
        self._parse_args()
        self._validate_args()
    
    @property
    def args(self) -> dict[str : str|int|None]:
        'returns dictionary of validated command line arguments'
        return self._args

    def _validate_raw_args(self):
        'simple validation if argv passed is a list of strings'
        # check if list
        if not isinstance(self._raw_args, list):
            Log.fatal("Please pass list of arguments (strings)")
            exit(1)
        # check if list of strings
        if not all(isinstance(arg, str) for arg in self._raw_args):
            Log.fatal("Please pass list of arguments (all must be strings)")
            exit(1)

    def _parse_args(self):
        argv_iter = iter(self._raw_args)

        for arg in argv_iter:
            # put commands without mandatory arg with continue and before doing next(iter, None) so it doesn't mess up the order
            if arg in ["--print", "-p"]:
                # catch situations where there are multiple [--print -p]
                if self._args["print_command"] is not None:
                    Log.fatal("There are multiple [--print -p] commands! Please only put one")
                    exit(1)

                self._args.update({"print_command":True})
                continue

            # put commands with mandatory arg after doing next(iter, None) so it doesn't mess up the order
            # put None as default value if there's no next iteration
            value = next(argv_iter, None)

            if arg in ["--file", "-f"]:
                # catch situations where there are multiple [--file -f]
                if self._args["file_path"] is not None:
                    Log.fatal("There are multiple [--file -f] commands! Please only put one")
                    exit(1)
                # if there is no argument after the file_path command
                if value is None:
                    Log.fatal(f"Please input an argument after '--file' or '-f'")
                    exit(1)

                file = Path(value).resolve()
                if file.is_file() and file.suffix == '.txt':
                    self._args.update({"file_path":file})

                else:
                    Log.fatal(f"'{file.as_posix()}' is not a valid path to a text file")
                    exit(1)
            
            elif arg in ["--size", "-s"]:
                # catch situations where there are multiple [--size -s]
                if self._args["size"] is not None:
                    Log.fatal("There are multiple [--size -s] commands! Please only put one")
                    exit(1)
                # if there is no argument after the size command
                if value is None:
                    Log.fatal(f"Please input an argument after '--size' or '-s'")
                    exit(1)

                if value.isdecimal():
                    self._args.update({"size":int(value)})
                
                else:
                    Log.fatal(f"'{value}' is not a valid size argument. Please avoid negative ('-') and decimal points ('.')")
                    exit(1)

            else:
                Log.fatal(f"'{arg}' is not a valid argument")
                exit(1)

    def _validate_args(self):
        """
        validates and cleans dictionary of args
        validations:
            - "file_path" and "size" cannot be coexist as arguments, only one should be passed
        """
        # check if there are no arguments passed (all args are None)
        if (not any(arg for arg in self._args.values())):
            # if no args are passed, put default arguments
            self._args.update({
                "file_path": Path("./test_data/bad_data.txt").resolve(),
                "print_command": True
                })
        
        # only one of the two arguments must exist
        elif self._args["file_path"] and self._args["size"]:
            Log.fatal("Either pass an argument for [--file -f] or [--size -s], not both!")
            exit(1)

if __name__ == "__main__":
    test = Args(argv[1:])
    magic = Magic_Square(test.args)

    if test.args["print_command"]:
        magic.print_magic_square()