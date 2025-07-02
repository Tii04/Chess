
fen = "rnbqkbnr/pppp1ppp/4p3/8/8/5N2/PPPPPPPP/RNBQKB1R w KQkq - 0 2"

def parse_fen(fen):
    fen_pieces, to_move, castling_rights, ep, hm, fm = fen.split(" ")
    pieces = [[]]
    for char in fen:
        if char.isdigit(): #change num to . == empty pos
            pieces[-1].extend(["."] * int(char))
        elif char == "/":  #new row
            pieces.append([])
        else:
            pieces[-1].append(char)

    #board_fen_pieces = [' '.join(str(piece) for piece in row[0:8]) for row in pieces]
    #board_fen_pieces = '\n'.join(fen_pieces)
    fen_pieces = [each[0:8] for each in pieces]
    #to_move = pieces[-1][9]

    return fen_pieces, to_move

    #caps upper pieces is white, to _move w == white, b, castling_rights, KQ kq k== king side queen side castling 2 empty space,
    #ep en passant capture if pawn from enemy in starting position mov 2 is side by side to my pawn from other comment ep == - no capture avail
    #hm == half move , if pawn move count = 0, elif capture piece count = 0
    #fm == full move, if b moves increment full move +1 repr by
    # / seperate board pieces
    # 5n2 5 empty N knight 2 empty

board1 = parse_fen(fen)

