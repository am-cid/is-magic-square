# is-magic-square
**is-magic-square** is a simple algorithm to determine whether an input magic square through text file is a valid magic square
## Features
1. check whether input magic square is a valid magic square
2. print magic square to console
3. highlight rows/columns/diagonals whose sum is **not equal** to the sum of the majority
    - values part of **column, row, and/or diagonal** whose sum is not equal to the sum of the majority will have a different highlight color
        - **blue** = part of 1 invalid column, row, or diagonal
        - **yellow** = part of any combination of 2 invalid column, row, or diagonal
        - **red** = part of all 3 invalid column, row, and diagonal
        - these can help the user determine which value/s can be changed for the magic square to be valid
4. has simple helpful `[INFO]` `[WARN]` and `[FATAL]` log messages for debugging

## Usage
1. run `python app.py <commands>`
    - example: `python app.py --print --file ./test_data/good_data.txt`
## Commands
1. `--file | -f path/to/text/file`
    - resolves the path for you so current working directory can be just `.` and parent directory can be `..`
    - example: `-f ./test_data/all_unique.txt`
2. `--print | -p`
    - takes no arguments

### Credits
- Masapol, Cid (Leader)
- Benevides, Sean Lester
- Ching, Charles Matthew
- Palileo, Jethro
- Sundiam, Eidrian
- Villanueva, Andre