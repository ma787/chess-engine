# Python Chess Engine
A chess engine and board representation written in Python. Supplied with a text client
that allows playing against the engine or another user.

## Installation and Usage
After downloading the project directory, navigate to it in a terminal and enter the following:

`pip install .`

After installing, run the following command to start the text client:

`python -m chess_engine.main`

Moves are entered in the format (source|target|promotion), e.g., e1c1, g8h6, e7e8q.

To run the test suite, navigate to the project directory and run the following command:

`python -m unittest`
