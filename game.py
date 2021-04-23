import pygame
import board

pygame.init()

def images(style):
    global WHITE_IMG, WHITE_QUEEN_IMG, BLACK_IMG, BLACK_QUEEN_IMG, BOARD
    WHITE_IMG = pygame.image.load(f'images\\checkers\\white_{style}.png')
    WHITE_QUEEN_IMG = pygame.image.load(f'images\\checkers\\white_queen_{style}.png')
    BLACK_IMG = pygame.image.load(f'images\\checkers\\black_{style}.png')
    BLACK_QUEEN_IMG = pygame.image.load(f'images\\checkers\\black_queen_{style}.png')
    BOARD = pygame.image.load(f'images\\board\\board_{style}.png')

def draw():
    gameDisplay.fill((128, 128, 128))
    for i in range(8):
        text = FONT_LARGE.render(f'{i}', 1, BLACK)
        gameDisplay.blit(text, (12, 25 + 100 * i))
        gameDisplay.blit(text, (50 + 25 + 100 * i, 800))
    for i in range(len(moves)):
        text = FONT.render(moves[i], 1, WHITE if moves[i][0] != '-' else BLACK, WHITE if moves[i][0] == '-' else BLACK)
        gameDisplay.blit(text, (850, 25 * (y_start + i + 2)))
    if b.winner == 0:
        PTM_TEXT = FONT.render(f"{'Black' if b.player_to_move == 1 else 'White'} to move", 1, BLACK, GREY)
    else:
        PTM_TEXT = FONT.render(f"{'Black' if b.winner == 1 else 'White'} has won!", 1, BLACK, RED)
    gameDisplay.blit(PTM_TEXT, (870, 0))
    gameDisplay.blit(MOVE_TEXT, (900, 25))
    gameDisplay.blit(BOARD, (50, 0))
    if tile_of_move != None:
        gameDisplay.blit(GLOW, (100 * tile_of_move.x + 50, 100 * tile_of_move.y))
    for element in b.board[-1]:
        if isinstance(element, board.Queen):
            gameDisplay.blit(WHITE_QUEEN_IMG, (100 * element.tile.x + 50, 100 * element.tile.y))
        else:
            gameDisplay.blit(WHITE_IMG, (100 * element.tile.x + 50, 100 * element.tile.y))
    for element in b.board[1]:
        if isinstance(element, board.Queen):
            gameDisplay.blit(BLACK_QUEEN_IMG, (100 * element.tile.x + 50, 100 * element.tile.y))
        else:
            gameDisplay.blit(BLACK_IMG, (100 * element.tile.x + 50, 100 * element.tile.y))
    pygame.display.update()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (200, 0, 0)

FONT = pygame.font.Font('georgia.ttf', 20)
FONT_LARGE = pygame.font.Font('georgia.ttf', 40)
moves = []
y_start = 0

MOVE_TEXT = FONT.render('Moves:', 1, BLACK, GREY)

STYLE = 0
WHITE_IMG = 0
WHITE_QUEEN_IMG = 0
BLACK_IMG = 0
BLACK_QUEEN_IMG = 0
BOARD = 0
images(STYLE)
GLOW = pygame.image.load(f'images\\glow.png')

gameDisplay = pygame.display.set_mode((1050, 850))

b = board.Board()

tile_of_move = None
tile_to_move = None
clicked = False

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == 0 and pygame.mouse.get_pos()[0] <= 850 \
        and pygame.mouse.get_pos()[0] >= 50 and pygame.mouse.get_pos()[1] <= 800 and b.winner == 0:
            clicked = 1
            tile_to_check = board.Tile((pygame.mouse.get_pos()[0] - 50) // 100, pygame.mouse.get_pos()[1] // 100)
            if b.checker_on_tile(tile_to_check)[0] == b.player_to_move:
                tile_of_move = tile_to_check
            elif b.checker_on_tile(tile_to_check) == [0] and tile_of_move != None:
                tile_to_move = tile_to_check
                if b.take_possible():
                    res = b.take(tile_of_move, tile_to_move) 
                    if res != None:
                        if res:
                            moves.append(f'{b.player_to_move}: {tile_of_move} -> {tile_to_move}')
                        else:
                            moves.append(f'{-b.player_to_move}: {tile_of_move} -> {tile_to_move}')
                else:
                    res = b.move(tile_of_move, tile_to_move)
                    if res != None:
                        moves.append(f'{-b.player_to_move}: {tile_of_move} -> {tile_to_move}')
                tile_of_move = None
                tile_to_move = None
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = 0
        if event.type == pygame.MOUSEWHEEL:
            y_start += event.y
    
    draw()

pygame.quit()
quit()
