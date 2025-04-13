import pygame

class Fighter():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect(x,y, 80,180)
        self.update_time = pygame.time.get_ticks()
        self.Flip = flip
        self.botFlip = False
        self.action = 0 
        self.frame_index = 0
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
        self.attack_move = False
        self.attack_hit = False
        self.running = False
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.attacking = False
        self.dead = False
        self.health = 10
        self.last_r_press_time = 0
        self.attack_cooldown_time = 800
       
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
        # pygame.draw.rect(surface,(0,0,0),self.rect)
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
        # self.attacking = False
        self.Flip = False
        self.botFlip = False

        current_time = pygame.time.get_ticks()
        key = pygame.key.get_pressed()

        # if self.dead == False and target.dead == False:
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
        if key[pygame.K_r]:
            if current_time - self.last_r_press_time >= self.attack_cooldown_time:
                self.attack_move = True
                self.last_r_press_time = current_time  # Update the last press time
            else:
                self.attack_move = False  # Reset attack move when the key is not held down
            
            # self.attack_move = False
            # else:
            #     if key[pygame.K_q]:
            #         self.running = True
            #     if key[pygame.K_a] or key[pygame.K_LEFT]:
            #         delta_x -= SPEED
            #         self.moving_left = True
            #     if key[pygame.K_d] or key[pygame.K_RIGHT]:
            #         delta_x += SPEED
            #         self.moving_right = True
            #     if key[pygame.K_w] or key[pygame.K_UP]:
            #         delta_y -= SPEED
            #         self.moving_up = True
            #     if key[pygame.K_s] or key[pygame.K_DOWN]:
            #         delta_y += SPEED
            #         self.moving_down = True
            #     if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.running == True:
            #         delta_x -= RUNNING_SPEED
            #     if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.running == True:
            #         delta_x += RUNNING_SPEED
            #     if (key[pygame.K_w] or key[pygame.K_UP]) and self.running == True:
            #         delta_y -= RUNNING_SPEED
            #     if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.running == True:
            #         delta_y += RUNNING_SPEED
                
                    # self.attack(screen,target)
                    # return
               

            # ensure player stays on screen
        if self.rect.left + delta_x < 0:
                delta_x = -self.rect.left
        if self.rect.right + delta_x > screen_width:
                delta_x = screen_width - self.rect.right
        if self.rect.top + delta_y < 0:
                delta_y = -self.rect.top
        if self.rect.bottom + delta_y > screen_height:
                delta_y = screen_height - self.rect.bottom
        
        # handle movement animaitions flipping mechanisms  
        if self.attacking:
            if self.moving_right and (self.rect.x - target.rect.x <= 120) and (self.rect.centerx > target.rect.centerx):
                self.botFlip = True
            if self.moving_right and (self.rect.x - target.rect.x > 120) and (self.rect.centerx > target.rect.centerx):
                self.botFlip = False

            if self.moving_left and (target.rect.x - self.rect.x <= 120) and (target.rect.centerx > self.rect.centerx):
                self.botFlip = True
            if self.moving_left and (target.rect.x - self.rect.x > 120) and (target.rect.centerx > self.rect.centerx):
                self.botFlip = False

            if self.moving_up  and (target.rect.y - self.rect.y <= 120) and (target.rect.y > self.rect.y):
                self.botFlip = True

            if self.moving_down and (self.rect.y - target.rect.y <= 120) and (target.rect.y < self.rect.y):
                self.botFlip = True
            
        # handle idle animations flipping mechanism when attacking 
        if self.attacking:
            if (not self.moving_left and not self.moving_down and not self.moving_left and not self.moving_right) and ((self.rect.x - target.rect.x <= 100) and (self.rect.centerx > target.rect.centerx)):
                self.Flip = True

            if (not self.moving_left and not self.moving_down and not self.moving_left and not self.moving_right) and ((self.rect.x - target.rect.x > 100) and (self.rect.centerx > target.rect.centerx)):
                self.Flip = False
                
            if (not self.moving_left and not self.moving_down and not self.moving_left and not self.moving_right) and ((target.rect.x - self.rect.x <= 120) and (self.rect.centerx < target.rect.centerx)):
                self.Flip = False

        self.rect.x += delta_x
        self.rect.y += delta_y

    # handle animation updates
    def update(self,screen,target):
        animation_cooldown = 100
        idle_condition = (not self.moving_down and not self.moving_up and not self.moving_left and not self.moving_right)
        # if self.health ==0:
        #     self.dead = True
        #     self.image = self.animation_list[6][0]

        if not self.attacking:
            if  self.moving_up == True and self.botFlip == False:
                self.update_action(2)
            if  self.moving_up == True and self.botFlip == True:
                self.update_action(0)
            if self.moving_up == True and self.running == True:
                self.update_action(5)
            if self.moving_down == True and self.botFlip == False:
                self.update_action(0)
            if self.moving_down == True and self.botFlip == True:
                self.update_action(2)
            if self.moving_down == True and self.running == True:
                self.update_action(3)
            if  self.moving_right == True and self.botFlip == False:
                self.update_action(1)
            if  self.moving_right == True and self.botFlip == True:
                self.update_action(1)
                self.Flip = True
                self.draw(screen)
            if self.moving_right and self.running == True:
                self.update_action(4)
            if self.moving_left == True and self.botFlip == False:
                self.update_action(1)
                self.Flip = True
                self.draw(screen)
            if self.moving_left == True and self.botFlip == True:
                self.update_action(1)
                self.Flip = False
                self.draw(screen)
            if self.moving_left == True and self.running == True:
                self.update_action(4)

            self.image = self.animation_list[self.action][self.frame_index]
            
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0

        if self.attacking:
            if self.moving_right == True and self.botFlip == False:
                self.update_action(8)
            if self.moving_right == True and self.botFlip == True:
                self.update_action(8)
                self.Flip = True
                self.draw(screen)  
            if self.moving_left == True and self.botFlip == False:
                self.update_action(8)
                self.Flip = True
                self.draw(screen)
            if self.moving_left == True and self.botFlip == True:
                self.update_action(8)
                self.Flip = False
                self.draw(screen)
            if self.moving_up == True and self.botFlip == False:
                self.update_action(10)
            if self.moving_up == True and self.botFlip == True:
                self.update_action(6)
            if self.moving_down == True and self.botFlip == False:
                self.update_action(6)
            if self.moving_down == True and self.botFlip == True:
                self.update_action(10)
        
            if idle_condition and self.action == 0:
                self.update_action(6)
            if idle_condition and self.action == 2:
                self.update_action(10)
            if idle_condition and self.action == 1:
                self.update_action(8)
            if idle_condition and self.action == 1 and self.Flip:
                self.update_action(8)
                self.Flip = True
                self.draw(screen)

            # if self.attack_move and idle_condition and self.action == 7:
            #     self.update_action(6)
            #     self.attack(screen,target)

            # attack logic for idle facing down 
            if self.attack_move and idle_condition and self.action == 6:
                self.attack(screen,target)
                self.update_action(7)
                self.attack_hit = True
            
            if self.attack_hit and idle_condition and self.action == 7:
                self.update_action_1(6)

            # attack logic for idle facing up 
            if self.attack_move and idle_condition and self.action == 10:
                self.attack(screen,target)
                self.update_action(11)
                self.attack_hit = True
            
            if self.attack_hit and idle_condition and self.action == 11:
                self.update_action_1(10)

            # attack logic for idle facing right 
            if self.attack_move and idle_condition and self.action == 8:
                self.attack(screen,target)
                self.update_action(9)
                self.attack_hit = True
            
            if self.attack_hit and idle_condition and self.action == 9:
                self.update_action_1(8)

            # attack logic for idle facing left 
            if self.attack_move and idle_condition and self.action == 8 and self.Flip:
                self.attack(screen,target)
                self.update_action(9)
                self.attack_hit = True
                self.draw(screen)
            
            if self.attack_hit and idle_condition and self.action == 9 and self.Flip:
                self.update_action_1(8)
                self.draw(screen)


            # if self.attack_move and idle_condition and self.action == 7:
            #     self.attack_hit = False
            #     self.attack(screen,target)

            # if idle_condition and self.action == 7:
            #     self.update_action(6)


            # if idle_condition and self.action == 2:
            #     self.update_action(10)
            # if idle_condition and self.action == 1:
            #     self.update_action(8)
            # if idle_condition and self.action == 1 and self.Flip:
            #     self.update_action(8)
            #     self.Flip = True
            #     self.draw(screen)

            if self.attack_move and self.moving_up == True:
                self.update_action(11)
                self.attack(screen,target)
            if self.attack_move and self.moving_down == True:
                self.update_action(7)
                self.attack(screen,target)
            if self.attack_move and self.moving_right == True:
                self.update_action(9)
                self.attack(screen,target)
            if self.attack_move and self.moving_left == True:
                self.update_action(9)
                self.Flip = True
                self.draw(screen)
                self.attack(screen,target)

            
            # handle idle fighting animations 
            
            
            # if self.attack_move and idle_condition == True and self.action == 8 and self.Flip == True:
            #     self.update_action(9)
            #     self.Flip = True
            #     self.draw(screen)
            # if self.attack_move and idle_condition == True and self.action == 8 and self.Flip == False:
            #     self.attack(screen,target)
                # self.update_action(8)
            # if self.attack_move and idle_condition == True and self.action == 9 and self.Flip == True:
            #     self.update_action(8)
            #     self.Flip = True
            #     self.draw(screen)
            # if self.attack_move and idle_condition == True and self.action == 9 and self.Flip == False:
            #     self.update_action(8)
            # if self.action == 9:
            #     self.update_action(8)
            # if self.action == 10:
            #     self.update_action(11)
            # if self.action == 6:
            #     self.update_action(7)
                   
            self.image = self.animation_list[self.action][0]
            
    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.update_time = pygame.time.get_ticks()

    def update_action_1(self,new_action):
        animation_cooldown = 500
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.action = new_action
                self.update_time = pygame.time.get_ticks()
                
    def attack(self,surface,target):
        if self.moving_right:
            attacking_rect = pygame.Rect(self.rect.centerx - 10, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
        if self.moving_right and (self.rect.x - target.rect.x > 80) and (self.rect.centerx > target.rect.centerx):
            attacking_rect = pygame.Rect(self.rect.centerx - 50, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
        if self.moving_right and (self.rect.x - target.rect.x > 100) and (self.rect.centerx > target.rect.centerx):
            attacking_rect = pygame.Rect(self.rect.centerx - 10, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
    
        if self.moving_left:
            attacking_rect = pygame.Rect(self.rect.centerx - 50, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
        if self.moving_left and (target.rect.x - self.rect.x > 80) and (target.rect.centerx > self.rect.centerx):
            attacking_rect = pygame.Rect(self.rect.centerx - 10, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
        if self.moving_left and (target.rect.x - self.rect.x > 100) and (target.rect.centerx > self.rect.centerx):
            attacking_rect = pygame.Rect(self.rect.centerx - 50, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)

        if self.moving_up:
            attacking_rect = pygame.Rect(self.rect.centerx - 28, self.rect.y + 55, self.rect.width - 10, self.rect.height/2 + 10)
        if self.moving_up and (target.rect.y - self.rect.y < 120) and (self.rect.centery < target.rect.centery):
            attacking_rect = pygame.Rect(self.rect.centerx - 40, self.rect.y + 125, self.rect.width - 10, self.rect.height/2 + 10)
        if self.moving_up and (self.rect.y - target.rect.y > 120) and (self.rect.centery < target.rect.centery):
            attacking_rect = pygame.Rect(self.rect.centerx - 28, self.rect.y + 55, self.rect.width - 10, self.rect.height/2 + 10)

        if self.moving_down:
            attacking_rect = pygame.Rect(self.rect.centerx - 40, self.rect.y + 125, self.rect.width - 10, self.rect.height/2)
        if self.moving_down and (self.rect.y - target.rect.y < 120) and (self.rect.centery > target.rect.centery):
            attacking_rect = pygame.Rect(self.rect.centerx - 28, self.rect.y + 55, self.rect.width - 10, self.rect.height/2 + 10)
        if self.moving_down and (self.rect.y - target.rect.y > 120) and (self.rect.centery > target.rect.centery):
            attacking_rect = pygame.Rect(self.rect.centerx - 40, self.rect.y + 125, self.rect.width - 10, self.rect.height/2)
        
        idle_condition = (not self.moving_down and not self.moving_up and not self.moving_left and not self.moving_right)
        
        if (self.action == 6) and idle_condition:
            attacking_rect = pygame.Rect(self.rect.centerx - 40, self.rect.y + 125, self.rect.width - 10, self.rect.height/2)

        if (self.action == 10) and idle_condition:
           attacking_rect = pygame.Rect(self.rect.centerx - 28, self.rect.y + 55, self.rect.width - 10, self.rect.height/2 + 10)
   
        if (self.action == 8) and idle_condition:
            attacking_rect = pygame.Rect(self.rect.centerx - 10, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
     
        if (self.action == 8) and idle_condition and self.Flip:
           attacking_rect = pygame.Rect(self.rect.centerx - 50, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
      

        
        # if (self.action == 7) and idle_condition and not self.attack_hit:
        #     self.update_action(6)
        #     attacking_rect = pygame.Rect(self.rect.centerx - 40, self.rect.y + 125, self.rect.width - 10, self.rect.height/2)
            
        
        # if (self.action == 6) and idle_condition:
        #     attacking_rect = pygame.Rect(self.rect.centerx - 40, self.rect.y + 125, self.rect.width - 10, self.rect.height/2)
        #     self.update_action(6)
            

        # if (self.action == 9) and not self.Flip and (not self.moving_down and not self.moving_up and not self.moving_right and not self.moving_left):
        #     attacking_rect = pygame.Rect(self.rect.centerx - 10, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)

        # if (self.action == 8) and self.Flip and (not self.moving_down and not self.moving_up and not self.moving_right and not self.moving_left):
        #     attacking_rect = pygame.Rect(self.rect.centerx - 50, self.rect.y + 80, self.rect.width - 5, self.rect.height/2)
            # self.update_action(9)
        
        if attacking_rect.colliderect(target.rect):
         target.health -= 10
        
        pygame.draw.rect(surface,(0,255,255),attacking_rect)


         

  #idle animations transitions
    


