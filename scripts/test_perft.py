"""Module providing functions to test engine against standard perft results."""

import datetime
import sys
import time


from chess_engine import fen_parser as fp, perft_divide as pd


def parse_results_file(file_path):
    """Extracts perft results from file."""
    results = {}

    with open(file_path, "r", encoding="UTF-8") as f:
        lines = f.readlines()

        for line in lines:
            if line == "/n":
                break

            info = line.split(";")
            results[info[0].strip()] = [
                int(info[i].split(" ")[1]) for i in range(1, len(info))
            ]

    return results


def run_tests(results, depth_lim):
    """Compares the engine's perft results to a provided set of results."""
    start = time.time()

    f_string = "{:12}{:72}"
    print(f"{"":12}{"FEN":65}{1:8}{2:8}{3:8}{4:8}{5:8}{6:8}{"Time Elapsed":>19}")
    total = len(results)
    n = 1

    for fen, depths in results.items():
        bd = fp.fen_to_board(fen)
        lim = min(len(depths) + 1, depth_lim + 1)

        print(f_string.format(f"({n}/{total})", fen), end="", flush=True)

        for i in range(1, lim):
            res = str(pd.perft(bd, i) - depths[i - 1])
            print(f"{res:8}", end="", flush=True)

        for i in range(lim, 7):
            print(f"{'-':8}", end="")

        print(f"{datetime.timedelta(seconds=time.time() - start)}\n")
        n += 1

    end = time.time()
    print(f"\nTime elapsed: {datetime.timedelta(seconds=end - start)}")


def main():
    """Runs the comparison function."""
    try:
        depth = int(sys.argv[1])
        if depth < 0:
            depth = 6
    except ValueError:
        depth = 6

    run_tests(parse_results_file(sys.argv[2]), depth)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
