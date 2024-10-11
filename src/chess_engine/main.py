"Module providing the text client."
import sys
import time

from chess_engine import (
    board,
    engine,
    hashing as hsh,
    lan_parser as lp,
    move,
    move_generation as mg,
)


def make_user_move(bd, legal_moves):
    """Carries out a legal move entered by the user.

    Args:
        bd (Board): The board object the game is being played on.
        legal_moves (dict): The set of legal moves that can be
            made from this position and their LAN strings.

    Returns:
        int: 0 if successful, and -1 otherwise.
    """
    current_side = "Black" if bd.black else "White"

    while True:
        user_input = input(f"Enter move ({current_side}): ")

        if user_input not in legal_moves.keys():
            print("Please enter a valid move.")

        else:
            mv = legal_moves[user_input]
            move.make_move(mv, bd)
            return


def add_board_hash(bd, positions):
    """Adds a new board hash to the list of positions and checks for a draw.
    
    Args:
        bd (Board): The board object the game is being played on.
        positions (list): The list of hashed board positions encountered
            during the game.
            
    Returns:
        tuple[list, int]: The updated list of positions, and the updated
            state of the game prior to mate detection.
    """
    bd_hash = hsh.zobrist_hash(bd)
    positions.append(bd_hash)

    # fivefold repetition or fifty-move rule
    if positions.count(bd_hash) == 5 or bd.halfmove_clock == 100:
        return 2
    return -1


def play_game(eng=None):
    """Runs a game of chess between a player and another player/engine.

    Args:
        eng (Engine, optional): The engine object to play against.
            Defaults to None.
    """
    bd = board.Board()
    state = -1
    positions = []
    legal_moves =  {lp.convert_move_to_lan(mv, bd): mv for mv in mg.all_legal_moves(bd)}
    eng_check = eng is not None

    print(f"Eng.black: {eng.black}, Board.black: {bd.black}")

    while state == -1:
        print(bd)

        if eng_check and eng.black == bd.black:
            move.make_move(eng.find_move(bd), bd)
        else:
            make_user_move(bd, legal_moves)

        state = add_board_hash(bd, positions)
        if state == 2:
            break

        legal_moves =  {lp.convert_move_to_lan(mv, bd): mv for mv in mg.all_legal_moves(bd)}
        check = mg.square_under_threat(bd, bd.find_king(bd.black), not bd.black)

        # checkmate or stalemate
        if len(legal_moves) == 0:
            state = 2 - int(check)*int(bd.black) - int(check)

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
