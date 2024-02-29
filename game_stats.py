class GameStats():
	"""Track statistics for Alien Invasion."""

	def __init__(self, game):
		"""Initialize statistics."""
		self.settings = game.settings
		self.reset_stats()

		# Start alien invasion on a inactive flag, so the game doesn't imediately begin 
		self.game_active = False

		# High score should never be reset
		with open('high_score.txt') as points:
			saved_high_score = points.read()
		self.high_score = int(saved_high_score)

	def reset_stats(self):
		"""Reset statistics that can change during the game."""
		self.lifes_left = self.settings.player_lifes
		self.score = 0
		self.wave = 1