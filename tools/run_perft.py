import sys
import time


from chess_engine import board, fen_parser as fp, perft_divide as pd


def main():
    """Runs perft and reports the result and time elapsed."""
    if len(sys.argv) > 2:
        bd = fp.fen_to_board(sys.argv[2])
    else:
        bd = board.Board()

    start = time.time()
    n = pd.perft(bd, int(sys.argv[1]))
    elapsed = time.time() - start
    print(f"Nodes: {n}\nTime elapsed: {elapsed}\nNPS: {n / elapsed}")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
