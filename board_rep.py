letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
digits = list(range(1, 9))

ranks = dict(zip(letters, digits))

digit_strings = [str(x) for x in digits]
tens = [20, 30, 40, 50, 60, 70, 80, 90]

files = dict(zip(digit_strings, tens))

# encodes standard chess position references (e.g. "e1") to the array index

U = 10
D = -10
R = 1
L = -1

# directions to move


def parse_string(check_string):
    """Validates the move string and converts to array indices."""

    if len(check_string) != 4:
        return []
    else:
        pos_refs = [check_string[:2], check_string[2:]]  # splits string into the two positions it points to
        locations = []

        for part in pos_refs:
            if (part[0] in letters) and (part[1] in digit_strings):
                locations.append(ranks[part[0]] + files[part[1]])  # the array indices of the positions
            else:
                return []  # returns an empty array if the format is invalid

        return locations


def check_location(loc_array):
    """Checks if the position on the board is occupied."""

    for piece in Piece.piece_list:
        if loc_array[0] in piece.positions:
            return piece

    return


def check_move_distance(piece, location):
    """Checks if a piece's move-set allows them to reach a square."""
    diff = abs(location[0] - location[1])

    if piece.piece_type in (2, 4, 5):
        repeat = True
    else:
        repeat = False

    for move in piece.moves:
        if repeat:
            if diff % move == 0:
                return True
        else:
            if diff == move:
                return True


side_to_move = "white"

while 1:
    move_string = input("What move would you like to make: ")
    move_locations = parse_string(move_string)

    if not move_locations:
        print("Please enter your move in the correct format, e.g. 'a1b2'.")

    piece_to_move = check_location(move_locations)

    if not piece_to_move:
        print("There is no piece to move at this position.")
    else:
        piece_to_move.make_move(move_locations[0], move_locations[1])  # passes move to the piece class

    if side_to_move == "white":
        side_to_move = "black"
    else:
        side_to_move = "white"

    break
