import pygame
import sys
import time
import Logic as cf

pygame.init()
size = width, height = 700, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)


largeFont = pygame.font.Font(None, 40)
moveFont = pygame.font.Font(None, 60)
titleFont = pygame.font.Font(None, 80)


board = cf.initial_state()
user_color = None
ai_color = None
ai_turn = False
game_over = False
winner = None
column_buttons = [pygame.Rect(col * 100, 0, 100, 50) for col in range(cf.COLUMNS)]


def draw_board(board, line_coords=None):
    screen.fill(black)

    for i, button in enumerate(column_buttons):
        pygame.draw.rect(screen, white, button)
        text = largeFont.render(str(i + 1), True, black)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    for row in range(cf.ROWS):
        for col in range(cf.COLUMNS):
            pygame.draw.rect(screen, white, (col * 100, row * 100 + 100, 100, 100), 3)
            if board[row][col] == cf.RED:
                color = red
            elif board[row][col] == cf.YELLOW:
                color = yellow
            else:
                continue

            pygame.draw.circle(screen, color, (col * 100 + 50, row * 100 + 150), 40)

    if line_coords:
        pygame.draw.line(screen, blue, line_coords[0], line_coords[1], 5)

    pygame.display.flip()


def start_screen():
    screen.fill(black)
    title = titleFont.render("Connect Four", True, white)
    title_rect = title.get_rect(center=(width / 2, height / 4))
    screen.blit(title, title_rect)

    red_button = pygame.Rect(width / 4, height / 2, width / 2, 50)
    yellow_button = pygame.Rect(width / 4, height / 2 + 60, width / 2, 50)

    red_text = largeFont.render("Play as Red", True, black)
    yellow_text = largeFont.render("Play as Yellow", True, black)

    pygame.draw.rect(screen, red, red_button)
    pygame.draw.rect(screen, yellow, yellow_button)

    screen.blit(red_text, red_text.get_rect(center=red_button.center))
    screen.blit(yellow_text, yellow_text.get_rect(center=yellow_button.center))

    pygame.display.flip()

    global user_color, ai_color, ai_turn
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if red_button.collidepoint(event.pos):
                    user_color = cf.RED
                    ai_color = cf.YELLOW
                    return
                elif yellow_button.collidepoint(event.pos):
                    user_color = cf.YELLOW
                    ai_color = cf.RED
                    ai_turn = True
                    return


def check_direction(board, row, col, delta_row, delta_col):
    player = board[row][col]
    winning_positions = [(row, col)]

    for i in range(1, 4):
        r, c = row + i * delta_row, col + i * delta_col
        if 0 <= r < cf.ROWS and 0 <= c < cf.COLUMNS and board[r][c] == player:
            winning_positions.append((r, c))
        else:
            return None

    if len(winning_positions) == 4:
        return winning_positions
    return None


def highlight_winner(board):
    for row in range(cf.ROWS):
        for col in range(cf.COLUMNS):
            if board[row][col] != cf.EMPTY:
                for delta_row, delta_col in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    winning_positions = check_direction(board, row, col, delta_row, delta_col)
                    if winning_positions:
                        start = (
                            winning_positions[0][1] * 100 + 50,
                            winning_positions[0][0] * 100 + 150,
                        )
                        end = (
                            winning_positions[-1][1] * 100 + 50,
                            winning_positions[-1][0] * 100 + 150,
                        )
                        return start, end
    return None


def game_over_screen(winner):
    screen.fill(black)
    if winner:
        text = f"{'Red' if winner == cf.RED else 'Yellow'} Wins!"
    else:
        text = "It's a Tie!"

    title = titleFont.render(text, True, white)
    title_rect = title.get_rect(center=(width / 2, height / 2 - 50))
    screen.blit(title, title_rect)

    play_again_button = pygame.Rect(width / 4, height / 2 + 50, width / 2, 50)
    play_again_text = largeFont.render("Play Again", True, black)
    play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
    pygame.draw.rect(screen, white, play_again_button)
    screen.blit(play_again_text, play_again_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    return True


start_screen()


while True:
    draw_board(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not ai_turn and not game_over:
            for col, button in enumerate(column_buttons):
                if button.collidepoint(event.pos) and col in cf.actions(board):
                    board = cf.result(board, col)
                    draw_board(board)
                    time.sleep(0.5)
                    ai_turn = True
                    break

    if ai_turn and not game_over:
        time.sleep(0.5)
        _, col = cf.minimax(board, 4, float('-inf'), float('inf'), user_color != cf.RED, ai_color)
        if col is not None:
            board = cf.result(board, col)
            draw_board(board)
            time.sleep(0.5)
        ai_turn = False

    winner = cf.winner(board)
    if cf.terminal(board):
        game_over = True
        line_coords = highlight_winner(board)
        draw_board(board, line_coords=line_coords)
        time.sleep(3)
        if game_over_screen(winner):
            board = cf.initial_state()
            game_over = False
            ai_turn = ai_color == cf.RED
            winner = None
