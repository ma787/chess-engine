# Python Chess Engine
A chess engine and board representation written in Python. Supplied with a text client
that allows playing against the engine or another user.

## Requirements
In order to use the perft script, the modules **pexpect** and **tabulate** must be installed.
Also, **stockfish** must be installed and on your PATH.

## Installation
The engine can be installed by entering the project directory and running this command:

`pip install .`

## Usage

### Text Client
`python -m chess_engine.main`

Moves are entered in the format **[SOURCE][TARGET][PROMOTION]**, e.g., e1c1, g8h6, e7e8q.

### Testing
To run the test suite:

`python -m unittest`

To run the perft comparison script:

`python ./scripts/perftcomp.py DEPTH FEN [MOVES]`

**DEPTH:** The depth to report perft results for.

**FEN:** The FEN-string of the starting board position.

**MOVES:** An optional space separated list of moves to apply to the starting position. The format
of these moves is the same as above.

The script prints a table comparing the engine perft results to stockfish.
