import pygame
import character
import threading
import sys

pygame.init()
pos = (0, 0)
screen_width = 1300
screen_height = 700
Font = pygame.font.SysFont("Arial", 40)
key_player_1 = [pygame.K_d, pygame.K_a, pygame.K_d, pygame.K_j, pygame.K_w, pygame.K_s]
key_player_2 = [pygame.K_LEFT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP1, pygame.K_UP, pygame.K_DOWN]


# Set background
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Mortal Combat")
Background1 = pygame.transform.scale(pygame.image.load("Data/Background1.jpg"), (screen_width, screen_height))
Background2 = pygame.transform.scale(pygame.image.load("Data/Background2.jpg"), (screen_width, screen_height))
Menu = pygame.transform.scale(pygame.image.load("Data/Menu.png"), (screen_width, screen_height))


# Thread


def draw_text(x, y, Text, Color):
    text = Font.render(Text, True, Color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)
    return textRect


def draw_health_bar(x, y, char):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, char.health, 20))


def draw_char(sprite, x, i, char):
    sprite.update()
    sprite.draw(screen)
    textRect = draw_text(x, 50, f"Player {i}", (255, 255, 255))
    draw_health_bar(x - textRect.width/2, 90, char)


def game(background):
    # load character
    char1 = character.create_char(1, 100, 380, key_player_1)
    char2 = character.create_char(2, 1100, 380, key_player_2)
    player1 = pygame.sprite.Group(char1)
    player2 = pygame.sprite.Group(char2)

    e = False
    while not e:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                e = True
        screen.blit(background, (0, 0))
        p1 = threading.Thread(target=draw_char(player1, 100, 1, char1))
        p2 = threading.Thread(target=draw_char(player2, 1100, 2, char2))

        p1.start()
        p2.start()
        char1.fight(char2)
        p1.join()
        p2.join()
        if not char1.alive or not char2.alive:
            draw_text(screen_width/2, screen_height/2, "GAME OVER", (255, 255, 255))

        pygame.display.update()
        clock.tick(24)  # FPS


# game loop
clock = pygame.time.Clock()
color = (255, 255, 255)
Exit = False
while not Exit:
    screen.blit(Menu, (0, 0))
    start = draw_text(screen_width / 2, screen_height / 2, "START", color)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True
            sys.exit()
        if start.collidepoint(mouse_pos):
            color = (100, 100, 100)
            if event.type == pygame.MOUSEBUTTONUP:
                game(Background2)
        else:
            color = (255, 255, 255)

    pygame.display.update()

pygame.quit()
