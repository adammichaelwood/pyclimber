"""This module implements the enemy blob type for Py-Climber"""

import pygame
from pygame.sprite import Sprite
from animation import Animation
from animated_sprite import AnimatedSprite

class Blob(AnimatedSprite):
    """Blob enemy object"""

    def __init__(self, settings, screen, images):
        """Initialize the blob"""
        super().__init__(settings, screen, images)
        
        # Override the start position
        self.dx = self.settings.enemy_blob_dx
        
        # Set the blob-specific animations
        self.animations[self.settings.anim_name_walk_left] = Animation([0, 1, 2, 1], 2)
        self.animations[self.settings.anim_name_walk_right] = Animation([3, 4, 5, 4], 2)
        self.animations[self.settings.anim_name_jump_down_left] = Animation([6], 1)
        self.animations[self.settings.anim_name_jump_down_right] = Animation([6], 1)
        self.current_animation = self.settings.anim_name_walk_right
        self.facing_left = False

    def update_current_animation(self):
        """Set the correct animation based on state"""
        # WALKING
        if self.dy == 0:
            if self.dx < 0:
                self.set_current_animation(self.settings.anim_name_walk_left)
            else:
                self.set_current_animation(self.settings.anim_name_walk_right)
        # JUMPING
        else:
            if self.dy > 0:
                if self.facing_left:
                    self.set_current_animation(self.settings.anim_name_jump_down_left)
                else:
                    self.set_current_animation(self.settings.anim_name_jump_down_right)

    def update(self, tile_map):
        """Updates the blob sprite's position"""
        
        last_dx = self.dx
        super().update(tile_map)
        # Blobs only stop when they hit a wall so reverse course
        if last_dx != 0 and self.dx == 0:
            self.facing_left = not self.facing_left
            if self.facing_left:
                self.dx = 1.0
            else:
                self.dx = -1.0

        self.finish_update()

    def handle_collision(self, collision_list, group):
        """Given a list of sprites that collide with the sprite, alter state such as position, velocity, etc"""
        # If there's only 1 block, then we're over an edge, so do nothing in that case
        # and just let the sprite fall, otherwise, clamp to the top of the block
        if collision_list:
            if len(collision_list) > 1:
                self.falling = False
                self.falling_frames = 1
                self.dy = 0
                self.rect.bottom = collision_list[0].rect.top
            elif len(collision_list) == 1:
                if self.facing_left and self.rect.right > collision_list[0].rect.left:
                    self.falling = False
                    self.falling_frames = 1
                    self.dy = 0
                    self.rect.bottom = collision_list[0].rect.top
                elif not self.facing_left and self.rect.left < collision_list[0].rect.right:
                    self.falling = False
                    self.falling_frames = 1
                    self.dy = 0
                    self.rect.bottom = collision_list[0].rect.top