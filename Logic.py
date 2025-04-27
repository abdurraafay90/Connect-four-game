from copy import deepcopy

RED = "R"
YELLOW = "Y"
EMPTY = None
ROWS = 6
COLUMNS = 7


def initial_state():
    return [[EMPTY] * COLUMNS for _ in range(ROWS)]


def player(board):
    reds = sum(row.count(RED) for row in board)
    yellows = sum(row.count(YELLOW) for row in board)
    return RED if reds <= yellows else YELLOW


def actions(board):
    return {col for col in range(COLUMNS) if board[0][col] == EMPTY}


def result(board, column):
    new_board = deepcopy(board)
    for row in reversed(range(ROWS)):
        if new_board[row][column] == EMPTY:
            new_board[row][column] = player(board)
            break
    return new_board


def winner(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != EMPTY and (
                check_direction(board, row, col, 1, 0) or
                check_direction(board, row, col, 0, 1) or
                check_direction(board, row, col, 1, 1) or
                check_direction(board, row, col, 1, -1)
            ):
                return board[row][col]
    return None


def check_direction(board, row, col, d_row, d_col):
    piece = board[row][col]
    for i in range(1, 4):
        r= row + i * d_row
        c= col + i * d_col
        if r < 0 or r >= ROWS or c < 0 or c >= COLUMNS or board[r][c] != piece:
            return False
    return True


def terminal(board):
    return (winner(board) is not None
            or all(board[0][col] != EMPTY for col in range(COLUMNS)))


def utility(board):
    win = winner(board)
    return 1 if win == RED else -1 if win == YELLOW else 0


def minimax(board, depth, alpha, beta, maximizing_player, ai_color):
    if terminal(board):
        return utility(board), None

    if depth == 0:
        return 0, None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False, ai_color)
            if eval > max_eval:
                max_eval = eval
                best_move = action
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True, ai_color)
            if eval < min_eval:
                min_eval = eval
                best_move = action
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
