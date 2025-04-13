import pygame,math

class Enemy():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect(x,y, 80,180)
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
        self.health = 100

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
        # ensure bot only attacks when target is nearby 
        if not self.dead and (self.rect.x - target.rect.x <= 100) and (self.rect.x - target.rect.x >=0) and (target.rect.centerx < self.rect.centerx): 
            self.attack_move = True
        if not self.dead and (target.rect.x - self.rect.x <= 100) and (target.rect.x - self.rect.x >=0) and (target.rect.centerx > self.rect.centerx): 
            self.attack_move = True
        
        # ensure players face each other 
        if (target.rect.x <= self.rect.x):
            self.Flip = True
        else:
            self.Flip = False

    def update(self,screen,target):
        animation_cooldown = 300
        
        # if self.health == 0:
        #     self.dead = True
        #     self.attack_move = False
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

    # AI bot follows the player
    def move(self,target):
        SPEED = 3
        # Calculate direction from the bot to the player
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)  # Euclidean distance

        # Keep a small distance between the player and the bot
        if distance > 93:
             dx /= distance
             dy /= distance
             self.rect.x += dx*SPEED
             self.rect.y += dy*SPEED
        else:   
            # if the bot reached the target, we maintain the same position.
            pass

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self,surface):
        pygame.draw.rect(surface, (0,100,100), self.rect)
        img = pygame.transform.flip(self.image, self.Flip , False)
        surface.blit(img, (self.rect.x - (self.offset[0]* self.image_scale),self.rect.y - (self.offset[1]* self.image_scale)))

    def attack(self,surface,target):
        # attacking_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.Flip), self.rect.y, self.rect.width-30, self.rect.height)
        # attacking_rect_1 = pygame.Rect(self.rect.x - 100, self.rect.y, self.rect.width, self.rect.height)
        animation_cooldown = 500
        if self.Flip:
            attacking_rect_2 = pygame.Rect(self.rect.centerx - 110, self.rect.y + 30, self.rect.width - 10, self.rect.height - 30)
        else:
            attacking_rect_2 = pygame.Rect(self.rect.centerx + 40, self.rect.y + 30, self.rect.width - 10, self.rect.height - 30)

        # pygame.draw.rect(surface,(0,0,255),attacking_rect_2)
        # if attacking_rect_1.colliderect(target.rect):
        #     target.health -= 0
        #     pygame.draw.rect(surface,(0,0,255),attacking_rect_1)
        if attacking_rect_2.colliderect(target.rect):
            target.health -= 10
            # pygame.draw.rect(surface,(0,0,255),attacking_rect_2)

       
        
