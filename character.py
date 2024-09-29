import pygame


def create_char(i, x, y, key):
    sprite_sheet_attack = pygame.image.load(f'Data/character/char{i}/Attack1.png')
    sprite_sheet_run = pygame.image.load(f'Data/character/char{i}/run.png')
    sprite_sheet_jump = pygame.image.load(f'Data/character/char{i}/jump.png')
    sprite_sheet_idle = pygame.image.load(f'Data/character/char{i}/idle.png')
    sprite_sheet_run_attack = pygame.image.load(f'Data/character/char{i}/RunAttack1.png')
    sprite_sheet_squat = pygame.image.load(f'Data/character/char{i}/SquatAttack.png')
    sprite_sheet_walk_attack = pygame.image.load(f'Data/character/char{i}/WalkAttack1.png')

    frame_width = 42
    frame_height = 42

    attack = [pygame.transform.scale(sprite_sheet_attack.subsurface((i * frame_width, 0), (frame_width, frame_height)),
                                     (126, 126)) for i in range(6)]
    run = [pygame.transform.scale(sprite_sheet_run.subsurface((i * frame_width, 0), (frame_width, frame_height)),
                                  (126, 126)) for i in range(6)]
    jump = [pygame.transform.scale(sprite_sheet_jump.subsurface((i * frame_width, 0), (frame_width, frame_height)),
                                   (126, 126)) for i in range(8)]
    idle = [pygame.transform.scale(sprite_sheet_idle.subsurface((i * frame_width, 0), (frame_width, frame_height)),
                                   (126, 126)) for i in range(4)]
    run_attack = [
        pygame.transform.scale(sprite_sheet_run_attack.subsurface((i * frame_width, 0), (frame_width, frame_height)),
                               (126, 126)) for i in range(6)]
    squat = [pygame.transform.scale(sprite_sheet_squat.subsurface((i * frame_width, 0), (frame_width, frame_height)),
                                    (126, 126)) for i in range(6)]
    walk_attack = [
        pygame.transform.scale(sprite_sheet_walk_attack.subsurface((i * frame_width, 0), (frame_width, frame_height)),
                               (126, 126)) for i in range(6)]

    sprite = Character(x, y, key, attack, run, jump, idle, run_attack, squat, walk_attack)
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
        # Key
        self.key = key
        self.prev_key = key[0]
        # Chỉ so
        self.health = 200
        self.mana = 30
        self.base_atk = 5

    def flip_frame(self, frame, counter):
        if self.prev_key != self.key[1]:
            self.image = frame[counter]
        else:
            self.image = pygame.transform.flip(frame[counter], True, False)

    def update_prev_key(self, key, dis):
        if key[self.key[1]]:
            self.rect.x = max(0, self.rect.x - dis)
            self.prev_key = self.key[1]
        if key[self.key[2]]:
            self.rect.x = min(1300 - 126, self.rect.x + dis)
            self.prev_key = self.key[2]

    def update(self):
        key = pygame.key.get_pressed()
        # Jump
        if key[self.key[4]] or self.rect.y != 380:
            self.flip_frame(self.jump_frame, self.jump_counter)
            self.rect.y = 380 - self.jump_counter * (7 - self.jump_counter) * 10
            self.update_prev_key(key, 15)
            self.jump_counter = update_counter(self.jump_counter, 7)
            pygame.time.delay(25)
        # squat attack
        elif key[self.key[5]]:
            self.flip_frame(self.squat_frame, self.squat_counter)
            self.update_prev_key(key, 15)
            self.squat_counter = update_counter(self.squat_counter, 5)
            pygame.time.delay(30)
        # run
        elif key[self.key[1]] or key[self.key[2]]:
            if key[self.key[3]]:
                self.flip_frame(self.run_attack_frame, self.run_Counter)
            else:
                self.flip_frame(self.run_frame, self.run_Counter)
            self.update_prev_key(key, 15)
            self.run_Counter = update_counter(self.run_Counter, 5)
        # attack
        elif key[self.key[3]]:
            self.flip_frame(self.attack_frame, self.attack_counter)
            self.attack_counter = update_counter(self.attack_counter, 5)
        # idle
        else:
            self.flip_frame(self.idle_frame, self.idle_counter)
            self.idle_counter = update_counter(self.idle_counter, 3)

    def fight(self, char2):
        key = pygame.key.get_pressed()
        if self.rect.colliderect(char2.rect):
            if key[pygame.K_j] or key[pygame.K_s]:
                char2.health -= 10
            if key[pygame.K_KP1] or key[pygame.K_DOWN]:
                self.health -= 10
