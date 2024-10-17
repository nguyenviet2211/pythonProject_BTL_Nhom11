import pygame


def sprite_list(sprite, num_frame):
    width = sprite.get_width()/num_frame
    height = sprite.get_height()
    n = int(width/height)
    return [pygame.transform.scale(
        sprite.subsurface((i * width, 0), (width, height)), (126, 126)) for i in range(num_frame)]


def image(Image):
    return pygame.image.load(Image)


def create_char(i, key, x, ground, num_frame):
    sprite_sheet_attack = image(f'Data/character/char{i}/attack.png')
    sprite_sheet_run = image(f'Data/character/char{i}/run.png')
    sprite_sheet_jump = image(f'Data/character/char{i}/jump.png')
    sprite_sheet_idle = image(f'Data/character/char{i}/idle.png')
    sprite_sheet_run_attack = image(f'Data/character/char{i}/RunAttack.png')
    sprite_sheet_die = image(f'Data/character/char{i}/Death.png')

    attack = sprite_list(sprite_sheet_attack, num_frame[0])
    run = sprite_list(sprite_sheet_run, num_frame[1])
    jump = sprite_list(sprite_sheet_jump, num_frame[2])
    idle = sprite_list(sprite_sheet_idle, num_frame[3])
    run_attack = sprite_list(sprite_sheet_run_attack, num_frame[4])
    death = sprite_list(sprite_sheet_die, num_frame[5])

    sprite = Character(num_frame, key, x,  ground, attack, run, jump, idle, run_attack, death)
    return sprite


def update_counter(counter, num_frame) -> int:
    counter += 1
    if counter == num_frame:
        return 0
    return counter


class Character(pygame.sprite.Sprite):
    def __init__(self, num_frame, key, x, ground,  *frame):
        super().__init__()
        # frame
        self.attack_frame = frame[0]
        self.run_frame = frame[1]
        self.jump_frame = frame[2]
        self.idle_frame = frame[3]
        self.run_attack_frame = frame[4]
        self.death = frame[5]
        self.image = self.idle_frame[0]
        self.rect = self.image.get_rect()
        self.animation_speed = 4
        # counter
        self.attack_counter = 0
        self.run_Counter = 0
        self.jump_counter = 0
        self.idle_counter = 0
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
        self.rect.x = x
        self.rect.y = ground
        self.ground = ground
        self.num_frame = num_frame
        self.animation_speed = 10
        self.width = pygame.display.get_desktop_sizes()[0][0] - 226

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
            self.rect.x = min(self.width, self.rect.x + dis)
            self.prev_key = self.key[2]

    def update(self):
        if self.health > 0:
            key = pygame.key.get_pressed()
            # Jump
            if key[self.key[4]] or self.rect.y != self.ground:
                self.update_image(self.jump_frame, self.jump_counter)
                self.rect.y = self.ground - self.jump_counter * (7 - self.jump_counter) * 15
                self.update_prev_key(key, 15)
                self.jump_counter = update_counter(self.jump_counter, self.num_frame[2])
                pygame.time.delay(35)
            # squat attack
            # run
            elif key[self.key[1]] or key[self.key[2]]:
                if key[self.key[3]]:
                    self.update_image(self.run_attack_frame, self.run_Counter)
                else:
                    self.update_image(self.run_frame, self.run_Counter)
                self.update_prev_key(key, 15)
                self.run_Counter = update_counter(self.run_Counter, self.num_frame[1])
            # attack
            elif key[self.key[3]]:
                self.update_image(self.attack_frame, self.attack_counter)
                self.attack_counter = update_counter(self.attack_counter, self.num_frame[0])
            # idle
            else:
                self.update_image(self.idle_frame, self.idle_counter)
                self.idle_counter = update_counter(self.idle_counter, self.num_frame[3])
        elif self.death_counter < self.num_frame[5]:
            self.update_image(self.death, self.death_counter)
            self.death_counter += 1
            pygame.time.delay(50)
        else:
            self.alive = False

    def fight(self, char2):
        key = pygame.key.get_pressed()
        if pygame.sprite.collide_mask(self, char2):
            if (key[pygame.K_j]) and self.alive:
                char2.health -= self.base_atk
            if (key[pygame.K_KP1]) and char2.alive:
                self.health -= char2.base_atk
