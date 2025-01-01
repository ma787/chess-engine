"""Module implementing the UCI protocol."""

import sys


from chess_engine import (
    board,
    constants as cs,
    engine,
    fen_parser as fp,
    move,
    perft_divide as pd,
)


def position(bd, args):
    """Updates the board to match a FEN string."""
    if len(args) == 0:
        return bd

    next_arg = 0

    if args[0] == "startpos":
        bd = board.Board()
        next_arg = 1
    elif args[0] == "fen":
        try:
            bd = fp.fen_to_board(" ".join(args[1:7]))
            next_arg = 7
        except (IndexError, ValueError):
            return bd

    if not next_arg or len(args) < next_arg + 2 or args[next_arg] != "moves":
        return bd

    for mv in args[next_arg + 1 :]:
        move.make_move_from_string(mv, bd)

    return bd


def search(bd, t_table, args):
    """Performs a search according to the specified conditions."""
    options = {}
    i = 0
    while i < len(args):
        try:
            options[args[i]] = int(args[i + 1])
            i += 2
        except (IndexError, ValueError):
            return t_table

    depth = options.get("depth", 100)

    search_time = 0

    if "movetime" in options:
        search_time = options["movetime"]
    elif "infinite" in options:
        search_time = 10000000  # TODO: get rid of time cap here
    else:
        side = "b" if bd.black else "w"
        search_time = options.get(side + "time", search_time) / 20
        search_time += options.get(side + "inc", 0) / 2

    print(f"bestmove {engine.find_move(bd, search_time / 1000, depth, t_table)}")
    return t_table


def main():
    """Receives inputs from stdin and calls the required functions."""
    bd = board.Board()
    t_table = {}

    while True:
        line = input()

        if line:
            info = line.split(" ")
            command = info[0]

            match command:
                case "isready":
                    print("readyok")
                case "go":
                    if info[1] == "perft" and len(info) == 3:
                        pd.divide(bd, int(info[2]))
                    else:
                        t_table = search(bd, t_table, info[1:])
                case "position":
                    bd = position(bd, info[1:])
                case "quit":
                    sys.exit()
                case "uci":
                    print(f"id name {cs.NAME}")
                    print(f"id author {cs.AUTHOR}")
                    print("uciok")
                case "ucinewgame":
                    t_table = {}


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
