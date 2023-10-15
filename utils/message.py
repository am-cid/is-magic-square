class Log:
    'A class for formatting log messages with ANSI colors'
    _default = "\033[0m"
    _yellow = "\033[93m"
    _red = "\033[91m"

    @classmethod
    def info(cls, text: str, end: str="\n") -> str:
        """
        [INFO]
        these typically provide non-critical information or updates about the program's execution
        they are meant to inform without indicating any issues or errors
        """
        print(f"[INFO] {text}", end=end)
    
    @classmethod
    def warn(cls, text: str, end: str="\n") -> str:
        """
        [WARN]
        these are used to alert users/developers about potential issues in the program.
        while not critical errors, they suggest a need for attention or corrective action.
        """
        # ANSI escape code for yellow
        text_color = cls._yellow
        print(f"{text_color}[WARN]{cls._default} {text}", end=end)
    
    @classmethod
    def fatal(cls, text: str, end: str="\n") -> str:
        """
        [FATAL]
        these indicate severe issues that prevent the program from functioning correctly.
        this may or may not lead to the termination of the program, depending on the developer.
        """
        # ANSI escape code for red
        text_color = cls._red
        print(f"{text_color}[FATAL]{cls._default} {text}", end=end)