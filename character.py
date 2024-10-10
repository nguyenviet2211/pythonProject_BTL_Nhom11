import pygame


def sprite_list(sprite, n, width, height):
    return [pygame.transform.scale(sprite.subsurface((i * width, 0), (width, height)), (126, 126)) for i in range(n)]


def image(Image):
    return pygame.image.load(Image)


def create_char(i, x, y, key):
    sprite_sheet_attack = image(f'Data/character/char{i}/Attack1.png')
    sprite_sheet_run = image(f'Data/character/char{i}/run.png')
    sprite_sheet_jump = image(f'Data/character/char{i}/jump.png')
    sprite_sheet_idle = image(f'Data/character/char{i}/idle.png')
    sprite_sheet_run_attack = image(f'Data/character/char{i}/RunAttack1.png')
    sprite_sheet_squat_attack = image(f'Data/character/char{i}/SquatAttack.png')
    sprite_sheet_walk_attack = image(f'Data/character/char{i}/WalkAttack1.png')
    sprite_sheet_die = image(f'Data/character/char{i}/Death.png')

    frame_width = 42
    frame_height = 42

    attack = sprite_list(sprite_sheet_attack, 6, frame_width, frame_height)
    run = sprite_list(sprite_sheet_run, 6, frame_width, frame_height)
    jump = sprite_list(sprite_sheet_jump, 8, frame_width, frame_height)
    idle = sprite_list(sprite_sheet_idle, 4, frame_width, frame_height)
    run_attack = sprite_list(sprite_sheet_run_attack, 6, frame_width, frame_height)
    squat_attack = sprite_list(sprite_sheet_squat_attack, 6, frame_width, frame_height)
    walk_attack = sprite_list(sprite_sheet_walk_attack, 6, frame_width, frame_height)
    death = sprite_list(sprite_sheet_die, 9, frame_width, frame_height)

    sprite = Character(x, y, key, attack, run, jump, idle, run_attack, squat_attack, walk_attack, death)
    return sprite


def update_counter(counter, num_frame) -> int:
    counter += 1
    if counter > num_frame:
        return 0
    return counter


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, key, *frame):
        super().__init__()
        # frame
        self.attack_frame = frame[0]
        self.run_frame = frame[1]
        self.jump_frame = frame[2]
        self.idle_frame = frame[3]
        self.run_attack_frame = frame[4]
        self.squat_frame = frame[5]
        self.walk_attack_frame = frame[6]
        self.death = frame[7]
        self.image = self.idle_frame[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_speed = 4
        # counter
        self.attack_counter = 0
        self.run_Counter = 0
        self.jump_counter = 0
        self.idle_counter = 0
        self.squat_counter = 0
        self.fall_attack_counter = 0
        self.death_counter = 0
        # Key
        self.key = key
        self.prev_key = key[0]
        # Chỉ so
        self.health = 200
        self.mana = 30
        self.base_atk = 5
        self.alive = True

    def update_image(self, frame, counter):
        if self.prev_key != self.key[1]:
            self.image = frame[counter]
        else:
            self.image = pygame.transform.flip(frame[counter], True, False)

    def update_prev_key(self, key, dis):
        if key[self.key[1]]:
            self.rect.x = max(0, self.rect.x - dis)
            self.prev_key = self.key[1]
        elif key[self.key[2]]:
            self.rect.x = min(1300 - 126, self.rect.x + dis)
            self.prev_key = self.key[2]

    def update(self):
        if self.health > 0:
            key = pygame.key.get_pressed()
            # Jump
            if key[self.key[4]] or self.rect.y != 380:
                self.update_image(self.jump_frame, self.jump_counter)
                self.rect.y = 380 - self.jump_counter * (7 - self.jump_counter) * 15
                self.update_prev_key(key, 15)
                self.jump_counter = update_counter(self.jump_counter, 7)
                pygame.time.delay(25)
            # squat attack
            elif key[self.key[5]]:
                self.update_image(self.squat_frame, self.squat_counter)
                self.update_prev_key(key, 15)
                self.squat_counter = update_counter(self.squat_counter, 5)
            # run
            elif key[self.key[1]] or key[self.key[2]]:
                if key[self.key[3]]:
                    self.update_image(self.run_attack_frame, self.run_Counter)
                else:
                    self.update_image(self.run_frame, self.run_Counter)
                self.update_prev_key(key, 15)
                self.run_Counter = update_counter(self.run_Counter, 5)
            # attack
            elif key[self.key[3]]:
                self.update_image(self.attack_frame, self.attack_counter)
                self.attack_counter = update_counter(self.attack_counter, 5)
            # idle
            else:
                self.update_image(self.idle_frame, self.idle_counter)
                self.idle_counter = update_counter(self.idle_counter, 3)
        elif self.death_counter < 9:
            self.update_image(self.death, self.death_counter)
            self.death_counter += 1
            pygame.time.delay(50)
        else:
            self.alive = False

    def fight(self, char2):
        key = pygame.key.get_pressed()
        if pygame.sprite.collide_mask(self, char2):
            if (key[pygame.K_j] or key[pygame.K_s]) and self.alive:
                char2.health -= self.base_atk
            if (key[pygame.K_KP1] or key[pygame.K_DOWN]) and char2.alive:
                self.health -= char2.base_atk
