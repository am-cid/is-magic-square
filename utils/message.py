class Log:
    'A class for formatting log messages with ANSI colors'
    _default = "\033[0m"

    @classmethod
    def info(self):
        """
        [INFO]
        these typically provide non-critical information or updates about the program's execution
        they are meant to inform without indicating any issues or errors
        """
        return f"[INFO]"
    
    @classmethod
    def warn(cls):
        """
        [WARN]
        these are used to alert users/developers about potential issues in the program.
        while not critical errors, they suggest a need for attention or corrective action.
        """
        # ANSI escape code for yellow
        yellow = "\033[93m"
        return f"{yellow}[WARN]{cls._default}"
    
    @classmethod
    def fatal(cls):
        """
        [FATAL]
        these indicate severe issues that prevent the program from functioning correctly.
        this may or may not lead to the termination of the program, depending on the developer.
        """
        # ANSI escape code for red
        red = "\033[91m"
        return f"{red}[FATAL]{cls._default}"