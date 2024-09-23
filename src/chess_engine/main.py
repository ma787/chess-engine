"Module providing the text client."

import sys
import time

from chess_engine import engine, game


def main():
    """The text client."""
    print("Welcome!")

    while True:
        new_game = game.Game()
        eng = None

        divider = "\n_______________________________________________________________\n"

        print(divider + "Would you like to play with a friend or against the computer?")

        play_mode = input(
            """Please enter the corresponding number:
        (1): With a friend
        (2): Against the computer\nYour choice: """
        )

        message = """Please enter all moves in the following format:

Pawns: [starting position]['-' or 'x'][destination][piece type to promote to]
Other pieces: [piece type][starting position]['-' or 'x'][destination]

Use 'x' for captures and '-' for all other moves.

For example, 'e2-e4', 'Ng8-h6, 'Re5xd5', 'e7-e8Q' are all valid.
Kingside castle: '0-0'
Queenside castle: '0-0-0'"""

        while play_mode not in ("1", "2"):
            play_mode = input("Please enter either '1' or '2': ")

        play_mode = int(play_mode)

        if play_mode == 2:
            print(divider + "Would you like to play as White or Black?")
            player_colour = input(
                """Please enter the corresponding number:
        (1): White
        (2): Black\nYour choice: """
            )

            while player_colour not in ("1", "2"):
                player_colour = input("Please enter either '1' or '2': ")

            player_colour = int(player_colour) - 1

            if player_colour:
                eng = engine.Engine(True)
            else:
                eng = engine.Engine(False)

        print(divider + message + divider)
        time.sleep(0.5)

        while new_game.state == -1:
            print(new_game.board)
            side = "Black" if new_game.board.black else "White"

            if eng and (new_game.board.black == eng.black):
                new_game.update_game_state(eng.find_move(new_game.board))
            else:
                user_input = input(f"Enter move ({side}): ")
                change = new_game.update_game_state(user_input)

                while not change:
                    print("Please enter a valid move.")
                    user_input = input(f"Enter move ({side}): ")
                    change = new_game.update_game_state(user_input)

            if new_game.state != -1:
                print(new_game.board)

                if new_game.state == 0:
                    print("\nWhite wins.\n")

                elif new_game.state == 1:
                    print("\nBlack wins.\n")
                else:
                    print("\nIt is a draw.\n")

                break

            if new_game.check:
                print(f"\n{side} is in check.\n")
                time.sleep(0.2)

        print(divider + "Would you like to play another game?")
        done = input("Enter 'y' to do so, or press enter to exit: ")

        if done != "y":
            sys.exit()


if __name__ == "__main__":
    main()