def generate_moves(board1):

    min, max = 0, 8 #lowest and for highest bound
    d_p = {'q','Q','b','B'} #needs diag positive and negative and diag reverse pos and neg
    h_p = {'q','r','Q','R'}
    v_p = {'q','r','Q','R'}
    j,i = 0, 0 #used for matrix traverse
    moves = []
    dot  = '.'
    board, play = board1


    def diag(pos, board,play): #check diagonal pieces
        i,j = pos
        #j = pos[1]
        #l,k = i,j
        dot  = '.'
        moves = []
        u = 1
        d = -1
        diags = [(u,d),(u,u),(d,u),(d,d)]

        for g,h in diags:
            l,k =  i + g, j + h
            while 0 <= l < 8 and 0 <= k < 8:
                curr = board[l][k]
                if curr == dot:
                    moves.append((l,k))
                elif ('w' == play and curr.islower()) or ('b' == play and curr.isupper()): #capture piece
                    moves.append((l,k))
                    break
                else: #same color blocking
                    break

                l += g
                k += h

        return moves


    def vert(pos,board,play):
        i,j = pos
        #j = pos[1]
        line = [1, -1]
        dot  = '.'
        moves = []

        for l in line:
            g = i + l
            while 0 <= g < 8:
                curr = board[g][j]
                if curr == dot:
                    moves.append((g,j))
                elif (play == 'w' and curr.islower()) or (play == 'b' and curr.isupper()):
                    moves.append((g,j))
                    break
                else:
                    break

                g +=l

        '''while l < 8:
            if dot in board[l][k]:
                moves.append((l,k))
            l+=1'''

        return moves


    def hor(pos, board, play):
        i,j = pos
        #j = pos[1]
        #l,k = i,0
        line = [1,-1]
        dot  = '.'
        moves = []

        for k in line:
            h = k + j
            while 0 <= h < 8:
                curr = board[i][h]
                if curr == dot:
                    moves.append((i,h))
                elif (play == 'w' and curr.islower()) or (play == 'b' and curr.isupper()):
                    moves.append((i,h))
                    break
                else:
                    break
                h += k

        return moves

    while i < max:
        j=0
        while j < max:
            pos = [i,j]
            #knight to move n = piece, m is try moving
            n_m = [(i+2,j+1),(i+2,j-1),(i+1,j+2),(i+1,j-2),(i-1,j-2),(i-1,j-2),(i-2,j-1),(i-2,j+1)] #in board bounds, and is . return pos

            #pawns checking
            pbs_m = [(i+1, j), (i+2, j)] #pawn black to move from start # strat pos j == 1
            pba_m = [(i+1, j+1), (i+1, j-1)] #pawn black attack to move
            pb_m = [pbs_m[0]] #pawn okay to move
            pws_m = [(i-1, j), (i-2, j)] #start pos j == 6
            pw_m = [pws_m[0]]
            pwa_m = [(i-1, j+1), (i-1, j-1)]

            # king possible total
            k_m = [(i-1, j-1),(i-1, j),(i-1, j+1),(i+1, j-1),(i+1, j),(i+1, j+1),(i, j-1),(i,j+1)]
            piece = board[i][j]
            
            if 'b' == play:
                if piece.islower():
                    if piece in d_p:#diag function
                        moves.append([piece,diag(pos,board,play)])
                    elif piece in v_p:
                        moves.append([piece,vert(pos,board,play)])
                    elif piece in h_p:
                        moves.append([piece,hor(pos,board,play)])
                    elif piece == 'n':
                        temp = ['n']
                        for b,c in n_m:
                            if 0 <= b < max and 0 <= c < max:
                                if dot in board[b][c]:
                                    temp.append((b,c))
                                elif board[b][c].isupper():
                                    temp.append((b,c))
                        moves.append(temp)
                    elif piece == 'k':
                        temp = ['k']
                        for b,c in k_m:
                            if 0 <= b < max and 0 <= c < max:
                                if dot in board[b][c]:
                                    temp.append((b,c))
                                elif board[b][c].isupper():
                                    temp.append((b,c))
                        moves.append(temp)

                    elif piece == 'p':
                        temp = ['p']
                        for b,c in pba_m:
                            if 0 <= c < max and board[b][c].isupper():
                                temp.append((b,c))

                        for b,c in pbs_m:
                            if i == 1:# from start
                                if board[b][c] == dot:
                                    temp.append((b,c))

                        for b,c in pb_m:
                            if i != 1 :
                                if board[b][c] == dot:
                                    temp.append((b,c))

                        moves.append(temp)

            elif 'w' == play:
                if piece.isupper():
                    if piece in d_p: #diag function
                        moves.append([piece,diag(pos,board,play)])
                    elif piece in v_p:
                        moves.append([piece,vert(pos,board,play)])
                    elif piece in h_p:
                        moves.append([piece,hor(pos,board,play)])

                    elif piece == 'N':
                        temp = ['N']
                        for b,c in n_m:
                            if 0 <= b < max and 0 <= c < max:
                                if dot in board[b][c]:
                                    temp.append((b,c))
                                elif board[b][c].islower():
                                    temp.append((b,c))
                                    break
                        moves.append(temp)

                    elif piece == 'K':
                        temp = ['K']
                        for b,c in k_m:
                            if 0 <= b < max and 0 <= c < max:
                                if board[b][c] == dot:
                                    temp.append((b,c))
                                elif board[b][c].islower():
                                    temp.append((b,c))
                                    break
                                else:
                                    break
                        moves.append(temp)

                    elif piece == 'P':
                        temp = ['P']
                        for b,c in pwa_m:
                            if 0 <= c < max and board[b][c].islower() and board[b][c].isalpha():
                                temp.append((b,c))
                                break

                        if i == 6:# from start]
                            for b,c in pws_m:
                                if board[b][c] == '.':
                                    temp.append((b,c))

                        elif i != 6:
                            for b,c in pw_m:
                                if dot in board[b][c]:
                                    temp.append((b,c))

                        moves.append(temp)
            j+=1
        i += 1

    #SANITIZE
    sanit=[each for each in moves if each[-1]]
    sanit=[each for each in sanit if len(each) > 1]

                #pass
    return sanit #[piece, (0,5), (0,2)]


moves_total = generate_moves(board1)
print(moves_total)


def apply_move(board, move):
    raise NotImplementedError("This function is not implemented yet. Please complete it")


def boardview(board1):
    boardp, play = board1

    boardp = [' '.join(str(piece) for piece in row[0:8]) for row in boardp]
    boardp = '\n'.join(boardp)

    return boardp
    
print(boardview(board1))
