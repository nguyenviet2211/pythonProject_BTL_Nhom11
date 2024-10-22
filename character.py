import pygame

"""so frame cua skill"""
NumSkillFrame = [97, 97, 97, 97, ]
"""kich thuoc skill"""
sizeSkill = [(200, 150), (126, 126), (126, 126), (70, 70)]


def frame_list(Image, num_frame, w, h):
    width = Image.get_width() / num_frame
    height = Image.get_height()
    return [pygame.transform.scale(
        Image.subsurface((i * width, 0), (width, height)), (w, h)) for i in range(num_frame)]


def image(Image):
    return pygame.image.load(Image)


SkillFrame = [
    frame_list(image(f"Data/character/char{i}/skill2.png"), NumSkillFrame[i], sizeSkill[i][0], sizeSkill[i][1])
    for i in range(4)]

FlipSkillFrame = [frame_list(image(f"Data/character/char{i}/skill.png"),
                             NumSkillFrame[i],
                             sizeSkill[i][0], sizeSkill[i][1])
                  for i in range(4)]


def create_char(i, key, x, ground, num_frame, h):
    sprite_sheet_attack = image(f'Data/character/char{i}/attack.png')
    sprite_sheet_run = image(f'Data/character/char{i}/run.png')
    sprite_sheet_jump = image(f'Data/character/char{i}/jump.png')
    sprite_sheet_idle = image(f'Data/character/char{i}/idle.png')
    sprite_sheet_die = image(f'Data/character/char{i}/Death.png')
    sprite_sheet_use_skill = image(f'Data/character/char{i}/useSkill.png')

    attack = frame_list(sprite_sheet_attack, num_frame[0], h, h)
    run = frame_list(sprite_sheet_run, num_frame[1], h, h)
    jump = frame_list(sprite_sheet_jump, num_frame[2], h, h)
    idle = frame_list(sprite_sheet_idle, num_frame[3], h, h)
    death = frame_list(sprite_sheet_die, num_frame[4], h, h)
    use_skill = frame_list(sprite_sheet_use_skill, num_frame[5], h, h)

    sprite = Character(num_frame, key, x, ground, attack, run, jump, idle, death, use_skill)
    return sprite


def update_counter(counter, num_frame) -> int:
    counter += 1
    if counter == num_frame:
        return 0
    return counter


class Character(pygame.sprite.Sprite):
    def __init__(self, num_frame, key, x, ground, *Frame):
        super().__init__()
        # frame
        self.attack = Frame[0]
        self.run = Frame[1]
        self.jump = Frame[2]
        self.idle = Frame[3]
        self.death = Frame[4]
        self.use_skill = Frame[5]
        self.queue_frame = []
        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        self.animation_speed = 4
        # counter
        self.attack_counter = 0
        self.run_Counter = 0
        self.jump_counter = 0
        self.idle_counter = 0
        self.death_counter = 0
        self.use_skill_counter = 0
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
        self.screenWidth = pygame.display.get_desktop_sizes()[0][0] - 226
        self.using_skill = False
        self.direction = self.prev_key == self.key[0]

    """doi huong cua frame"""

    def update_image(self, frame, counter):
        if self.prev_key != self.key[1]:
            self.image = frame[counter]
        else:
            self.image = pygame.transform.flip(frame[counter], True, False)

    """cap nhat toa do x"""

    def update_prev_key(self, key, dis):
        if key[self.key[1]]:
            self.rect.x = max(0, self.rect.x - dis)
            self.prev_key = self.key[1]
        elif key[self.key[2]]:
            self.rect.x = min(self.screenWidth, self.rect.x + dis)
            self.prev_key = self.key[2]

    def Jump(self):
        self.update_image(self.jump, self.jump_counter)
        self.rect.y = self.ground - self.jump_counter * (7 - self.jump_counter) * 15
        self.jump_counter = update_counter(self.jump_counter, self.num_frame[2])

    def Run(self):
        self.update_image(self.run, self.run_Counter)
        self.run_Counter = update_counter(self.run_Counter, self.num_frame[1])

    def Attack(self):
        self.update_image(self.attack, self.attack_counter)
        self.attack_counter = update_counter(self.attack_counter, self.num_frame[0])

    def Idle(self):
        self.update_image(self.idle, self.idle_counter)
        self.idle_counter = update_counter(self.idle_counter, self.num_frame[3])

    def Die(self):
        self.update_image(self.death, self.death_counter)
        self.death_counter += 1
        pygame.time.delay(50)

    def Use_skill(self):
        self.queue_frame.extend(self.use_skill)

    """key[1] : sang trái"""
    """key[2] : sang phải"""
    """key[3] : đánh thuong"""
    """key[4] : nhảy"""
    """key[5] : dùng skill"""

    def update(self):
        if self.health > 0:
            self.direction = self.prev_key == self.key[0]
            if len(self.queue_frame):
                self.update_image(self.queue_frame, 0)
                self.queue_frame.pop(0)
                if len(self.queue_frame) == 1:
                    self.using_skill = True
                pygame.time.delay(20)
            else:
                self.using_skill = False
                key = pygame.key.get_pressed()
                # Jump
                if key[self.key[4]] or self.rect.y != self.ground:
                    self.Jump()
                # Run
                if key[self.key[1]] or key[self.key[2]]:
                    if key[self.key[4]] or self.rect.y != self.ground:
                        self.Jump()
                    elif key[self.key[3]]:
                        self.Attack()
                    elif key[self.key[5]]:
                        self.Use_skill()
                    else:
                        self.Run()
                    self.update_prev_key(key, 15)
                elif key[self.key[3]]:
                    self.Attack()
                elif key[self.key[5]] and self.mana >= 30:
                    self.Use_skill()
                # idle
                else:
                    self.Idle()
        elif self.death_counter < self.num_frame[4]:
            self.Die()
        else:
            self.alive = False
            self.kill()


