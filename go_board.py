# Author: Ashley Owens
# Date: 6/4/2020
# Description: CS 162, Portfolio Project
# Uses PyGame to implement the Gess Board Game.


try:
    import sys, os, pygame
    from socket import *
    from pygame.locals import *
    from GessGame import GessGame, GessBoard
except ImportError:
    print("Could not load module: ImportError.")
    sys.exit(2)


def load_image(name):
    """
    :param name: filename to be loaded (string)
    :return: image object, rectangular area of the image object
    """
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print('Cannot load image: ', fullname)
        raise SystemExit
    return image


def update_board(screen, background):
    """
    Initializes and updates the visual components of
    the game board to include changes in stone positions.
    :param screen: pygame display object
    :param background: jpg image
    :return: updated coordinates dictionary
    """
    # Creates an outline of the game board.
    line = pygame.Rect(50, 50, 600, 600)
    pygame.draw.rect(background, steel, line, 3)
    bs_image = load_image('blackstone.png')
    ws_image = load_image('whitestone.png')

    # Creates the game board grid from the back end and saves
    # each Rect object in a list for later dictionary mapping.
    grid_rects = []
    for i in range(20):

        for j in range(20):
            if game.get_board()[j+1][i] == 'B':
                rect = pygame.Rect(50+(30 * i), 50+(30 * j), 30, 30)
                grid_rects.append(rect)
                image_rect = (52+(30 * i), 52+(30 * j))
                background.blit(bs_image, image_rect)
                pygame.draw.rect(background, steel, rect, 1)

            elif game.get_board()[j+1][i] == 'W':
                rect = pygame.Rect(50+(30 * i), 50+(30 * j), 30, 30)
                grid_rects.append(rect)
                image_rect = (52+(30 * i), 52+(30 * j))
                background.blit(ws_image, image_rect)
                pygame.draw.rect(background, steel, rect, 1)

            else:
                rect = pygame.Rect(50+(30 * i), 50+(30 * j), 30, 30)
                grid_rects.append(rect)
                pygame.draw.rect(background, steel, rect, 1)

    # Adds visualization to differentiate player turns.
    font = pygame.font.SysFont('sfnsdisplaycondensedregularotf', 20)
    text = font.render("Player Turn: ", True, steel)
    background.blit(text, (10, 670))

    if game.get_turn() == "BLACK":
        image_rect = (105, 670)
        background.blit(bs_image, image_rect)
    else:
        image_rect = (105, 670)
        background.blit(ws_image, image_rect)
    screen.blit(background, (0, 0))

    # Adds text column headers to the game board.
    font = pygame.font.SysFont('copperplatettc', 20)
    for i in range(len(letters)):
        if letters[i] == 'I':
            text = font.render(letters[i], True, steel)
            screen.blit(text, (62+(i * 30), 28))
        else:
            text = font.render(letters[i], True, steel)
            screen.blit(text, (58+(i * 30), 28))

    # Adds text row headers to the game board.
    for i in range(len(nums)-11):
        text = font.render(str(nums[i]), True, steel)
        screen.blit(text, (31, 56+(i * 30)))
    for i in range(9, len(nums)):
        text = font.render(str(nums[i]), True, steel)
        screen.blit(text, (21, 56+(i * 30)))

    # Updates dictionary of all rect objects.
    coordinates = update_dict(grid_rects)
    return coordinates


def update_dict(grid_rects):
    """
    Creates a dictionary mapping of each Rect object on the
    game board to it's alphanumeric position ('A2').
    :param grid_rects: ordered list of Rect objects comprising the game board.
    :return: coordinates dictionary
    """
    alpha_num_lst = []
    for i in range(len(letters)):
        for j in range(1, 21):
            coord = letters[i]+str(j)
            alpha_num_lst.append(coord)

    # Key is alphanumeric position, value is that position's Rect object.
    coordinates = dict(zip(alpha_num_lst, grid_rects))
    return coordinates


def main():
    """
    Initializes game board screen, stones, and runs game loop.
    """
    pygame.init()
    x, y = 700, 740

    # Initializes the PyGame screen, background, and mapping dict.
    screen = pygame.display.set_mode((x, y))
    icon = load_image('gameicon.png')
    background = load_image('board_bg.jpg')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Gess')
    coordinates = update_board(screen, background)
    pygame.display.update()
    clicks = []

    # Initiates the game loop.
    while True:

        # Clicking on window exit button ends game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # Locates click coordinates in dict and adds red outline to enhance footprint.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for click in range(0, 1):
                    for key, value in coordinates.items():
                        if value.collidepoint(event.pos):
                            clicks.append(key)
                            rect = pygame.Rect(value)
                            inflated = rect.inflate(60, 60)
                            pygame.draw.rect(background, red, inflated, 4)
                            screen.blit(background, (0, 0))
                            update_board(screen, background)
                            pygame.display.update()
                print(clicks)

            # Waits for second location coordinate.
            if len(clicks) < 2:
                continue

            # Calls location coordinates with make_move and updates game board.
            else:
                if game.make_move(clicks[0], clicks[1]) is True:
                    clicks.clear()
                    background = load_image('board_bg.jpg')
                    update_board(screen, background)
                    pygame.display.update()
                    print(game.print_board())

                    # Adds text to game board if a player won.
                    if game.get_game_state() == 'BLACK_WON':
                        font = pygame.font.SysFont('copperplatettc', 20)
                        text1 = font.render("Game Over.", True, red)
                        text2 = font.render("Black Player Wins!", True, red)
                        screen.blit(text1, (295, 675))
                        screen.blit(text2, (255, 700))
                        pygame.display.update()
                    elif game.get_game_state() == 'WHITE_WON':
                        font = pygame.font.SysFont('copperplatettc', 20)
                        text1 = font.render("Game Over.", True, red)
                        text2 = font.render("White Player Wins!", True, red)
                        screen.blit(text1, (295, 675))
                        screen.blit(text2, (255, 700))
                        pygame.display.update()

                # Adds text to game board if move attempt was invalid.
                else:
                    clicks.clear()
                    background = load_image('board_bg.jpg')
                    update_board(screen, background)
                    font = pygame.font.SysFont('sfnsdisplaycondensedregularotf', 20)
                    text = font.render("Invalid selection. Please try again.", True, steel)
                    screen.blit(text, (10, 705))
                    pygame.display.update()


if __name__ == '__main__':
    """
    Initializes game and board objects from GuessGame file. 
    Creates lists for column/row headers and calls main function.
    """
    game = GessGame()
    board = GessBoard()
    positions = board.set_positions()
    letters = [chr(x) for x in range(ord('A'), ord('U'))]
    nums = [n for n in range(1, 21)]
    steel = (10, 10, 60)
    red = (175, 0, 30)
    main()
