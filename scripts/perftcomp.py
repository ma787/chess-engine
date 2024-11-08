"""Module providing a tool to compare perft results to stockfish."""

import sys


import pexpect
import tabulate


from chess_engine import board, move, perft_divide as pd


def parse_stockfish_output():
    """Reads stockfish perft output from a file.

    Returns:
        tuple: A dict associating each move with its number of child nodes,
            and the total number of nodes at the given depth (int).
    """
    with open("scripts/stockfish_output.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
        results = {}

        i = 5

        while True:
            l = lines[i]
            if l == "\n":
                return results, int(lines[-2][16:])
            [mv, n] = lines[i].split(": ")
            results[mv] = int(n)
            i += 1


def parse_engine_output():
    """Reads engine perft output from a file.

    Returns:
        tuple: A dict associating each move with its number of child nodes,
            and the total number of nodes at the given depth (int).
    """
    with open("scripts/engine_output.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
        results = {}
        i = 0

        while True:
            l = lines[i]
            if l == "\n":
                return results, int(lines[-1])
            [mv, n] = l.split(" ")
            results[mv] = int(n)
            i += 1


def run_engines(depth, fen, moves):
    """Runs perft on the engine and stockfish, saving the outputs to files.

    Args:
        depth (str): The depth to run perft at.
        fen (str): The initial board position.
        moves (str): A space-separated list of moves to apply to the starting
            position.
    """
    commands = [f"position fen {fen} moves {moves}", f"go perft {depth}", "quit"]

    with open("scripts/stockfish_output.txt", "wb") as f:
        with pexpect.spawn("stockfish") as p:
            p.logfile_read = f
            p.setecho(False)
            for c in commands:
                p.sendline(c)
            p.expect(pexpect.EOF)

    with open("scripts/engine_output.txt", "w", encoding="UTF-8") as g:
        bd = board.Board.of_fen(sys.argv[2])
        if moves:
            for m in moves.split(" "):
                move.make_move_from_string(m, bd)
        pd.divide(bd, depth, stdout=g)


def print_diff():
    """Displays the difference in perft results between the engine and stockfish."""
    s_results, s_nodes = parse_stockfish_output()
    test_results, test_nodes = parse_engine_output()
    overall_results = []

    for mv, s_res in s_results.items():
        if mv in test_results:
            t_res = test_results[mv]
            diff = t_res - s_res
        else:
            t_res = "-"
            diff = -s_res
        overall_results.append([mv, s_res, t_res, diff])

    extra = [m for m in test_results if m not in s_results]

    for mv in extra:
        overall_results.append([mv, "-", test_results[mv], test_results[mv]])

    overall_results.append(["Total", s_nodes, test_nodes, test_nodes - s_nodes])

    headers = ["Move", "Stockfish", "My Engine", "Difference"]

    print(tabulate.tabulate(overall_results, headers=headers, tablefmt="plain"))


def main():
    """Runs the engines and prints the difference in perft results."""
    depth = int(sys.argv[1])
    fen = sys.argv[2]

    if len(sys.argv) > 3:
        moves = sys.argv[3]
    else:
        moves = ""

    run_engines(depth, fen, moves)
    print_diff()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
