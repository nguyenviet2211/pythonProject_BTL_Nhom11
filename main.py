import pygame
import character
import threading
import sys

pygame.init()
screen_width, screen_height = 1300, 700
Font = pygame.font.SysFont("Press Start 2P", 40)
key_player_1 = [pygame.K_d, pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_w, pygame.K_s]
key_player_2 = [pygame.K_LEFT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP1, pygame.K_UP, pygame.K_DOWN]


def load_image(image, w, h):
    return pygame.transform.scale(pygame.image.load(image).convert_alpha(), (w, h))


def black_blur():
    blur = pygame.Surface((screen_width, screen_height))
    blur.fill((0, 0, 0))
    blur.set_alpha(120)
    screen.blit(blur, (0, 0))


# load data
screen = pygame.display.set_mode((screen_width, screen_height))
Background = [load_image(f"Data/Background/Background{i}.jpg", screen_width, screen_height) for i in range(1, 3)]
Background_info = [500, 380]
Menu = load_image("Data/Background3.jpg", screen_width, screen_height)
cloud = [load_image(f"Data/cloud/{i}.png", 300, 100) for i in range(1, 10)]
cloud_position = [100 * i for i in range(1, 10)]
Button = load_image("Data/game_button/buttons-1.png", 200, 50)
clock = pygame.time.Clock()
name_character = ["rabbit", "snow man", "monster"]
x1, x2, x3 = 1, 3, 0
color1, color2 = (255, 255, 255), (100, 100, 100)


def draw_text(x, y, Text, Color, button=None):
    text = Font.render(Text, True, Color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    if button is not None:
        rect = button.get_rect()
        rect.center = (x, y)
        screen.blit(button, rect)
    screen.blit(text, textRect)
    return textRect


def draw_health_bar(x, y, char):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, char.health, 20))


def draw_char(sprite, x, i, char):
    sprite.update()
    sprite.draw(screen)
    textRect = draw_text(x, 50, f"Player {i}", (255, 255, 255))
    draw_health_bar(x - textRect.width / 2, 90, char)


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
        char1.fight(char2)
        p1.join()
        p2.join()
        if not char1.alive or not char2.alive:
            black_blur()
            draw_text(screen_width / 2, screen_height / 2, "GAME OVER", (255, 255, 255))

        pygame.display.update()
        clock.tick(24)  # FPS


def _2p_mode():
    screen.fill((0, 0, 0))
    color = color1
    Exit = False
    while not Exit:
        oke = draw_text(screen_width / 2, screen_height - 100, "OKE", color, Button)
        mouse = pygame.mouse.get_pos()

        draw_text()

        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                Exit = True
            if oke.collidepoint(mouse):
                color = color2
                if even.type == pygame.MOUSEBUTTONUP:
                    Exit = True
            else:
                color = color1

            pygame.display.update()


def menu():
    pygame.display.flip()
    pygame.display.set_caption("2P game")
    color = [color1, color1, color1]

    Exit = False
    while not Exit:
        screen.blit(Menu, (0, 0))
        start_button = draw_text(screen_width / 2, screen_height / 2 - 60, "START", color[0], Button)
        _2P_ = draw_text(screen_width / 2, screen_height / 2, "2P", color[1], Button)
        exit_button = draw_text(screen_width / 2, screen_height / 2 + 60, "EXIT", color[2], Button)
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
                pass

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    menu()
