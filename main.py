import sys
import time

from game import Game


def main():
    print("Welcome!")
    while True:
        new_game = Game()

        divider = "\n_______________________________________________________________\n"

        print(divider + "Would you like to play with a friend or against the computer?")

        play_mode = input("""Please enter the corresponding number:
(1): With a friend
(2): Against the computer\nYour choice: """)

        message = ("""Please enter all moves in the following format:

For pawns: [starting position]['-' or 'x' for captures][destination][First letter of piece type to promote to]
For other pieces: [First letter of piece type][starting position]['-' or 'x' for captures][destination]

For example, 'e2-e4', 'Ng8-h6, 'Re5xd5', 'e7-e8Q' are all valid.
For castling moves, please enter '0-0' for king-side castling and '0-0-0' for queen-side castling.""")

        while play_mode not in ("1", "2"):
            play_mode = input("Please enter either '1' or '2': ")

        play_mode = int(play_mode)

        if play_mode == 2:
            print(divider + "Would you like to play as White or Black?")
            player_colour = input("""Please enter the corresponding number:
(1): White
(2): Black\nYour choice: """)

            while player_colour not in ("1", "2"):
                player_colour = input("Please enter either '1' or '2': ")

            player_colour = int(player_colour) - 1

            print(divider + message + divider)
            time.sleep(0.5)
            new_game.play_engine(player_colour)

        else:
            print(divider + message + divider)
            time.sleep(0.5)
            new_game.play_game()

        print(divider + "Would you like to play another game?")
        done = input("Press 'y' to do so, or press any other key to exit: ")

        if done != "y":
            sys.exit()


if __name__ == "__main__":
    main()
