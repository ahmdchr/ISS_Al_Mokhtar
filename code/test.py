def start(self):
        """Start playing the cutscene."""
        self.is_playing = True
        self.current_step = 0
        self.step_timer = 0
        # Reset knight positions to the rightmost edge of the map
        for i, knight in enumerate(self.knights):
            knight_x = self.map_width - 100  # Rightmost edge minus a margin
            knight_y = min(self.map_height - 100, 100 + (i * 20))  # Staggered positions vertically
            knight.x = knight_x
            knight.y = knight_y
        
        # Initial camera position (focus on knights)
        first_knight = self.knights[0]
        self.camera_x = first_knight.x - SCREEN_WIDTH // 2
        self.camera_y = first_knight.y - SCREEN_HEIGHT // 2
        self.clamp_camera()
        
        # Set knight targets - each knight moves to a unique position
        for i, knight in enumerate(self.knights):
            knight.move_to(
                self.map_width // 2 + (i * 30),  # Spread out horizontally
                self.map_height // 2 + (i * 10)-200  # Slight vertical offset
            )
def update(self, delta_time):
        """Update the cutscene state."""
        if not self.is_playing:
            return False
            
        self.step_timer += delta_time
        
        # Update knights
        for knight in self.knights:
            knight.update(delta_time)
        
        # Update camera position
        if self.camera_x < self.camera_target_x:
            self.camera_x += min(self.camera_speed, self.camera_target_x - self.camera_x)
        elif self.camera_x > self.camera_target_x:
            self.camera_x -= min(self.camera_speed, self.camera_x - self.camera_target_x)
            
        if self.camera_y < self.camera_target_y:
            self.camera_y += min(self.camera_speed, self.camera_target_y - self.camera_y)
        elif self.camera_y > self.camera_target_y:
            self.camera_y -= min(self.camera_speed, self.camera_y - self.camera_target_y)
        
        # Keep camera within map boundaries
        self.clamp_camera()
        
        # Cutscene step logic
        if self.current_step == 0:
            # Focus on knights approaching
            first_knight = self.knights[0]
            self.camera_target_x = first_knight.x - SCREEN_WIDTH // 2
            self.camera_target_y = first_knight.y - SCREEN_HEIGHT // 2
            
            # Check if all knights have reached their positions
            all_knights_arrived = True
            for knight in self.knights:
                if abs(knight.x - knight.target_x) > 5 or abs(knight.y - knight.target_y) > 5:
                    all_knights_arrived = False
                    break
            
            if all_knights_arrived and self.step_timer > 3.0:  # Wait 3 seconds
                
                self.current_step = 1
                self.step_timer = 0
                
        elif self.current_step == 1:
            # End cutscene
            if self.step_timer > 1.0:
                self.is_playing = False
                return True  # Cutscene is finished
        
        return False  # Cutscene still playing