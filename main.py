Back_RankPattern = [1,2,3,4,5,3,2,1]
import time, random
Piece_Dictionary = {
    1 : "♖",
    2 : "♘",
    3 : "♗",
    4 : "♕",
    5 : "♔",

    -1 : "♜",
    -2 : "♞",
    -3 : "♝",
    -4 : "♛",
    -5 : "♚",

    6 : "♙",
    -6 : "♟",
    0 : ""
}

Piece_DictionaryNEW = {
    1: "R", 2: "N", 3: "B", 4: "Q", 5: "K", 6: "P",
    -1: "r", -2: "n", -3: "b", -4: "q", -5: "k", -6: "p",
    0: " "
}
File_Dictionary = {
    "a" : 0,
    "b" : 1,
    "c" : 2,
    "d" : 3,
    "e" : 4,
    "f" : 5,
    "g" : 6,
    "h" : 7
}

board = []

def CreateBoard():
    for i in range(64):
        if i < 8:
            board.append(Back_RankPattern[i % 8])
        elif i >= 8 and i < 16:
            board.append(6)
        elif i >= 48 and i < 56:
            board.append(-6)
        elif i >= 56 and i < 64:
            board.append(-Back_RankPattern[i % 8])
        else:
            board.append(0)

def DisplayBoard():
    # Chessboard backgrounds
    Light_Square = "\033[48;2;240;217;181m"   # Light beige
    Dark_Square = "\033[48;2;181;136;99m"     # Medium brown
    # Piece colors
    White_Piece = "\033[38;2;255;255;255m"
    Black_Piece = "\033[38;2;0;0;0m"
    Reset = "\033[0m"

    print("\n     a    b    c    d    e    f    g    h")

    for row in range(7, -1, -1):
        print(row + 1, end="  ")

        for col in range(8):
            index = row * 8 + col
            piece = board[index]
            background_shade = (
                Light_Square
                if (row + col) % 2 == 0
                else Dark_Square
            )
            symbol = Piece_Dictionary.get(piece, " ")
            if piece > 0:
                piece_color = White_Piece
            elif piece < 0:
                piece_color = Black_Piece
            else:
                piece_color = ""

            if piece != 0:
                square = (background_shade +"  " +piece_color +symbol +background_shade +"  " +Reset)
            else:
                square = background_shade + "     " + Reset

            print(square, end="")
        print()

    print("     a    b    c    d    e    f    g    h\n")



def SquareToIndex(square):
    file_char = square[0]
    rank_char = square[1]

    rank_index = int(rank_char) - 1
    file_index = File_Dictionary.get(file_char, -1)
    return rank_index * 8 + file_index

