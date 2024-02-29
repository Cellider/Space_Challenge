import pygame
from pygame.sprite import Sprite
from pygame.locals import *

class Lifes(Sprite):
	"""Class to manage life sprite."""

	def __init__(self, game):
		"""Create life."""
		super().__init__()
		self.screen = game.screen
		self.screen_rect = game.screen.get_rect()
		self.settings = game.settings

		# Load the life image and rect.
		self.image = pygame.image.load('sprites/life.bmp')
		self.rect = self.image.get_rect()

	def draw(self):
		"""Draw the gun into the screen."""
		self.screen.blit(self.image, self.rect)