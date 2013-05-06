import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame.sprite import Sprite

from vec2d import vec2d

N_CREEPS = 1
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
CREEP_FILENAMES = [
		"image/enemy_ship_v1.png",
		"image/enemy_ship_v2.png",
		"image/enemy_ship_v3.png",
		"image/enemy_ship_v4.png"]
creeps = []

class Creep(Sprite):
	##
	# A creep sprite that bounces off walls and changes its 
	# direction from time to time
	##
	def __init__(self, screen, img_filename, init_position, init_direction, speed):
		
	##
	#	Create a new Creep.
	#
	#
	#	screen:
	#		The screen on which the creep lives ( must be a 
	#		pygame surface object, such as pygame.display)
	#
	#	img_filename:
	#		Image file for the creep.
	#
	#	init_position:
	#		A vec2d or a pair specifying the initial position 
	#		of the creep on the screen
	#
	#	init_direction:	
	#		A vec2d or pair specifying the initial direction of the creep. 	
	#		Must have an angle that is multiple of 45 degrees.
	#
	#	speed:
	#		Creep speed, in pixels/millisecond (px/ms)
	#
	##
		Sprite.__init__(self)
		
		self.screen = screen
		self.speed = speed
		
		#base_image holds the original image, positioned to
		# angle 0.
		# image will be rotated.
		#
		self.base_image = pygame.image.load(img_filename).convert_alpha()
		self.image = self.base_image
		
		#A vector specifying the creep's position on the screen
		#
		self.pos = vec2d(init_position)
		
		# the direction is a normalized vector
		#
		self.direction = vec2d(init_direction).normalized()
	
	def update(self, time_passed):
		self._change_direction(time_passed)
		##
		#	Make the creep point in the correct direction.
		#	since our direction vector is in screen coordinates
		# (i.e. right bottom is 1,1), and rotate() rotates
		#counter-clockwise, the angle must be inverted to work correctly
		#
		##
		self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)
		displacement = vec2d(self.direction.x * self.speed * time_passed, self.direction.y * self.speed * time_passed)
		
		self.pos += displacement
		##
		# When the image is rotated, its size is changed.
		# We must take the size into account for detecting 
		# collisions with the walls
		##
		self.image_w, self.image_h = self.image.get_size()
		bounds_rect = self.screen.get_rect().inflate(
						-self.image_w, -self.image_h)
		
		if self.pos.x < bounds_rect.left:
			self.pos.x = bounds_rect.left
			self.direction.x *= -1
		elif self.pos.x > bounds_rect.right:
			self.pos.x = bounds_rect.right
			self.direction.x *= -1
		if self.pos.y < bounds_rect.top:
			self.pos.y = bounds_rect.top
			self.direction.y *= -1
		elif self.pos.y > bounds_rect.bottom:
			self.pos.y = bounds_rect.bottom
			self.direction.y *= -1

		
	def blitme(self):
		##
		#	Blit the creep onto the screen that was provided in the constructor
		##
		draw_pos = self.image.get_rect().move(
			self.pos.x - self.image_w /2,
			self.pos.y - self.image_h /2)
		self.screen.blit(self.image, draw_pos)
	
		
	
	_counter = 0
	_breed = 0
	
	
	def _change_direction(self, time_passed):
		# Turn by 45 degrees in a random direction one per 0.4 to 0.5 seconds.
		
		self._counter += time_passed
		if self._counter > randint(400, 500):
			self.direction.rotate(45 * randint(-1, 1))
			self._counter = 0
			
	def reproduce(self, time_passed):
		# reproduce another creep after 27 to 55 seconds have passed
		self._breed += time_passed
		if self._breed > randint(27000, 55000):
			creeps.append(Creep(screen, 
							choice(CREEP_FILENAMES),
							(	randint(0, SCREEN_WIDTH),
								randint(0, SCREEN_HEIGHT)),
							(	choice([-1, 1]),
								choice([-1, 1])),
							0.1))
			N_CREEPS = 0
			self._breed = 0
			

def run_game():
	#Basic game window parameters
	pygame.display.set_caption("Carnivores & Herbavores")
	BG_COLOR = 100, 100, 80 


	pygame.init()
	clock = pygame.time.Clock()	

	#Creates N_CREEPS, random creeps.
	for i in range(N_CREEPS):
		creeps.append(Creep(screen, 
							choice(CREEP_FILENAMES),
							(	randint(0, SCREEN_WIDTH),
								randint(0, SCREEN_HEIGHT)),
							(	choice([-1, 1]),
								choice([-1, 1])),
							0.1))
	# The main game loop
	#
	while True:
		# limit frame speed to 50 fps
		#
		time_passed = clock.tick(50)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game()
		
		# Redraw the background
		screen.fill(BG_COLOR)
		# If creep collides with each other, destroy the smaller creep
		
		# Update and redraw all creeps
		for creep in creeps:
			creep.update(time_passed)
			creep.blitme()
			creep.reproduce(time_passed)
		
		pygame.display.flip()

def exit_game():
	sys.exit()
	
run_game()
