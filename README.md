# Aether Chess Engine
A UCI chess engine written in Python.

## Requirements
In order to use the *compare_perft* script, **pexpect** must be installed on Linux/WSL.
**stockfish** must be installed and on your PATH.

## Installation
The engine can be installed by entering the project directory and running this command:

`pip install .`

## Usage
To run the engine in UCI mode:

`python tools/uci.py`

Only a subset of the UCI protocol is currently supported. Features such as pondering and configurable options are not available.

### Testing
To run the test suite:

`python -m unittest`

### Tools

### compare_perft
Prints a table comparing the engine perft results to stockfish.

`python ./scripts/compare_perft.py DEPTH FEN [MOVES]`

**DEPTH:** The depth to report perft results for.

**FEN:** The FEN-string of the starting board position.

**MOVES:** An optional space separated list of moves to apply to the starting position. The format of these moves is the same as above.

### run_perft
Runs perft to a specified depth and prints the result, time taken and NPS.

`python ./scripts/run_perft.py DEPTH [FEN]`

**DEPTH:** The depth to report perft results for.

**FEN:** The FEN-string of the starting board position. Defaults to the starting position.

### test_perft
Prints a table comparing the engine's perft results to those found in an EPD file.

`python ./scripts/test_perft.py DEPTH FILE_PATH`

**DEPTH:** The maximum depth to report perft results for.

**FILE_PATH:** The path to the EPD file containing the results. See the *perft_results* directory for some example files.