class Skill(pygame.sprite.Sprite):
    def __init__(self, i):
        super().__init__()
        self.num_char = i
        self.skill_frame = SkillFrame[i]
        self.flip_skill_frame = FlipSkillFrame[i]
        self.skill_counter = NumSkillFrame[i]
        self.NumFrame = NumSkillFrame[i]
        self.image = self.skill_frame[self.NumFrame - 1]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.direction = True  # quay sang trai

    def update(self, x, y, direction):
        pass

    def reset(self):
        self.skill_counter = self.NumFrame
        self.image = self.skill_frame[self.NumFrame - 1]


class Naruto(Skill):
    def __init__(self, i):
        super().__init__(i)

    def update(self, x, y, d):
        if self.skill_counter != self.NumFrame:
            if not self.direction:
                self.image = self.skill_frame[self.skill_counter]
            else:
                self.image = self.flip_skill_frame[self.skill_counter]
            self.skill_counter += 1
        else:
            if self.direction:
                self.rect.x = x - 100
            else:
                self.rect.x = x + 100
            self.rect.y = y
            self.direction = d


class Monster(Skill):
    def __init__(self, i):
        super().__init__(i)

    def update(self, x, y, d):
        if self.skill_counter != self.NumFrame:
            if not self.direction:
                self.image = self.skill_frame[self.skill_counter]
            else:
                self.image = self.flip_skill_frame[self.skill_counter]
            self.skill_counter += 1
        else:
            self.rect.y = y - 100
            self.rect.x = x
            self.direction = d


def update_skill_frame(Char_skill, x, y, direction):
    Char_skill.update(x, y, direction)


"""kiem tra va cham"""


def collide_check(direction1, direction2, char1, char2):
    width = char1.rect.width
    height = char1.rect.height
    punch_surface = pygame.Surface((width//5, height), pygame.SRCALPHA)
    body_surface = pygame.Surface((width//1.2, height), pygame.SRCALPHA)
    punch_x, punch_y = char1.rect.x, char1.rect.y
    body_x, body_y = char2.rect.x, char2.rect.y
    if direction1:
        punch_surface.blit(char1.image, (0, 0))
    else:
        punch_surface.blit(char1.image, (-width//1.2, 0))
        punch_x += width//1.2

    if direction2:
        body_surface.blit(char2.image, (-width//7, 0))
        body_x += width//7
    else:
        body_surface.blit(char2.image, (0, 0))
    mask_punch = pygame.mask.from_surface(punch_surface)
    mask_body = pygame.mask.from_surface(body_surface)
    offset = (punch_x - body_x, punch_y - body_y)

    return mask_punch.overlap(mask_body, offset)


def fight(char1, char2, char_skill1, char_skill2):
    key = pygame.key.get_pressed()
    if pygame.sprite.collide_mask(char1, char_skill2):
        char1.health -= 1
    if pygame.sprite.collide_mask(char2, char_skill1):
        char2.health -= 1
    if key[pygame.K_j] and char1.alive and collide_check(char1.direction, char2.direction, char1, char2):
        char2.health -= 5
    if key[pygame.K_KP1] and char2.alive and collide_check(char2.direction, char1.direction, char2, char1):
        char1.health -= 5
