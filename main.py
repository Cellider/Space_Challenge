import sys
from time import sleep
import pygame

from settings import Settings
from player import Player
from enemies import Enemy1, Enemy2, Enemy3 
from bullet import LeftBullet, RightBullet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from laser import Laser, Beam
from gun import Gun
from canon import Canon
from shield import Shield
from explosion import Explosion

class SpaceShooters:
	"""Class to manage the main part of the game code."""

	def __init__(self):
		"""Initialize the game, create and store game resources."""
		pygame.init()

		# Set screen to match the background size.
		self.screen = pygame.display.set_mode((1366, 768))
		# Set a text on game window
		pygame.display.set_caption('Space Shooters')
		self.screen_image = pygame.image.load('sprites/space.bmp')

		# Create instance to store settings, game stats and scoreboard
		self.settings = Settings()
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		# Create the objects of the game
		self.player = Player(self)
		self.gun = Gun(self)
		self.canon = Canon(self)
		self.enemies1 = pygame.sprite.Group()
		self.enemies2 = pygame.sprite.Group()
		self.enemies3 = pygame.sprite.Group()
		self.enemies_list = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.active_laser = pygame.sprite.Group()
		self.beam = Beam(self)
		self.active_shield = pygame.sprite.Group()
		self.explosion_list = pygame.sprite.Group()

		# Make the Play button.
		self.play_button =  Button(self, 'PLAY')

		# Use this attributes to control the bullets.
		self.last_fired = 0
		self.fired_times = 0
		self.keep_firing = False

		# Keep track of the canon animation state and time of animation
		self.fire_laser = False
		self.laser_active = False
		self.wait_for_canon = False
		self.canon_loading = 0

		# Keep track of the shield state and time it lasts
		self.shield_active_time = 0
		# The player wont get any damage if this is true
		self.shield_is_active = False

		# Keep track of when the player was last hit
		self.last_player_hit = 0
	
	def run_game(self):
		"""Start the main loop events and respond to them"""

		while True:
			# Check for event first so we can know when the player click the start button
			self._check_events()

			self._update_screen()
			# We update the screen before anything else so the player can see the game before clicking the start button
			if self.stats.game_active == True:
				self.player.update()
				self.gun.update()
				self.canon.update()
				self._update_bullets()
				self._update_enemies()
				self._update_laser()
				self.beam.update()
				self._update_shield()
				self._update_explosions()
				# If the flage keep_firing is true, it will keep creating bullets with a 200 millisecond cooldown
				if self.keep_firing == True:
					if pygame.time.get_ticks() - self.last_fired > self.settings.bullet_cooldown:
						self.last_fired = pygame.time.get_ticks()
						self._fire_bullet()

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks PLAY."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)

		if button_clicked and not self.stats.game_active:
			# Reset the game settings
			#self.settings._initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_wave()
			self.sb.prep_lifes()

			# Get rid of any remaining aliens and bullets.
			self.enemies_list.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship
			self._create_fleet()
			self.player.center_player()

			# Hide the mouse cursor
			pygame.mouse.set_visible(False)

		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_keydown_events(self, event):
		"""Listen for keypress inputs."""
		if event.key == pygame.K_RIGHT:
			self.player.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.player.moving_left = True
		elif event.key == pygame.K_UP:
			self.player.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.player.moving_down = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			# Respond if the player is holding down they space key
			self.keep_firing = True
		elif event.key == pygame.K_z:
			self._activate_laser(event)
		elif event.key == pygame.K_x:
			self._activate_shield(event)
				

	def _check_keyup_events(self, event):
		"""Listen for key releases."""
		if event.key == pygame.K_RIGHT:
			self.player.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.player.moving_left = False
		elif event.key == pygame.K_UP:
			self.player.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.player.moving_down = False
		elif event.key == pygame.K_SPACE:
			# Respond if the player releases the space key
				self.keep_firing = False
 
	def _fire_bullet(self):
		"""Create a new bullet and add to the bullets list"""
		# We keep track of what side of the player's ship to fire the bullet using fired times
		# We also add all them to bullets list to also treat all them as one when needed
		if len(self.bullets) < self.settings.bullet_limit:
			self.fired_times += 1
			if self.fired_times == 1:
				new_bullet = RightBullet(self)
				self.bullets.add(new_bullet)
			elif self.fired_times == 2:
				new_bullet = LeftBullet(self)
				self.bullets.add(new_bullet)
				self.fired_times = 0


	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
		# Update bullets according to which side they should be fired
		for bullet in self.bullets.sprites():
			# Check side returns a string to which side they are: right or left
			side = bullet.check_side()
			# Send to the gun object the side string, so it knows which sprite it should activate
			self.gun.fire_bullet(side)
			bullet.update()

		# Get rid of bullet that go further than the screen.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_enemy_collisions()

	def _check_bullet_enemy_collisions(self):
		"""Respond to bullet-alien collisions."""
		# Check for any bullets that have hit an enemy.
		# If so, get rid of the bullet and the enemy.
		collisions = pygame.sprite.groupcollide(
		self.bullets, self.enemies_list, True, False)
 

		if collisions:
			for enemies in collisions.values():
				for enemy in enemies:
					enemy.hp -= self.settings.bullet_damage
					if enemy.hp <= 0:
						self._create_explosion(enemy.rect.centerx, enemy.rect.centery)
						self.enemies_list.remove(enemy)
						self.stats.score += enemy.points * len(enemies)
			self.sb.prep_score()
			self.sb.check_high_score()
		#enemy_hit = pygame.sprite.spritecollideany(self.beam, self.enemies1)
		#if enemy_hit:
		#	self.enemies1.remove(enemy_hit)


		if not self.enemies_list:
 			# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.settings.speedup_game()

			# Increase wave.
			self.stats.wave += 1
			self.sb.prep_wave()

	def _activate_laser(self, event):
		"""Activate the laser once player press the Z key."""
		# Will only activate if the player has lasers avaibale and one is not already active
		if self.settings.laser_amount > 0 and len(self.active_laser) < 1:
			laser = Laser(self)
			self.active_laser.add(laser)
			# start playing the animation sprite for loading the canon
			self.canon.load_canon()
			# decrease how many lasers the player has available
			self.settings.laser_amount -= 1
			self.sb.prep_laser_counter()
			# we will keep track of how much time has passed since the animation for loading has started
			self.canon_loading = pygame.time.get_ticks()
			# we set this flag so the _update_laser will only work once the player has pressed Z
			self.wait_for_canon = True
		

	def _update_laser(self):
		"""Keep track of the laser and canon objects and respond accordingly."""
		if self.wait_for_canon:
			# Will only update the laser once enough time (self.canon_load_time) has passed
			# Instead of setting a flag to keep track of when the animation ends, we simply set an timer 
			# That get reset everytime activate_laser is called (self.canon_loading)
			if pygame.time.get_ticks() - self.canon_loading >= self.settings.canon_load_time:
				# Activate the fire_laser animation on the canon
				self.canon.fire_canon()
				for laser in self.active_laser.sprites():
					# Will only allow the laser to be draw into the screen if this flag is true
					self.fire_laser = True
					laser.update()
					self._check_laser_enemy_collisions()
			# The laser lasts 10 seconds. Instead of creating a new timer, we use self.canon_loading
			# And set self.laser_preparing with a bigger value
			if pygame.time.get_ticks() - self.canon_loading >= self.settings.laser_timer:
				# Will start the animation for stopping the canon, keep track of the canon state
				# And stopping the loop by setting the flags to False
				self.canon.stop_canon()
				self.active_laser.empty()
				self.wait_for_canon = False
				self.fire_laser = False

	def _check_laser_enemy_collisions(self):
		"""Respond to bullet-alien collisions."""
		# Check for any bullets that have hit an enemy.
		# If so, get rid of the bullet and the enemy.
		collisions = pygame.sprite.groupcollide(
		self.active_laser, self.enemies_list, False, True)
 

		if collisions:           
			for enemies in collisions.values():
				for enemy in enemies:
						self._create_explosion(enemy.rect.centerx, enemy.rect.centery)
						self.enemies_list.remove(enemy)
						self.stats.score += enemy.points * len(enemies)
			self.sb.prep_score()
			self.sb.check_high_score()
		#enemy_hit = pygame.sprite.spritecollideany(self.beam, self.enemies1)            
		#if enemy_hit:
		#	self.enemies1.remove(enemy_hit)


		if not self.enemies_list:
 			# Destroy existing bullets and create new fleet.
			#self.active_laser.empty()
			self._create_fleet()
			self.settings.speedup_game()

			# Increase wave.
			self.stats.wave += 1
			self.sb.prep_wave()

	def _activate_shield(self, event):
		"""Create a shield to protect the player from any damage."""
		if self.settings.shield_amount > 0 and len(self.active_shield) < 1:
			shield = Shield(self)
			self.active_shield.add(shield)
			# start playing the animation sprite for activating the shield
			shield.activate()
			# decrease how many shield the player has available
			self.settings.shield_amount -= 1
			self.sb.prep_shield_counter()
			# Keep track of when the shield was activated
			self.shield_active_time = pygame.time.get_ticks()
			self.shield_is_active = True

	def _update_shield(self):
		"""Animate the sprite and position of the shield"""
		for shield in self.active_shield.sprites():
			shield.update()
			# start animation for deactivating the shield
			if pygame.time.get_ticks() - self.shield_active_time >= self.settings.shield_timer:
				# the player can now take damage again                  
				self.shield_is_active = False
				shield.deactivate()
				# return true or false depeding on shield state
				if not shield.shield_state():
					self.active_shield.empty()




	def _create_fleet(self):
		"""Create a fleet of aliens."""
		# Create an alien and find the number of aliens in a row.
		# Spacing between each alien is equal to one alien width.
		enemy = Enemy1(self)
		enemy_width, enemy_height = enemy.rect.size 
		available_space_x = self.settings.screen_width - (2 * enemy_width)
		number_enemies_x = available_space_x // (2 * enemy_width)

		# Determine the number of rows of aliens that fit on the screen.
		player_height = self.player.rect.height
		available_space_y = (self.settings.screen_height -
		(3 * enemy_height) - player_height)
		number_rows = available_space_y // (2 * enemy_height)

		# Create the full fleet of aliens.
		for row_number in range(number_rows):
			for enemy_number in range(number_enemies_x):
				self._create_alien(enemy_number, row_number)

	def _create_alien(self, enemy_number, row_number):
		"""Create an alien and place it in the row."""
		enemy = Enemy1(self)
		enemy_width, enemy_height = enemy.rect.size
		enemy.x = enemy_width + 2 * enemy_width * enemy_number
		enemy.rect.x = enemy.x 
		enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
		self.enemies_list.add(enemy)

	def _update_enemies(self):
		"""Moves the fleet of enemies to the right and then to left"""
		self._check_fleet_edges()
		self.enemies_list.update()

		enemy_hit_player = pygame.sprite.spritecollideany(self.player, self.enemies_list)
		if enemy_hit_player:
			self.enemies_list.remove(enemy_hit_player)
			self._player_hit()

		# Look for any aliens that may hit the bottom of the screen
		self._check_enemies_bottom()

	def _create_explosion(self, xposition, yposition):
		"""Put an explosion sprite on top of the last rect of an enemy when its destroyed"""
		explosion = Explosion(self)
		self.explosion_list.add(explosion)
		explosion.get_position(xposition, yposition)

	def _update_explosions(self):
		"""Animate the sprite for the explosion"""
		for explosion in self.explosion_list.sprites():
			# Stop the animation when check_state() returns false
			if explosion.check_state():
				explosion.update()
			elif not explosion.check_state():
				self.explosion_list.remove(explosion)



	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge"""
		for enemy in self.enemies_list.sprites():
			if enemy.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the whole fleet and change its direction"""
		for enemy in self.enemies_list.sprites():
			enemy.rect.y += self.settings.e1_drop_speed 
		self.settings.fleet_direction *= -1

	def _check_enemies_bottom(self):
		"""Check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for enemy in self.enemies_list.sprites():
			if enemy.rect.bottom >= screen_rect.bottom:
				# Treat this the same way if the player got hit
				self._player_hit(True)
				break

	def _player_hit(self, bottom=''):
		"""Respond to the ship being hit by an alien"""
		# The player will not take damag with an active shield                                 
		if self.shield_is_active and not bottom:
			pass
		# The player cannot take damage for a short period of tim after getting hit once
		elif pygame.time.get_ticks() - self.last_player_hit < self.settings.iframe  and not bottom:
			pass
		elif self.stats.lifes_left > 0:
			# Decrement ship_left, and update scoreboard.
			self.stats.lifes_left-= 1
			self.sb.prep_lifes()

			# Get rid of any remaining aliens and bullets
			self.enemies_list.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship
			self._create_fleet()
			#self.player.center_player()
			self.last_player_hit = pygame.time.get_ticks()

		else: 
			self.stats.game_active = False

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.blit(self.screen_image, (0, 0))
		self.player.draw()
		self.gun.draw()
		self.canon.draw()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		if self.fire_laser:
			for laser in self.active_laser.sprites():
				laser.draw_laser()
		self.beam.draw_beam()
		for shield in self.active_shield.sprites():
			shield.draw()
		for explosion in self.explosion_list.sprites():
			explosion.draw()
		self.enemies_list.draw(self.screen)

		# Draw the score information.
		self.sb.show_score()
		
		# Draw the play button if the game inactive.
		if not self.stats.game_active:
			self.play_button.draw_button()
 
		pygame.display.flip()


if __name__ == '__main__':
	# Make an instance and run the game
	game = SpaceShooters()
	game.run_game()