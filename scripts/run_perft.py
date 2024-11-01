import sys


from chess_engine import board, perft_divide as pd


def main():
    bd = board.Board()
    pd.perft(bd, int(sys.argv[1]))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
