"""Module providing functions to test engine against standard perft results."""

import datetime
import sys
import time


from chess_engine import fen_parser as fp, perft_divide as pd


def parse_results_file(file_path):
    """Extracts perft results from file."""
    all_results = {}

    with open(file_path, "r", encoding="UTF-8") as f:
        lines = f.readlines()

        for line in lines:
            if line == "/n":
                break

            info = line.split(";")
            fen = info[0].strip()
            all_results[fen] = {}

            for i in range(1, len(info)):
                result = info[i].split(" ")
                all_results[fen][int(result[0][1:])] = int(result[1])

    return all_results


def run_tests(all_results, depth_lim):
    """Compares the engine's perft results to a provided set of results."""
    start = time.time()

    print(f"{"":12}{"FEN":72}", end="", flush=True)
    for i in range(1, depth_lim + 1):
        print(f"{i:8}", end="", flush=True)
    print(f"{"Time Elapsed":>19}")

    total = len(all_results)
    n = 1

    for fen, results in all_results.items():
        bd = fp.fen_to_board(fen)
        print(f"{f"({n}/{total})":12}{fen:72}", end="", flush=True)

        for i in range(1, depth_lim + 1):
            if i in results:
                res = str(pd.perft(bd, i) - results[i])
                print(f"{res:>8}", end="", flush=True)
            else:
                print(f"{'-':>8}", end="", flush=True)

        elapsed = datetime.timedelta(seconds=time.time() - start)
        print(f"{str(elapsed):>19}")
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
