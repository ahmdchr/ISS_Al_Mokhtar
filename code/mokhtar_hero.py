import pygame

class Fighter():
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
        self.attack_move = False
        self.running = False
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.attacking = False
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
    
    def draw(self,surface):
        if self.dead == True:
            img = pygame.transform.rotate(self.image, -90)
        else:
            img = pygame.transform.flip(self.image, self.Flip , False)
        surface.blit(img, (self.rect.x - (self.offset[0]* self.image_scale),self.rect.y - (self.offset[1]* self.image_scale)))
        
    def move(self,screen_width,screen_height,screen,target):
        SPEED = 3
        RUNNING_SPEED = 5
        delta_x = 0
        delta_y = 0
        self.running = False
        self.moving_up = False
        self.moving_down = False 
        self.moving_right = False
        self.moving_left = False
        self.attack_move = False
        self.Flip = False

        key = pygame.key.get_pressed()
        if self.dead == False and target.dead == False:
            if self.attacking == False:
                if key[pygame.K_q]:
                    self.running = True
                if key[pygame.K_a] or key[pygame.K_LEFT]:
                    delta_x -= SPEED
                    self.moving_left = True
                if key[pygame.K_d] or key[pygame.K_RIGHT]:
                    delta_x += SPEED
                    self.moving_right = True
                if key[pygame.K_w] or key[pygame.K_UP]:
                    delta_y -= SPEED
                    self.moving_up = True
                if key[pygame.K_s] or key[pygame.K_DOWN]:
                    delta_y += SPEED
                    self.moving_down = True
                if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.running == True:
                    delta_x -= RUNNING_SPEED
                if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.running == True:
                    delta_x += RUNNING_SPEED
                if (key[pygame.K_w] or key[pygame.K_UP]) and self.running == True:
                    delta_y -= RUNNING_SPEED
                if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.running == True:
                    delta_y += RUNNING_SPEED
                if key[pygame.K_1]:
                    self.attacking = True    
            else:
                if key[pygame.K_q]:
                    self.running = True
                if key[pygame.K_a] or key[pygame.K_LEFT]:
                    delta_x -= SPEED
                    self.moving_left = True
                if key[pygame.K_d] or key[pygame.K_RIGHT]:
                    delta_x += SPEED
                    self.moving_right = True
                if key[pygame.K_w] or key[pygame.K_UP]:
                    delta_y -= SPEED
                    self.moving_up = True
                if key[pygame.K_s] or key[pygame.K_DOWN]:
                    delta_y += SPEED
                    self.moving_down = True
                if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.running == True:
                    delta_x -= RUNNING_SPEED
                if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.running == True:
                    delta_x += RUNNING_SPEED
                if (key[pygame.K_w] or key[pygame.K_UP]) and self.running == True:
                    delta_y -= RUNNING_SPEED
                if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.running == True:
                    delta_y += RUNNING_SPEED
                if key[pygame.K_r]:
                    self.attack_move = True
                    self.attack(screen,target)
                if key[pygame.K_1]:
                    self.attacking = False
                
            # ensure player stays on screen
            if self.rect.left + delta_x < 0:
                    delta_x = -self.rect.left
            if self.rect.right + delta_x > screen_width:
                    delta_x = screen_width - self.rect.right
            if self.rect.top + delta_y < 0:
                    delta_y = -self.rect.top
            if self.rect.bottom + delta_y > screen_height:
                    delta_y = screen_height - self.rect.bottom
            if (120 + target.rect.right) >= screen_width:
                    delta_x = screen_width - target.rect.right - 120 - 10

                
            # ensure players face each other 
            if target.rect.x - self.rect.x <= -80:
                    self.Flip = True
            else:
                    self.Flip = False
        
            self.rect.x += delta_x
            self.rect.y += delta_y
        
    # handle animation updates
    def update(self,screen):
        animation_cooldown = 350
        if self.health ==0:
            self.dead = True
            self.image = self.animation_list[6][0]
        if self.attacking == False:
            self.update_action(0)
            if  self.moving_up == True:
                self.update_action(2)
            if self.moving_up == True and self.running == True:
                self.update_action(5)
            if self.moving_down == True:
                self.update_action(0)
            if self.moving_down == True and self.running == True:
                self.update_action(3)
            if  self.moving_right == True:
                self.update_action(1)
            if self.moving_right and self.running == True:
                self.update_action(4)
            if self.moving_left == True:
                self.update_action(1)
                self.Flip = True
                self.draw(screen)
            if self.moving_left == True and self.running == True:
                self.update_action(4)
            self.image = self.animation_list[self.action][self.frame_index]

            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0
        else:
            self.update_action(6)
            if self.moving_down == True:
                self.update_action(6)
            if self.moving_right == True:
                self.update_action(8)
            if self.moving_left == True:
                self.update_action(8)
                self.Flip = True
                self.draw(screen)
            if self.moving_up == True:
                self.update_action(10)
            if self.attack_move:
                self.update_action(7)
            if self.attack_move and self.moving_up == True:
                self.update_action(11)
            if self.attack_move and self.moving_down == True:
                self.update_action(7)
            if self.attack_move and self.moving_right == True:
                self.update_action(9)
            if self.attack_move and self.moving_left == True:
                self.update_action(9)
                self.Flip = True
                self.draw(screen)
           
            self.image = self.animation_list[self.action][self.frame_index]

            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()
                    if self.frame_index >= len(self.animation_list[self.action]):
                        self.frame_index = 0
    
    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def attack(self,surface,target):
        attacking_rect = pygame.Rect(self.rect.centerx - (self.rect.width * self.Flip), self.rect.y, 2*self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
         target.health -= 5
     
        


