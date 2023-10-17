# is-magic-square
**is-magic-square** is a simple algorithm to determine whether an input magic square through text file is a valid magic square. This can also generate a magic square and export it to a text file.

### example text file:
```
8 1 6
3 5 7
4 9 2
```
- *values are separated by whitespace/s*

example magic square input text files can be found at `./test_data/`
## Features
1. check whether input magic square is a valid magic square
2. warns the user if the magic square input is not an **odd sided square** but continues execution
3. print magic square to console
4. highlight rows/columns/diagonals whose sum is **not equal** to the sum of the majority (invalid)
5. has simple helpful `[INFO]` `[WARN]` and `[FATAL]` log logs for debugging
6. generate odd sided magic square, exports it to text file, and processes that text file as if it was an input magic square

*for more information please see [The Wiki](https://github.com/am-cid/is-magic-square/wiki)*

## Usage
1. run `python app.py <commands>`
    - example: `python app.py --print --file ./test_data/good_data.txt`
## Commands
1. `--file | -f path/to/text/file`
    - resolves the path for you so current working directory can be just `.`, parent directory can be `..`, grandparent directory can be `../..`, etc
    - example: `-f ./test_data/all_unique.txt`
    - default file path if none is inputted is `./test_data/bad_data.txt`
2. `--print | -p`
    - takes no arguments
    - default behavior if this command is not indicated is the magic square will not be printed to console
        - `[INFO]` `[WARN]` and `[FATAL]` logs will still be printed though
3. `--size | -s number`
    - accepts only positive odd numbers; minimum of 3

### Credits
- Masapol, Cid (Leader)
- Benevides, Sean Lester
- Ching, Charles Matthew
- Palileo, Jethro
- Sundiam, Eidrian
- Villanueva, Andre
