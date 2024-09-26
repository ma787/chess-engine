"Module providing the text client."

import sys
import time

from chess_engine import (
    board,
    engine,
    hashing,
    lan_parser as lp,
    move,
    move_generation as mg,
)


def make_user_move(bd):
    """Carries out a legal move entered by the user.

    Args:
        bd (Board): The board object the game is being played on.

    Returns:
        int: 0 if successful, and -1 otherwise.
    """
    current_side = "Black" if bd.black else "White"

    while True:
        user_input = input(f"Enter move ({current_side}): ")
        mv = lp.convert_lan_to_move(user_input, bd)

        if mv == -1 or not move.legal(mv, bd):
            print("Please enter a valid move.")

        else:
            move.make_move(mv, bd)
            return


def update_game_state(bd, zh, positions):
    """Updates the state of the game after a move is made.

    Args:
        bd (Board): The board object the game is being played on.
        zh (Hashing): The hashing object used to hash board positions.
        positions (list): The list of hashed board positions encountered
            during the game.

    Returns:
        int: The new state of the game:
            -1: ongoing, 0: white win, 1: black win, 2: draw
    """
    state = -1
    board_hash = zh.zobrist_hash(bd)
    positions.append(board_hash)

    # check draw due to fivefold repetition or fifty move rule
    if positions.count(board_hash) == 5 or bd.halfmove_clock == 100:
        state = 2
        return True

    check = mg.in_check(bd)
    moves = mg.all_possible_moves(bd)

    # checkmate or stalemate
    if len(moves) == 0:
        state = int(not bd.black) if check else 2

    return state, check


def play_game(eng=None):
    """Runs a game of chess between a player and another player/engine.

    Args:
        eng (Engine, optional): The engine object to play against.
            Defaults to None.
    """
    bd = board.Board()
    zh = hashing.Hashing()
    state = -1
    positions = []
    eng_check = eng is not None

    print(f"Eng.black: {eng.black}, Board.black: {bd.black}")

    while state == -1:
        print(bd)

        if eng_check and not (eng.black ^ bd.black):
            move.make_move(eng.find_move(bd), bd)
            
        else:
            make_user_move(bd)

        state, check = update_game_state(bd, zh, positions)

        if state == -1 and check:
            print(f"\n{"Black" if bd.black else "White"} is in check.\n")

    print(bd)

    if state == 0:
        print("\nWhite wins.\n")
    elif state == 1:
        print("\nBlack wins.\n")
    else:
        print("\nDraw.\n")


def get_user_choice(fst, snd):
    """D"""
    choice = input(
        f"""Please enter the corresponding number:
        (1): {fst}
        (2): {snd}\nYour choice: """
    )

    while choice not in ("1", "2"):
        choice = input("Please enter either 1 or 2: ")

    return int(choice)


def main():
    """The text client."""
    print("Welcome!")

    while True:
        eng = None

        divider = "\n_______________________________________________________________\n"

        print(divider + "Would you like to play with a friend or against the computer?")
        play_mode = get_user_choice("With a friend", "Against the computer")

        if play_mode == 2:
            print(divider + "Would you like to play as White or Black?")
            player_colour = get_user_choice("White", "Black") - 1
            eng = engine.Engine(not bool(player_colour))

        message = """Please enter all moves in the following format:

Pawns: [starting position]['-' or 'x'][destination][piece type to promote to]
Other pieces: [piece type][starting position]['-' or 'x'][destination]

Use 'x' for captures and '-' for all other moves.

For example, 'e2-e4', 'Ng8-h6, 'Re5xd5', 'e7-e8Q' are all valid.
Kingside castle: '0-0'
Queenside castle: '0-0-0'"""

        print(divider + message + divider)
        time.sleep(0.5)

        play_game(eng=eng)

        print(divider + "Would you like to play another game?")
        done = input("Enter 'y' to do so, or press enter to exit: ")

        if done != "y":
            sys.exit()


if __name__ == "__main__":
    main()
