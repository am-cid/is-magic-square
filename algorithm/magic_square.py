from pathlib import Path
from collections import Counter

from utils.message import Log

class Magic_Square:
    """
    This class allows you to read and process magic squares from a text file, check if they are valid magic squares, and print them with color-coded elements.

    Magic squares are square grids filled with distinct numbers in such a way that the sums of the numbers in each row, column, and diagonal (the 2 main ones) are the same.

    This will take in any size square but will warn users if the size of the sides of the square is not odd (this will not affect whether the magic square is valid or not)
    """
    def __init__(self, text_file: Path):
        if not text_file.exists():
            Log.fatal(f"File not found: '{text_file}'")
            print("exiting...")
            exit(1)

        # read_file modifies _lines
        self._lines: list[list[int]]
        self._read_file(text_file)

        # compute sums modifies _sums and _is_magic_square
        self._sums: dict[str:int]
        self._is_magic_square: bool
        self._compute_sums()
        self._define_text_color()
    
    @property
    def is_magic_square(self) -> bool:
        'returns true if the magic square instance is a magic square'
        return self._is_magic_square
    
    @property
    def row_count(self) -> int:
        'returns the number of rows'
        return len(self._lines)

    @property
    def column_count(self) -> int:
        'returns the number of columns'
        return len(self._lines[0])

    @property
    def diagonal_count(self) -> int:
        "returns the number of diagonals (always 2); why are you even calling this? I'm just clarifying it for you that there are only 2 diagonals (main diagonals)"
        return 2

    @property
    def total_counts(self)-> int:
        'returns the total count of rows, columns, and main 2 diagonals'
        return self.row_count + self.column_count + 2
    
    @property
    def row_sums(self) -> list[int]:
        """
        returns the sums for each row; top to bottom
        implied order: row_1, row_2, ..., row_n
        """
        _row_sums = [value for key, value in self._sums.items() if key.startswith("row")]
        return _row_sums
    
    @property
    def column_sums(self) -> list[int]:
        """
        returns the sums for each column; left to right
        implied order: row_1, row_2, ..., column_n
        """
        _column_sums = [value for key, value in self._sums.items() if key.startswith("column")]
        return _column_sums
    
    @property
    def diagonal_sums(self) -> list[int]:
        """
        returns the sums for both diagonals
        implied order: diagonal_1 '/', and diagonal_2 '\\'
        """
        _diagonal_sums = [value for key, value in self._sums.items() if key.startswith("diagonal")]
        return _diagonal_sums

    @property
    def sums(self) -> list[int]:
        """
        returns all the sums for each row, column, and diagonal in a list
        implied order: row_1, row_2, ..., row_n, column_1, column_2, ..., column_n, diagonal_1, and diagonal_2
        """
        return self.row_sums + self.column_sums + self.diagonal_sums
    
    def _read_file(self, text_file: Path):
        """
        takes a file path to a magic square txt file and computes the rows and columns based on data read from file
        input: Path to txt file
        modifies: self._lines
        """
        with open(text_file, "r") as file:
            # outer comprehension outputs string for each line in the file
            # inner comprehension takes that ouputted string and turns it into a list by line.strip().split()
            # for each string that was split in this new list, turn those strings into ints
            lines = [[int(value) for value in line.strip().split()] for line in file]

        self._lines = lines

        row_count = len(self._lines)
        column_count = len(self._lines[0])

        if row_count % 2 != 1 or column_count % 2 != 1:
            Log.warn(f"'{text_file.name}' is not an odd sided square ({row_count}x{column_count})")
        elif row_count != column_count:
            Log.fatal(f"'{text_file.name}' contains a {row_count}x{column_count} shape which is not a square")
            print("exiting...")
            exit(1)

    def _compute_sums(self):
        """
        compute the sum of each row, column, and diagonal of a 2d list
        input: list of list of ints where each list is a row
        return: dict of str:int where str is the sum_name (row_1, column_2, etc) and int is the sum
                bool where it's true if every sum is the same (a magic square) and false if it's not
        """
        row_column_count = len(self._lines)
        sums = {}

        for i, row in enumerate(self._lines):
            row_sum = sum(row)
            column_sum = sum([row[i] for row in self._lines])

            self._is_magic_square = True
            # check against prev row
            if i > 1 and row_sum != sum(self._lines[i-1]):
                self._is_magic_square = False
            
            # check against prev column
            elif i > 1 and column_sum != sum([row[i-1] for row in self._lines]):
                self._is_magic_square = False
            
            sums.update({f"row_{i+1}": row_sum})
            sums.update({f"column_{i+1}": column_sum})

            # only add 2 diagonals
            if i == row_column_count - 1: # final iteration
                # first diagonal: /
                # row[i] because first row element must be the first, second row element must be the second, etc...
                diagonal_1_sum = {f"diagonal_1": sum([row[len(row)-1-j] for j, row in enumerate(self._lines)])}
                sums.update(diagonal_1_sum)

                # second diagonal: \
                # row[ (len(row)-1) - i ] because first row element must be the last, second row element must be the second from the last, etc...
                diagonal_2_sum = {f"diagonal_2": sum([row[j] for j, row in enumerate(self._lines)])}
                sums.update(diagonal_2_sum)

        self._sums = sums

    def _define_text_color(self):
        """
        gives each value in the magic square a text color
        white: default
        red: the row's OR column's sum is not equal to the majority's sum
        blue: value is part of both a row AND a column whose sum is not equal to the majority's sum
        """
        # counter returns a dictionary-like string representation of {value:int} where value is the value in my iterable and int is the number of times it occured
        # need to turn the default Counter string representation to dict
        sum_counter = Counter(self.sums).most_common()
        majority_sum, majority_sum_count = sum_counter[0]

        if len(set(self.sums)) == self.total_counts:
            Log.fatal("Interesting! All your sums are unique values. You basically achieved an anti-magic square. Congrats I guess")
            majority_sum = None
        
        elif not majority_sum_count > self.total_counts/2:
            Log.fatal(f"No majority (>50%) sum found. The majority sum found is '{majority_sum}' which is only {(majority_sum_count/self.total_counts)*100}% ({majority_sum_count}) of the total count of sums present ({self.total_counts})")

        # create a list that's exactly the same size as the magic square being processed but with all values as '0'
        lines_color = [[0]*self.column_count for _ in range(self.row_count)]

        # add +1 a row when the corresponding sum != majority sum
        for i, row_sum in enumerate(self.row_sums):
            lines_color[i] = [x+1 if row_sum != majority_sum else x for x in lines_color[i]]
        
        # add +1 a column when the corresponding sum != majority sum
        for i, column_sum in enumerate(self.column_sums):
            if column_sum != majority_sum:
                for line in lines_color:
                    line[i] += 1

        # add +1 a diagonal when the corresponding sum != majority sum
        diagonal_1_sum, diagonal_2_sum = self.diagonal_sums
        if diagonal_1_sum != majority_sum:
            for i, _ in enumerate(lines_color):
                lines_color[i][(len(lines_color)-1)-i] += 1

        if diagonal_2_sum != majority_sum:
            for i, _ in enumerate(lines_color):
                lines_color[i][i] += 1

        """ replace values in lines_color with ANSI escape code (for text color)
        if 0 (value isn't part of a row/column/diagonal whose sum != majority sum), default color
        if 1 (value is part of ONE of either row/column/diagonal whose sum != majority sum), blue
        if 2 (value is part of TWO of any combination of row/column/diagonal whose sum != majority sum), yellow
        if 3 (value is part of THREE OR MORE of any combination of row/column/diagonal whose sum != majority sum), red
        """
        blue = "\033[94m"
        yellow = "\033[93m"
        red = "\033[91m"
        default_color = "\033[0m"

        self._text_color = [
            [
                blue if val == 1
                else yellow if val == 2
                else red if val >= 3
                else default_color
                for val in line
            ]
            for line in lines_color
        ]
        self._majority_sum = majority_sum

    def print_magic_square(self):
        """
        prints the magic square with borders
        sums are printed outside the borders
        """
        # ANSI text color codes
        blue = "\033[94m"
        default_color = "\033[0m" # default value (acting as reset)
        text_color = default_color
        padding = 10

        if self.is_magic_square:
            Log.info("valid magic square! all sums are equal\n")
        else:
            Log.fatal(f"invalid magic square!", end=" ")
            if self._majority_sum:
                print(f"some sums are not equal to '{self._majority_sum}'\n")
            else:
                print(r"all values are unique lol", end="\n\n")

        # print column sums first (on top of border)
        for i in range(len(self._lines[0])):
            if self.column_sums[i] != self._majority_sum:
                text_color = blue

            column_label = f"c{i+1}: {self._sums[f'column_{i+1}']}"
            print(f"{text_color}{column_label:^{padding+1}}{default_color}", end="")
            text_color = default_color

        # diagonal_1: /
        if self.diagonal_sums[0] != self._majority_sum:
            text_color = blue

        diagonal_1_label = f"d1: {self._sums['diagonal_1']}"
        print(f"{text_color}{diagonal_1_label:>{padding}}{default_color}")
        text_color = default_color

        # print top border
        for _ in range(len(self._lines[0])):
            print(" ", end="")
            print(f"{'_'*padding}", end="")
        print()
        
        # print inner borders with values
        for i, (line, colors) in enumerate(zip(self._lines, self._text_color)):
            # inner border
            print(f"{'|'}", end="")
            for _ in line:
                print(f"{' ':^{padding}}", end="")
                print(f"{'|'}", end="")
            print()

            # values
            print(f"{'|'}", end="")
            for value, color in zip(line, colors):
                print(f"{color}{value:^{padding}}{default_color}", end="|")

            # row sums
            if self.row_sums[i] != self._majority_sum:
                text_color = blue

            row_label = f"r{i+1}: {self._sums[f'row_{i+1}']}"
            print(f"{text_color}{row_label:>{padding+1}}{default_color}", end="")
            text_color = default_color
            print()

            # low border
            for _ in line:
                print(f"|{'_'*padding}", end="")
            print("|")
        print()

        # diagonal_2: \
        # empty space
        for _ in range(len(self._lines[0])):
            print(f"{'':^{padding+1}}", end="")

        # the actual diagonal label with sum
        if self.diagonal_sums[1] != self._majority_sum:
            text_color = blue
        diagonal_2_label = f"d2: {self._sums['diagonal_2']}"
        print(f"{text_color}{diagonal_2_label:>{padding}}{default_color}")
        text_color = default_color