def isValidPawnMove(Piece_At_square_index, Move_To_square_index):
    piece = board[Piece_At_square_index]
    direction = 1 if piece > 0 else -1
    target_index = Piece_At_square_index + direction * 8
    file_index = Piece_At_square_index % 8

    #Double forward move for pawns
    if (Piece_At_square_index // 8 == 1 and direction == 1 or Piece_At_square_index // 8 == 6 and direction == -1) and board[Move_To_square_index] == 0 and Move_To_square_index == Piece_At_square_index + direction * 16 and board[target_index] == 0:
        return True
    
    if board[Move_To_square_index] == 0 and Move_To_square_index == target_index: #Single step forward
        return True

    if file_index != 0:
        if Move_To_square_index == target_index - 1 and board[Move_To_square_index] * piece < 0:
            return True

    if file_index != 7:
        if Move_To_square_index == target_index + 1 and board[Move_To_square_index] * piece < 0:
            return True
    
    return False #No other valid pawn moves


def isValidKnightMove(Piece_At_square_index, Move_To_square_index):
    piece = board[Piece_At_square_index]
    file_index = Piece_At_square_index % 8
    rank_index = Piece_At_square_index // 8

    Absolute_Pairs = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    for file_offset, rank_offset in Absolute_Pairs:
        new_file_index = file_index + file_offset
        new_rank_index = rank_index + rank_offset

        if 7 >= new_file_index >= 0 and 7 >= new_rank_index >= 0:
            target_index = new_rank_index * 8 + new_file_index
            if target_index == Move_To_square_index and board[target_index] * piece <= 0:
                return True
    return False

def isValidRookMove(Piece_At_square_index, Move_To_square_index):
    piece = board[Piece_At_square_index]
    file_index = Piece_At_square_index % 8
    rank_index = Piece_At_square_index // 8
    move_rank_index = Move_To_square_index // 8
    move_file_index = Move_To_square_index % 8

    if rank_index != move_rank_index and file_index != move_file_index:
        return False

    
    if file_index == move_file_index:
        step = 8 if Move_To_square_index > Piece_At_square_index else -8
        i = Piece_At_square_index + step
        while i != Move_To_square_index:
            if board[i] != 0:
                return False
            i += step
        if i == Move_To_square_index and board[i] * piece <= 0:
            return True
        else:
            return False

    elif rank_index == move_rank_index:
        step = 1 if Move_To_square_index > Piece_At_square_index else -1
        i = Piece_At_square_index + step
        while i != Move_To_square_index:
            if board[i] != 0:
                return False
            i += step
        if i == Move_To_square_index and board[i] * piece <= 0:
            return True
        else:
            return False

def isValidBishopMove(Piece_At_square_index, Move_To_square_index):
    Piece_file_index = Piece_At_square_index % 8
    Piece_rank_index = Piece_At_square_index // 8
    Move_file_index = Move_To_square_index % 8
    Move_rank_index = Move_To_square_index // 8

    same_diagonal = (Piece_file_index - Move_file_index) == (Piece_rank_index - Move_rank_index)
    same_anti_diagonal = (Piece_file_index - Piece_rank_index) == (Move_file_index - Move_rank_index)

    if not same_diagonal and not same_anti_diagonal:
        return False

    if Move_rank_index > Piece_rank_index: #Diagonally upwards
        step = 9 if Move_file_index > Piece_file_index else 7
        i = Piece_At_square_index + step

        while i != Move_To_square_index:
            if board[i] != 0:
                return False
            i += step
        if board[i] * board[Piece_At_square_index] <= 0:
            return True #Capture enemy piece or move to empty square
        else:
            return False

    elif Move_rank_index < Piece_rank_index: #Diagonally downwards
        step = -7 if Move_file_index > Piece_file_index else -9
        i = Piece_At_square_index + step

        while i != Move_To_square_index:
            if board[i] != 0:
                return False
            i += step
        if board[i] * board[Piece_At_square_index] <= 0:
            return True #Capture enemy piece or move to empty square
        else:
            return False

def isValidKingMove(Piece_At_square_index, Move_To_square_index):
    piece = board[Piece_At_square_index]
    file_index = Piece_At_square_index % 8
    rank_index = Piece_At_square_index // 8
    move_rank_index = Move_To_square_index // 8
    move_file_index = Move_To_square_index % 8

    if abs(file_index - move_file_index) <= 1 and abs(rank_index - move_rank_index) <= 1:
        if board[Move_To_square_index] * piece <= 0:
            return True
    return False

def isValidQueenMove(Piece_At_square_index, Move_To_square_index):
    return isValidRookMove(Piece_At_square_index, Move_To_square_index) or isValidBishopMove(Piece_At_square_index, Move_To_square_index)

Price_Values = {
    1 : 10, #Rook
    2 : 8, #Knight
    3 : 6, #Bishop
    4 : 20, #Queen
    5 : 999, #King
    6 : 2 #Pawn
}

def EvaluatePoints():
    total = 0
    
    for i in range(64):
        piece = board[i]
        if piece != 0:
            price = Price_Values[abs(piece)]
            if piece > 0:
                total += price
            else:
                total -= price
    return total
        
def GenerateAllMoves(color):
    moves = []
    for from_index in range(64):
        piece = board[from_index]
        if piece != 0 and piece * color > 0:
            for destinations in range(64):
                if destinations == from_index:
                    continue
                validator = FunctionMapId.get(abs(piece))
                if validator(from_index, destinations):
                    moves.append((from_index, destinations))
    return moves


def Maximizing(depth, is_Maximizinging, alpha, beta):
    if depth == 0:
        return EvaluatePoints()

    if is_Maximizinging: #For White pieces
        moves = GenerateAllMoves(1)
        best_score = float('-inf')

        for from_index, to_index in moves:
            from_indexpiece = board[from_index]
            to_piece = board[to_index]

            board[to_index] = board[from_index]
            board[from_index] = 0

            new_best_score = Maximizing(depth-1, False, alpha, beta)
            if best_score < new_best_score:
                best_score = new_best_score

            board[from_index] = from_indexpiece
            board[to_index] = to_piece

            alpha = max(alpha,best_score)
            if alpha >= beta:
                break

        return best_score

    else: #For Black pieces
        moves = GenerateAllMoves(-1)
        best_score = float('inf')

        for from_index, to_index in moves:
            from_indexpiece = board[from_index]
            to_piece = board[to_index]

            board[to_index] = board[from_index]
            board[from_index] = 0

            new_best_score = Maximizing(depth-1, True, alpha, beta)
            if best_score > new_best_score:
                best_score = new_best_score

            board[from_index] = from_indexpiece
            board[to_index] = to_piece

            beta = min(beta,best_score)
            if beta <= alpha:
                break
        return best_score
    
import random

def FindKingSquare(color):
    for i in range(64):
        if board[i] == 5 * color:
            return i


def isKingChecked(color):
    King = FindKingSquare(color)
    Enemy_Color = -color

    for from_index in range(64):
        if board[from_index] != 0 and board[from_index] * Enemy_Color > 0:
            validator = FunctionMapId.get(abs(board[from_index]))
            if validator(from_index, King):
                return True
    return False

def isMoveLegal(from_index, to_index, color):
    from_index_piece = board[from_index]
    to_index_piece = board[to_index]

    board[to_index] = board[from_index]
    board[from_index] = 0

    is_Check = isKingChecked(color)

    board[to_index] = to_index_piece
    board[from_index] = from_index_piece

    return not is_Check

def GetLegalMoves(color):
    moves = GenerateAllMoves(color)
    new_moves = []
    for from_index,destinations in moves:
        if isMoveLegal(from_index, destinations,color):
            new_moves.append((from_index,destinations))
    return new_moves

def CheckGameStatus(color):
    new_moves = GetLegalMoves(color)
    if new_moves == [] and isKingChecked(color):
        return "Black" if color * -1 <0 else "White" #The other color won
    elif new_moves == [] and not isKingChecked(color):
        return "Stalemate" #Stalemate
    else:
        return "Continue" #Can continue
    

def FindBestMove(depth, color):
    moves = GenerateAllMoves(color)
    best_score = float('-inf') if color == 1 else float('inf')
    best_moves = []  # collect ALL moves tied for best, not just one

    for from_index, to_index in moves:
        from_indexpiece = board[from_index]
        to_piece = board[to_index]

        board[to_index] = board[from_index]
        board[from_index] = 0

        new_best_score = Maximizing(depth - 1, False if color > 0 else True, float('-inf'), float('inf'))

        if color > 0:  # maximizing
            if new_best_score > best_score:      # reset the list
                best_score = new_best_score
                best_moves = [(from_index, to_index)]
            elif new_best_score == best_score:    # tied — add to the list
                best_moves.append((from_index, to_index))
        else:  # minimizing
            if new_best_score < best_score:
                best_score = new_best_score
                best_moves = [(from_index, to_index)]
            elif new_best_score == best_score:
                best_moves.append((from_index, to_index))

        board[from_index] = from_indexpiece
        board[to_index] = to_piece

    return random.choice(best_moves)


def ActualMovePiece(Piece_At_square_index, Move_To_square_index):
    piece = board[Piece_At_square_index]
    board[Move_To_square_index] = piece
    board[Piece_At_square_index] = 0

FunctionMapId = {
    1 : isValidRookMove,
    2 : isValidKnightMove,
    3 : isValidBishopMove,
    4 : isValidQueenMove,
    5 : isValidKingMove,
    6 : isValidPawnMove
}

def MovePiece(Piece_At_square_index,Move_To_square_index):
    piece = board[Piece_At_square_index]
    validator = FunctionMapId.get(abs(piece))
    if validator(Piece_At_square_index, Move_To_square_index) and isMoveLegal(Piece_At_square_index,Move_To_square_index,-1 if piece < 0 else 1):
        ActualMovePiece(Piece_At_square_index, Move_To_square_index)
        return True
    return False

def PlayEngineMove(color):  #Play Black's move
    from_index, to_index = FindBestMove(2, color)
    MovePiece(from_index, to_index)



CreateBoard()
DisplayBoard()

Text = int(input("Enter choices \n 1 : AI vs AI \n 2 : Player vs AI \n"))
while True:
    if Text == 2:
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        Texts = input("Enter the Piece and Move index with space.").lower().split()
        if len(Texts) == 2:
            Piece_At_square_index = SquareToIndex(Texts[0])
            Move_To_square_index = SquareToIndex(Texts[1])
            if board[Piece_At_square_index] >= 1 and MovePiece(Piece_At_square_index,Move_To_square_index):
                status = CheckGameStatus(-1)
                DisplayBoard()
                if status == "Stalemate":
                    print("Stalemate")
                    break
                elif status == "Black" or status == "White":
                    print(status, "wins!")
                    break

                time.sleep(1)
            print("Black Moved")
            PlayEngineMove(-1)
            status = CheckGameStatus(1)
            DisplayBoard()
            if status == "Stalemate":
                    print("Stalemate")
                    break
            elif status == "Black" or status == "White":
                print(status, "wins!")
                break
            time.sleep(1)
    elif Text == 1:
        print("White moved!")
        PlayEngineMove(1)

        status = CheckGameStatus(-1)
        DisplayBoard()
        if status == "Stalemate":
            print("Stalemate")
            break
        elif status == "Black" or status == "White":
            print(status, "wins!")
            break

        time.sleep(1)

        print("Black moved!")
        PlayEngineMove(-1)
        status = CheckGameStatus(1)
        DisplayBoard()
        if status == "Stalemate":
                print("Stalemate")
                break
        elif status == "Black" or status == "White":
            print(status, "wins!")
            break
        time.sleep(1)
    else:
        print("Error! Enter options 1 or 2")
        break

    time.sleep(1)