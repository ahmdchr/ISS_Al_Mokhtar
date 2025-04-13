import pygame,math

class Enemy():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect((x,y, 80,180))
        self.update_time = pygame.time.get_ticks()
        self.Flip = flip
        self.action = 0 
        self.frame_index = 0
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
        self.attack_move = 0
        self.running = False
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.dead = False
        self.health = 1000

    def load_images(self, images_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
           temp_img_list = []
           for x in range(animation):
             temp_image = images_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
             temp_img_list.append(pygame.transform.scale(temp_image, (self.size * self.image_scale,self.size * self.image_scale)))
           animation_list.append(temp_img_list)
        return animation_list

    def get_target_status(self,target):
        # ensure players face each other 
        if (target.rect.x - self.rect.x >= -20) and not self.dead: 
            self.attack_move = True
        else: 
            self.attack_move = False

        if target.rect.centerx - self.rect.centerx <= 100:
                self.Flip = True
        else:
                self.Flip = False

    def update(self,screen,target):
        animation_cooldown = 350
        if self.health == 0:
            self.dead = True
            self.attack_move = False
        if self.attack_move == True and target.attacking == True:
           self.update_action(4)
           self.attack(screen,target)
        if self.dead == True and target.attacking == True:
           self.update_action(6)

        if self.dead == True:
            self.image = self.animation_list[6][6]
        else:
            if target.dead == True:
                self.image = self.animation_list[self.action][1]
            else:
                self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def move(self,target):
        SPEED = 3
        # AI bot follows the player
        # Calculate direction from the bot to the player
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)  # Euclidean distance

        # Normalize the direction vector to keep speed consistent
        if distance != 0:
            dx /= distance
            dy /= distance

        # Move the bot towards the player
        self.rect.x += dx * SPEED
        self.rect.y += dy * SPEED

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self,surface):
        img = pygame.transform.flip(self.image, self.Flip , False)
        surface.blit(img, (self.rect.x - (self.offset[0]* self.image_scale),self.rect.y - (self.offset[1]* self.image_scale)))

    def attack(self,surface,target):
        attacking_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.Flip), self.rect.y, self.rect.width-30, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 5
