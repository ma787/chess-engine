import sys
import time


from chess_engine import board, perft_divide as pd


def main():
    bd = board.Board()
    start = time.time()
    n = pd.perft(bd, int(sys.argv[1]))
    elapsed = time.time() - start
    print(f"Nodes: {n}\nTime elapsed: {elapsed}")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
