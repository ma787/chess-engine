"""Module providing functions to test engine against standard perft results."""

import datetime
import sys
import time


import tabulate


from chess_engine import fen_parser as fp, perft_divide as pd


def parse_results_file():
    """Extracts perft results from file."""
    results = {}

    with open("scripts/perftsuite.epd", "r", encoding="UTF-8") as f:
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
    overall_results = []
    start = time.time()

    for fen, depths in results.items():
        bd = fp.fen_to_board(fen)
        perft_res = [fen]
        for i in range(1, min(len(depths) + 1, depth_lim + 1)):
            perft_res.append(pd.perft(bd, i) - depths[i - 1])
        while len(perft_res) < 7:
            perft_res.append("-")
        overall_results.append(perft_res)

    end = time.time()
    headers = ["FEN", "1", "2", "3", "4", "5", "6"]
    print(tabulate.tabulate(overall_results, headers=headers, tablefmt="plain"))
    print(f"Time elapsed: {datetime.timedelta(seconds=end - start)}")


def main():
    """Runs the comparison function."""
    try:
        depth = int(sys.argv[1])
        if depth < 0:
            depth = 6
    except ValueError:
        depth = 6

    run_tests(parse_results_file(), depth)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
