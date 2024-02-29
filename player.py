import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Player(Sprite):
	"""Class to manage player aspects."""

	def __init__(self, game):
		"""Initiate player, initial positions"""
		super().__init__()
		self.screen = game.screen
		self.screen_rect = game.screen.get_rect()
		self.settings = game.settings

		# Load the ship image and get rect.
		self.image = pygame.image.load('sprites/player.bmp')
		self.rect = self.image.get_rect()

		# Load the gun image separately, so that the animation of shooting can act outside of the normal animation
		self.gun_image = pygame.image.load('sprites/gun.bmp')

		# List of all sprites for an animated sprite
		self.sprite_list = [pygame.image.load('sprites/player_standing1.bmp'),
							pygame.image.load('sprites/player_standing2.bmp'),
							pygame.image.load('sprites/player_standing3.bmp'),
							pygame.image.load('sprites/player_standing4.bmp'),
							pygame.image.load('sprites/player_standing5.bmp'),
							pygame.image.load('sprites/player_standing6.bmp'),
							pygame.image.load('sprites/player_standing7.bmp'),
							pygame.image.load('sprites/player_standing8.bmp'),
							pygame.image.load('sprites/player_standing9.bmp'),
							pygame.image.load('sprites/player_standing10.bmp')]

		# Will be used for changing images and animated sprite
		self.image_value = 0
		self.last_update = 0
		self.image_interval = 100

		# Start player on bottom center of the screen.
		self.rect.midbottom = self.screen_rect.midbottom

		# Store a decimal value for the player X, Y position.
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		# Movement flag.
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		"""Update the player's position based on movement flag"""
		# We will first update the X and Y value and then turn into the rect value
		# No elif or also, so that no line take priority
		# This also prevents the player from going beyond the screen

		if self.moving_right and self.rect.right < self.screen_rect.right:
			# Will only run if the player is moving right and is not at the right edge of screen
			self.x += self.settings.player_speed

		if self.moving_left and self.rect.left > 0:
			#Same thing as above but with left edge
			self.x -= self.settings.player_speed

		if self.moving_up and self.rect.top > 0:
			# Same thing as above but with top of the screen
			self.y -= self.settings.player_speed

		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			# Same thing as above but with bottom of the screen
			self.y += self.settings.player_speed

		# Starts a timer so that each 100 miliseconds the image changes, animating the sprite
		if pygame.time.get_ticks() - self.last_update > self.image_interval:
			self.image_value += 1
			self.last_update = pygame.time.get_ticks()

		# Restart the image loop when it ends
		if self.image_value >= len(self.sprite_list):
			self.image_value = 0
		
		# Assing the current sprite to the image
		self.image = self.sprite_list[self.image_value]


		# Update rect using values stored in self.x and self.y
		self.rect.x = self.x
		self.rect.y = self.y

	def draw(self):
		"""Draw the player into the screen at current position"""
		self.screen.blit(self.image, self.rect)

	def center_player(self):
		"""Put the player on center of screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)