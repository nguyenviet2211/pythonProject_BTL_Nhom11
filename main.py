import pygame
import character
import threading
import sys

pygame.init()
clock = pygame.time.Clock()
x1, x2, x3 = 0, 0, 0
color1, color2 = (255, 255, 255), (100, 100, 100)
Font = pygame.font.SysFont("Press Start 2P", 40)
key_player_1 = [pygame.K_d, pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_w, pygame.K_s]
key_player_2 = [pygame.K_LEFT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP1, pygame.K_UP, pygame.K_DOWN]
Background_info = [360, 500]
screen_width, screen_height = (pygame.display.get_desktop_sizes()[0][0] - 100,
                               pygame.display.get_desktop_sizes()[0][1] - 100)
screen = pygame.display.set_mode((screen_width, screen_height))


def load_image(image, w, h):
    return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (w, h))


def black_blur():
    blur = pygame.Surface((screen_width, screen_height))
    blur.fill((0, 0, 0))
    blur.set_alpha(120)
    screen.blit(blur, (0, 0))
    blur.set_alpha(None)


# load data
Background = [load_image(f"Data/Background/Background{i}.jpg", screen_width, screen_height) for i in range(2)]
Menu = load_image("Data/Background3.jpg", screen_width, screen_height)
Button = load_image("Data/game_button/buttons-3.png", 200, 50)
left_arrow = load_image("Data/game_button/buttons-4.png", 35, 50)
right_arrow = load_image("Data/game_button/buttons-6.png", 35, 50)
Char = [load_image(f"Data/character/char{i}/avatar.png", 100, 100) for i in range(3)]
name_character = ["monster", "rabbit", "snow man"]


def draw_text(x, y, Text, button=None, TextColor=(0, 0, 0), bg_color=None):
    text = Font.render(Text, True, TextColor)
    rect = textRect = text.get_rect()
    textRect.center = (x, y)
    if bg_color is not None:
        pygame.draw.rect(screen, bg_color, rect)
    if button is not None:
        rect = button.get_rect()
        rect.center = (x, y)
        screen.blit(button, rect)
    screen.blit(text, textRect)
    if button is not None:
        return rect
    return textRect


def draw_health_bar(x, y, char):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, char.health, 20))


def draw_char(sprite, x, i, char):
    sprite.update()
    sprite.draw(screen)
    textRect = draw_text(x, 50, f"Player {i}", None, (255, 255, 255))
    draw_health_bar(x - textRect.width / 2, 90, char)


def draw_arrow():
    left_arrow_char1 = draw_text(screen_width / 5 - 50, screen_height / 4 * 3, "", left_arrow)
    right_arrow_char1 = draw_text(screen_width / 5 + 50, screen_height / 4 * 3, "", right_arrow)
    left_arrow_background = draw_text(screen_width / 2 - 50, screen_height / 4 * 3, "", left_arrow)
    right_arrow_background = draw_text(screen_width / 2 + 50, screen_height / 4 * 3, "", right_arrow)
    left_arrow_char2 = draw_text(screen_width / 5 * 4 - 50, screen_height / 4 * 3, "", left_arrow)
    right_arrow_char2 = draw_text(screen_width / 5 * 4 + 50, screen_height / 4 * 3, "", right_arrow)
    return [left_arrow_char1, left_arrow_char2, right_arrow_char1,
            right_arrow_char2, left_arrow_background, right_arrow_background]


def menu():
    pygame.display.flip()
    pygame.display.set_caption("2P game")
    color = [color1, color1, color1]

    Exit = False
    while not Exit:
        screen.blit(Menu, (0, 0))
        start_button = draw_text(screen_width / 2, screen_height / 2 - 60, "START", Button, color[0])
        _2P_ = draw_text(screen_width / 2, screen_height / 2, "2P", Button, color[1])
        exit_button = draw_text(screen_width / 2, screen_height / 2 + 60, "EXIT", Button, color[2])
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True
            if start_button.collidepoint(mouse_pos):
                color[0] = color2
                if event.type == pygame.MOUSEBUTTONUP:
                    play_game(Background[x3])
                    color[0] = color1
            elif _2P_.collidepoint(mouse_pos):
                color[1] = color2
                if event.type == pygame.MOUSEBUTTONUP:
                    _2p_mode()
            elif exit_button.collidepoint(mouse_pos):
                color[2] = color2
                if event.type == pygame.MOUSEBUTTONUP:
                    Exit = True
            else:
                color[0], color[1], color[2] = color1, color1, color1

        pygame.display.update()

    pygame.quit()
    sys.exit()


def _2p_mode():
    rect1 = pygame.Rect(0, 0, 100, 100)
    rect2 = pygame.Rect(0, 0, 100, 100)
    rect_background = pygame.Rect(0, 0, 300, 150)
    rect1.center = (screen_width / 5, screen_height / 2)
    rect2.center = (screen_width / 5 * 4, screen_height / 2)
    rect_background.center = (screen_width / 2, screen_height / 2)
    global x1, x2, x3
    color = color1
    list_arrow = draw_arrow()
    Exit = False
    while not Exit:
        screen.fill((0, 0, 0))
        draw_text(screen_width / 2, screen_height / 4, "Map", None, color1)
        draw_text(screen_width / 5, screen_height / 4, name_character[x1], None, color1)
        draw_text(screen_width / 5 * 4, screen_height / 4, name_character[x2], None, color1)
        draw_arrow()
        start = draw_text(screen_width / 2, screen_height - 100, "START", Button, color)
        mouse = pygame.mouse.get_pos()
        screen.blits((
            (Char[x1], rect1),
            (Char[x2], rect2),
            (pygame.transform.scale(Background[x3], (300, 150)), rect_background))
        )
        pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.QUIT])
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                Exit = True
            if start.collidepoint(mouse):
                color = color2
                if even.type == pygame.MOUSEBUTTONUP:
                    play_game(Background[x3])
                    screen.fill(color1)
                    draw_arrow()
            else:
                color = color1

            if even.type == pygame.MOUSEBUTTONDOWN:
                if list_arrow[0].collidepoint(mouse):
                    x1 = (x1 + 2) % 3
                if list_arrow[1].collidepoint(mouse):
                    x2 = (x2 + 2) % 3
                if list_arrow[2].collidepoint(mouse):
                    x1 = (x1 + 1) % 3
                if list_arrow[3].collidepoint(mouse):
                    x2 = (x2 + 1) % 3
                if list_arrow[4].collidepoint(mouse):
                    x3 = (x3 + 1) % 2
                if list_arrow[5].collidepoint(mouse):
                    x3 = (x3 + 1) % 2

        pygame.display.update()


def play_game(background):
    # load character
    char1 = character.create_char(x1, key_player_1, 100, Background_info[x3])
    char2 = character.create_char(x2, key_player_2, 1100, Background_info[x3])
    Group1 = pygame.sprite.Group(char1)
    Group2 = pygame.sprite.Group(char2)
    e = False
    while not e:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                e = True
        screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
        p1 = threading.Thread(target=draw_char(Group1, 100, 1, char1))
        p2 = threading.Thread(target=draw_char(Group2, 1100, 2, char2))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        char1.fight(char2)
        if not char1.alive or not char2.alive:
            black_blur()
            draw_text(screen_width / 2, screen_height / 2, "GAME OVER", None, (255, 255, 255))
        pygame.display.update()
        clock.tick(30)  # FPS


if __name__ == '__main__':
    menu()
