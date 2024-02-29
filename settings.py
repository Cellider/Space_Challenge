class Settings:
	"""Class to store, mainly, numerical values used in the game."""

	def __init__(self):
		"""Initialize value that should not change"""

		# Use this to know where to place the enemies on the screen
		self.screen_width = 800
		self.screen_height = 600
		# Increase this bad boy to do funny stuff
		self.speedup_rate = 1.1

		# Player settings.
		self.player_lifes = 7
		self.player_speed = 2

		# Player bullet settings.
		self.bullet_limit = 6
		self.bullet_damage = 1
		self.bullet_speed = 3
		self.bullet_cooldown = 200

		# Laser settings
		self.laser_damage = 10
		self.laser_amount = 5
		self.laser_timer = 12800

		# Shield settings
		self.shield_amount = 3
		self.shield_timer = 15000


		# Enemy 1 settings.
		self.e1_speed = 2
		self.e1_drop_speed = 10
		self.e1_value = 50
		self.e1_health = 3

		# Enemy 2 settings.
		self.e2_speed = 6
		self.e2_drop_speed = 10
		self.e2_value = 100
		self.enemy_2_health = 2

		# Enemy 3 settings.
		self.e3_value = 200
		self.e3_drop_speed = 5
		self.e3_speed = 4
		self.e3_health = 4

		# General enemy settings
		self.fleet_direction = 1

		# How long the invisibility frame will last in miliseconds
		self.iframe = 3000

		# How long the explosion animation lasts
		self.explosion_timer = 400

		# How long the animation for loading the canon lasts
		self.canon_load_time = 2800

	def speedup_game(self):
		"""Speedup the game as the player clear waves of enemies"""
		self.e1_speed *= self.speedup_rate
		self.bullet_speed *= self.speedup_rate