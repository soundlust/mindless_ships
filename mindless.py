import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame.sprite import Sprite

from vec2d import vec2d

N_CREEPS = 1
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
CARN_FILENAMES = [
		"image/enemy_ship_v4.png"]
HERB_FILENAMES = [
		"image/enemy_ship_v1.png",
		"image/enemy_ship_v2.png",
		"image/enemy_ship_v3.png"]
carns = []
herbs = []

class Creep(Sprite):
	##
	# A creep sprite that bounces off walls and changes its 
	# direction from time to time
	##
	def __init__(self, screen, img_filename, init_position, init_direction, speed):
		
	
		Sprite.__init__(self)
		
		self.screen = screen
		self.speed = speed
		
		#base_image holds the original image, positioned to
		# angle 0.
		# image will be rotated.
		#
		self.base_image = pygame.image.load(img_filename).convert_alpha()
		self.image = self.base_image
		
		self.pos = vec2d(init_position)
		
		
		self.direction = vec2d(init_direction).normalized()
	
	def update(self, time_passed):
		self._change_direction(time_passed)
		
		self.image = pygame.transform.rotate(self.base_image, -self.direction.angle)
		displacement = vec2d(self.direction.x * self.speed * time_passed, self.direction.y * self.speed * time_passed)
		
		self.pos += displacement
		
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
		if self._breed > randint(7000, 15000):
			carns.append(Creep(screen, 
							choice(CARN_FILENAMES),
							(	randint(0, SCREEN_WIDTH),
								randint(0, SCREEN_HEIGHT)),
							(	choice([-1, 1]),
								choice([-1, 1])),
							0.1))
			N_CREEPS = 1
			self._breed = 0
			

def run_game():
	#Basic game window parameters
	pygame.display.set_caption("Carnivores & Herbavores")
	BG_COLOR = 10, 2, 15 


	pygame.init()
	clock = pygame.time.Clock()	

	#Creates N_CREEPS, random creeps.
	for i in range(N_CREEPS):
		carns.append(Creep(screen, 
							choice(CARN_FILENAMES),
							(	randint(0, SCREEN_WIDTH),
								randint(0, SCREEN_HEIGHT)),
							(	choice([-1, 1]),
								choice([-1, 1])),
							0.1))

	for y in range(N_CREEPS):
		herbs.append(Creep(screen, 
							choice(HERB_FILENAMES),
							(	randint(0, SCREEN_WIDTH),
								randint(0, SCREEN_HEIGHT)),
							(	choice([-1, 1]),
								choice([-1, 1])),
							0.1))
	
	while True:
		
		time_passed = clock.tick(50)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_game()
		
		# Redraw the background
		screen.fill(BG_COLOR)

		# No clue how to handle collision
		# 
		#pygame.sprite.groupcollide(carns, herbs, 1, 0)
		
		# Update and redraw all creeps
		for herb in herbs:
			herb.update(time_passed)
			herb.blitme()
			herb.reproduce(time_passed)

		for carn in carns:
			carn.update(time_passed)
			carn.blitme()
			carn.reproduce(time_passed)
		
		pygame.display.flip()

def exit_game():
	sys.exit()
	
run_game()
