"""This module caches images for the Py-Climber game"""

import pygame

class ImageResources():
    """Hold all of the loaded image data to be shared"""

    def __init__(self, settings):
        """Load and store the images we need"""

        self.settings = settings
        # Load the tile frames
        self.tile_images = []
        tile_images = self.tile_images
        self.load_image_to_tiles('images/tiles.bmp', self.settings.tile_width, self.settings.tile_height, tile_images)

        # Load the sprite frames
        self.player_sprite_images = []
        player_images = self.player_sprite_images
        self.load_image_to_tiles('images/sprite_player.bmp', self.settings.player_width, self.settings.player_height, player_images)

        # Load the enemy blob frames
        self.enemy_blob_images = []
        blob_images = self.enemy_blob_images
        self.load_image_to_tiles('images/sprite_blob.bmp', self.settings.enemy_blob_width, self.settings.enemy_blob_height, blob_images)

        # Load the platform block image
        self.block_image = pygame.image.load('images/block.bmp')
        self.block_image.set_colorkey(self.settings.color_key)


    def load_image_to_tiles(self, file_name, tile_width, tile_height, images):
        """Load the specified image and attempt to split it into tiles
        of the specified width and height."""
        image = pygame.image.load(file_name)
        image_rect = image.get_rect()

        image_width = image_rect.width
        image_height = image_rect.height

        # Calculate the number of tiles in one row of the image (ignoring any remaining space)
        tiles_per_row = image_width // tile_width
        # Calculate the number of tiles in one col of the image (ignoring any remaining space)
        tiles_per_col = image_height // tile_height

        # The index for the row is over the number of cols in a row and vice versa
        for row_index in range(0, tiles_per_col):
            for col_index in range(0, tiles_per_row):
                # Create a new surface the size of the tile
                new_surface = pygame.Surface((tile_width, tile_height))
                # Set transparency color key (colors matching this won't get copied in blits)
                new_surface.set_colorkey(self.settings.color_key)
                # Copy just the sub-section of the image onto the surface
                new_surface.blit(image, (0, 0), (col_index * tile_width, row_index * tile_height, tile_width, tile_height))
                # Now add it to our list of surfaces, these will be index-addressed for now
                images.append(new_surface)