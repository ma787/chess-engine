"Module providing the text client."
import sys
import time

from chess_engine import board, engine, hashing as hsh, move, move_gen as mg


def make_user_move(bd, legal_moves):
    """Carries out a legal move entered by the user.

    Args:
        bd (Board): The board object the game is being played on.
        legal_moves (list): The set of legal moves that can be
            made from this position and their LAN strings.

    Returns:
        int: 0 if successful, and -1 otherwise.
    """
    current_side = "Black" if bd.black else "White"

    while True:
        user_input = input(f"Enter move ({current_side}): ")
        mv = move.string_to_int(bd, user_input)

        if mv not in legal_moves:
            print("Please enter a valid move.")
        else:
            move.make_move(mv, bd)
            return


def end_of_game(bd, legal_moves):
    """Checks if there are no remaining legal moves."""
    for mv in legal_moves:
        result = move.make_move(mv, bd)
        if result != -1:
            move.unmake_move(mv, bd)
            return False
    return True


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


def play_game(player_colour, engine_mode):
    """Runs a game of chess between a player and another player/engine."""
    bd = board.Board()
    if player_colour is None:
        player_colour = bd.black

    state = -1
    positions = []
    legal_moves = mg.all_moves(bd)
    t_table = {}

    while state == -1:
        print(bd)

        if bd.black != player_colour and engine_mode:
            move.make_move(engine.find_move(bd, t_table), bd)
        else:
            make_user_move(bd, legal_moves)

        state = add_board_hash(bd, positions)
        if state == 2:
            break

        legal_moves = mg.all_moves(bd)

        # checkmate or stalemate
        if end_of_game(bd, legal_moves):
            if bd.check:
                state = bd.black ^ 1
            else:
                state = 2

        if state == -1 and bd.check:
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
        divider = (
            "\n_________________________________________________________________\n"
        )

        player_colour = None
        engine_mode = False

        print(divider + "Would you like to play with a friend or against the computer?")
        play_mode = get_user_choice("With a friend", "Against the computer")

        if play_mode == 2:
            print(divider + "Would you like to play as White or Black?")
            player_colour = get_user_choice("White", "Black") - 1
            engine_mode = True

        message = """Move format: (source|target|promotion), e.g., e1c1, g8h6, e7e8q."""

        print(divider + message + "\n")
        time.sleep(0.5)

        play_game(player_colour, engine_mode)

        print(divider + "Would you like to play another game?")
        done = input("Enter 'y' to do so, or press enter to exit: ")

        if done != "y":
            sys.exit()


if __name__ == "__main__":
    main()
