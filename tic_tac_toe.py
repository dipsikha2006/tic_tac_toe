import pygame
import math
import sys


pygame.init()

WIDTH, HEIGHT = 300, 350  
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 64, 52)      
GREEN = (52, 235, 88)     
GRAY = (200, 200, 200)
LINE_WIDTH = 5


FONT = pygame.font.SysFont("Consolas", 30, bold=True)
BIG_FONT = pygame.font.SysFont("Consolas", 40, bold=True)


board = [" "] * 9
human = "X"
ai = "O"

def check_winner(b):
    winning_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), 
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)             
    ]
    for x, y, z in winning_positions:
        if b[x] != " " and b[x] == b[y] == b[z]:
            return b[x]
    if " " not in b:
        return "Draw"
    return None

def alpha_beta(b, depth, alpha, beta, maximizing):
    result = check_winner(b)
    if result == ai: return 10 - depth
    if result == human: return depth - 10
    if result == "Draw": return 0

    if maximizing:
        best_score = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = ai
                score = alpha_beta(b, depth + 1, alpha, beta, False)
                b[i] = " "
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha: break
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = human
                score = alpha_beta(b, depth + 1, alpha, beta, True)
                b[i] = " "
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha: break
        return best_score

def find_best_move():
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            score = alpha_beta(board, 0, -math.inf, math.inf, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move



def draw_grid():
    WIN.fill(WHITE)
    # Vertical lines
    pygame.draw.line(WIN, BLACK, (100, 0), (100, 300), LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (200, 0), (200, 300), LINE_WIDTH)
    # Horizontal lines
    pygame.draw.line(WIN, BLACK, (0, 100), (300, 100), LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (0, 200), (300, 200), LINE_WIDTH)

def draw_figures():
    for i in range(9):
        col = i % 3
        row = i // 3
        center_x = col * 100 + 50
        center_y = row * 100 + 50
        radius = 30
        offset = 25

        if board[i] == human:
            
            pygame.draw.line(WIN, RED, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), LINE_WIDTH)
            pygame.draw.line(WIN, RED, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), LINE_WIDTH)
        elif board[i] == ai:
    
            pygame.draw.circle(WIN, GREEN, (center_x, center_y), radius, LINE_WIDTH)

def draw_status(message, color):
    
    pygame.draw.rect(WIN, WHITE, (0, 300, WIDTH, 50))
    text = FONT.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH/2, 325))
    WIN.blit(text, text_rect)

def draw_winner_line(start_pos, end_pos):
    pygame.draw.line(WIN, BLACK, start_pos, end_pos, 10)

def get_winning_line_pos(result):
    winning_positions = [
        [(0, 1, 2), (50, 50), (250, 50)],   
        [(3, 4, 5), (50, 150), (250, 150)],
        [(6, 7, 8), (50, 250), (250, 250)], 
        [(0, 3, 6), (50, 50), (50, 250)],   
        [(1, 4, 7), (150, 50), (150, 250)], 
        [(2, 5, 8), (250, 50), (250, 250)], 
        [(0, 4, 8), (50, 50), (250, 250)],  
        [(2, 4, 6), (250, 50), (50, 250)]   
    ]
    for combo, start, end in winning_positions:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == result:
            return start, end
    return None

 
def main():
    global board
    game_over = False
    current_player = human  
    
    draw_grid()
    draw_status("Your Turn! (X)", RED)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_player == human:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]

                    
                    if mouseY < 300:
                        clicked_row = int(mouseY // 100)
                        clicked_col = int(mouseX // 100)
                        clicked_index = clicked_row * 3 + clicked_col

                        if board[clicked_index] == " ":
                            board[clicked_index] = human
                            current_player = ai
                            
                            draw_grid()
                            draw_figures()
                            draw_status("AI Thinking...", GREEN)
                            pygame.display.update()

            
            if current_player == ai and not game_over:
                pygame.time.delay(500) 
                ai_move = find_best_move()
                if ai_move is not None:
                    board[ai_move] = ai
                
                current_player = human
                draw_grid()
                draw_figures()
                draw_status("Your Turn! (X)", RED)
                pygame.display.update()

            
            result = check_winner(board)
            if result and not game_over:
                game_over = True
                if result == human:
                    msg = "YOU WIN! (Press R)"
                    color = RED
                elif result == ai:
                    msg = "AI WINS! (Press R)"
                    color = GREEN
                else:
                    msg = "DRAW! (Press R)"
                    color = BLACK
                
                draw_status(msg, color)
                
                if result != "Draw":
                    line_pos = get_winning_line_pos(result)
                    if line_pos:
                        draw_winner_line(line_pos[0], line_pos[1])

                pygame.display.update()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = [" "] * 9
                    game_over = False
                    current_player = human
                    draw_grid()
                    draw_figures()
                    draw_status("Your Turn! (X)", RED)
                    pygame.display.update()

        
        pygame.display.update()

if __name__ == "__main__":
    main()
