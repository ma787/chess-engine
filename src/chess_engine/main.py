import sys
import time

from chess_engine import attributes as attrs, engine, game


def main():
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

For pawns: [starting position]['-' or 'x' for captures][destination][First letter of piece type to promote to]
For other pieces: [First letter of piece type][starting position]['-' or 'x' for captures][destination]

For example, 'e2-e4', 'Ng8-h6, 'Re5xd5', 'e7-e8Q' are all valid.
For castling moves, please enter '0-0' for king-side castling and '0-0-0' for queen-side castling."""

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

            if player_colour == attrs.Colour.BLACK.value:
                eng = engine.Engine(attrs.Colour.WHITE)
            else:
                eng = engine.Engine(attrs.Colour.BLACK)

        print(divider + message + divider)
        time.sleep(1)

        while new_game.state == -1:
            print(new_game.board)

            if eng and (new_game.board.side_to_move.value == eng.colour.value):
                new_game.update_game_state(eng.find_move(new_game.board))
            else:
                user_input = input(
                    f"Enter move ({new_game.board.side_to_move.name.title()}): "
                )
                change = new_game.update_game_state(user_input)

                while not change:
                    print("Please enter a valid move.")
                    user_input = input(
                        f"Enter move ({new_game.board.side_to_move.name.title()}): "
                    )
                    change = new_game.update_game_state(user_input)

            if new_game.state != -1:
                print(new_game.board)

                if new_game.state == attrs.Colour.WHITE.value:
                    print("\nWhite wins.\n")

                elif new_game.state == attrs.Colour.BLACK.value:
                    print("\nBlack wins.\n")
                else:
                    print("\nIt is a draw.\n")

                print(f"White's score: {new_game.scores[attrs.Colour.WHITE.value]}")
                print(f"Black's score: {new_game.scores[attrs.Colour.BLACK.value]}")

                break

            if new_game.check:
                print(f"\n{new_game.board.side_to_move.name.title()} is in check.\n")

        print(divider + "Would you like to play another game?")
        done = input("Enter 'y' to do so, or press enter to exit: ")

        if done != "y":
            sys.exit()


if __name__ == "__main__":
    main()
