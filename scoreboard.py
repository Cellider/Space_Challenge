import pygame.font
from pygame.sprite import Group

from player import Player
from lifes import Lifes

class Scoreboard:
	"""Class to manage reporting score information"""

	def __init__(self, game):
		"""Initialize scorekeeping attributes."""
		self.game = game 
		self.screen = game.screen
		self.screen_rect = game.screen.get_rect()
		self.settings = game.settings
		self.stats = game.stats

		# Font settings for score information.
		self.text_color = (0, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Prepare the initial score images.
		self.prep_score()
		self.prep_high_score()
		self.prep_wave()
		self.prep_lifes()
		self.prep_shield()
		self.prep_shield_counter()
		self.prep_laser()
		self.prep_laser_counter()

	def prep_score(self):
		"""Turn the score text into a rendered image."""
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True,
				self.text_color, None) 

		# Display the score at the top right of the screen.
		self.score_rect = self.score_image.get_rect()
		self.score_rect.centerx = self.screen_rect.centerx
		self.score_rect.top = self.score_rect.top

	def show_score(self):
		"""Draw scores, lifes and lvel into the screen."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.wave_image, self.wave_rect)
		self.lifes.draw(self.screen)
		self.screen.blit(self.shield_image, self.shield_rect)
		self.screen.blit(self.shield_counter_image, self.shield_counter_rect)
		self.screen.blit(self.laser_image, self.laser_rect)
		self.screen.blit(self.laser_counter_image, self.laser_counter_rect)

	def prep_high_score(self):
		"""Turn the high score into a rendred image."""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
				self.text_color, None)

		# Center the high score at the top of the screen.
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.screen_rect.right
		self.high_score_rect.top = 50

	def check_high_score(self):
		"""Check to see it there's a new high score."""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			with open('high_score.txt', 'w') as points:
				points.write(str(self.stats.score))
			self.prep_high_score()

	def prep_wave(self):
		"""Turn the wave number into a rendered image."""
		wave_str = str(self.stats.wave)
		self.wave_image = self.font.render(wave_str, True,
				self.text_color, None)

		# Position the level below the score.
		self.wave_rect = self.wave_image.get_rect()
		self.wave_rect.right = self.high_score_rect.right
		self.wave_rect.top = self.high_score_rect.bottom

	def prep_lifes(self):
		"""Show how many lifes are left."""
		self.lifes = Group()
		vertical_space = 0
		horizontal_space = 0
		number = 0
		placement_number = 0
		for life_number in range(self.stats.lifes_left):
			if number%3 == 0 and number > 1:
				horizontal_space += 50
				vertical_space = 0
				number = 0
			vertical_space += 10
			life = Lifes(self.game)
			life.rect.y = 50 + horizontal_space
			life.rect.x = 10 + life.rect.width * number + vertical_space
			self.lifes.add(life)
			number += 1

	def prep_shield(self):
		"""Turn the wave number into a rendered image."""
		self.shield_image = pygame.image.load('sprites/shield.bmp')

		# Position the level below the score.
		self.shield_rect = self.shield_image.get_rect()
		self.shield_rect.centery = 500
		self.shield_rect.centerx = 50

	def prep_shield_counter(self):
		"""Turn the high score into a rendred image."""
		shield_counter = (self.settings.shield_amount)
		shield_counter_str = "{:,}".format(shield_counter)
		self.shield_counter_image = self.font.render(shield_counter_str, True,
				self.text_color, None)

		# Center the high score at the top of the screen.
		self.shield_counter_rect = self.shield_counter_image.get_rect()
		self.shield_counter_rect.centery = self.shield_rect.centery
		self.shield_counter_rect.right = 134 # shield.bmp size + 40 


	def prep_laser(self):
		"""Turn the wave number into a rendered image."""
		self.laser_image = pygame.image.load('sprites/laser_pwu.bmp')

		# Position the level below the score.
		self.laser_rect = self.shield_image.get_rect()
		self.laser_rect.centery = 400
		self.laser_rect.centerx = 50

	def prep_laser_counter(self):
		"""Turn the high score into a rendred image."""
		laser_counter = (self.settings.laser_amount)
		laser_counter_str = "{:,}".format(laser_counter)
		self.laser_counter_image = self.font.render(laser_counter_str, True,
				self.text_color, None)

		# Center the high score at the top of the screen.
		self.laser_counter_rect = self.laser_counter_image.get_rect()
		self.laser_counter_rect.centery = self.laser_rect.centery
		self.laser_counter_rect.right = 140 # laser_pwu.bmp size + 40 