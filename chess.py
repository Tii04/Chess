fen  = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
def parse_fen(fen):
    # Please complete this function
    fen_pieces, to_move, castling_rights, ep, hm, fm = fen.split(" ")
    pieces = [[]]
    for char in fen_pieces:
        if char.isdigit():
            pieces[-1].extend(["."] * int(char))
        elif char == "/":
            pieces.append([])
        else:
            pieces[-1].append(char)

    fen_pieces = [' '.join(str(piece) for piece in row[0:8]) for row in pieces]
    fen_pieces = '\n'.join(fen_pieces)
    to_move = pieces[-1][9]

    return fen_pieces, to_move


def generate_moves(board):
    raise NotImplementedError("This function is not implemented yet. Please complete it")


def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet. Please complete it")
