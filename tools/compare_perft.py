"""Module providing a tool to compare perft results to stockfish."""

import io
import re
import sys


import pexpect


from chess_engine import (
    constants as cs,
    fen_parser as fp,
    move,
    move_gen as mg,
    perft_divide as pd,
)


def run_stockfish(depth, fen, moves):
    """Runs perft on stockfish and stores the output in a dictionary.

    Args:
        depth (str): The depth to run perft at.
        fen (str): The initial board position.
        moves (str): A space-separated list of moves to apply to the starting
            position.

    Returns:
        dict: Associates each move with its number of child nodes, and the
            total number of nodes at the given depth.
    """
    commands = [f"position fen {fen} moves {moves}", f"go perft {depth}", "quit"]
    output = io.BytesIO()

    with pexpect.spawn("stockfish") as p:
        p.logfile_read = output
        p.setecho(False)
        for c in commands:
            p.sendline(c)
        p.expect(pexpect.EOF, timeout=100)

    lines = output.getvalue().decode("UTF-8").split("\r\n")
    output.close()

    results = {}
    i = 0

    while True:
        l = lines[i]
        i += 1

        if l == "":
            return results, int(lines[-3].split(": ")[1])

        if not re.match(r"[a-h][1-8][a-h][1-8][a-z]?: ", l):
            continue

        [mv, n] = l.split(": ")
        results[mv] = int(n)


def compare_engines(depth, fen, moves):
    """Displays the difference in perft results between the engine and stockfish."""
    s_results, s_total = run_stockfish(depth, fen, moves)

    bd = fp.fen_to_board(sys.argv[2])
    if moves:
        for m in moves.split(" "):
            move.make_move_from_string(m, bd)

    f_string = "{:8}{:>16}{:>16}{:>16}"
    print(f_string.format("Move", "Stockfish", cs.NAME, "Difference"))

    moves = set(mg.all_moves(bd))
    total = 0

    for mstr, s_res in s_results.items():
        mv = move.string_to_int(bd, mstr)

        if mv in moves:
            moves.remove(mv)
            pr_type = cs.Q

            if len(mstr) == 5:
                moves.add(mv)
                pr_type = cs.LETTERS.index(mstr[-1]) & 7

            n, total = pd.get_result(bd, mv, depth, total, pr_type=pr_type)
            print(f_string.format(mstr, s_res, n, n - s_res))
        else:
            print(f_string.format(mstr, s_res, "-", -s_res))

    for mv in moves:
        mstr = move.int_to_string(bd, mv)
        if len(mstr) == 5:
            continue

        n, total = pd.get_result(bd, mv, depth, total)
        if n:
            print(f_string.format(mstr, "-", n, n))

    print(f_string.format("Total", s_total, total, total - s_total))


def main():
    """Runs the engines and prints the difference in perft results."""
    depth = int(sys.argv[1])
    fen = sys.argv[2]

    if len(sys.argv) > 3:
        moves = sys.argv[3]
    else:
        moves = ""

    compare_engines(depth, fen, moves)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
