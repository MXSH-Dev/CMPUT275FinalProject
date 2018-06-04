import pygame
import time
from random import*
from LoadMusic import*
from bullets import*

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255, 102, 153)
ORANGE = (255, 51, 0)
YELLOW = (255, 255, 102)
LIGHT_GREEN = (102, 255, 102)

# the size of the window
Screen_W = 600
Screen_H = 900

# base class for all planes
class BasePlane(object):
	def __init__(self,screen):
		# random initial spawning position
		self.x = 0
		self.y = 0 - randint(1,50)

		self.screen = screen

	# move straight down
	def move(self):
		self.y += 2

	#respawn new enemies
	def reset(self):
		self.x = randint(1,550)
		self.y = 0 - randint(1,50)
		self.active = True

	def shoot(self,chance,value):
		check = randint(1,chance)
		if check == value:
			newBullet = EmBullet(self.screen,self.x,self.y)
			self.bulletList.append(newBullet)


# class for the first kind of enemy
class EnemyPlane1(BasePlane):
	def __init__(self,screen):
		# random initial spawning position
		self.x = randint(1,550)
		self.y = 0 - randint(1,50)

		self.screen = screen

		# load the image
		self.image = pygame.image.load('./planes/em1.gif').convert()
		
		self.bulletList = list()

		self.direction = 'right'

		self.active = True

		self.dest_images = list()
		# destroying images
		self.dest_images.extend([
				pygame.image.load('./planes/enemy1explode1.gif').convert(),
				pygame.image.load('./planes/enemy1explode2.gif').convert(),
				pygame.image.load('./planes/em_final1.gif').convert()

			])
	
	# display the enemy
	def display(self,chance):
		self.screen.blit(self.image,(self.x,self.y))
		# shoot randomly
		self.shoot(chance,50)

		NoUseBullets = list()

		# clear the useless bullets
		if(len(self.bulletList)>0):
			for b in self.bulletList:
				if b.checkBullet() == True:
					NoUseBullets.append(b)
		
		if(len(NoUseBullets)>0):
			for i in NoUseBullets:
				self.bulletList.remove(i)
		# show bullets
		for b in self.bulletList:
			b.display()
			b.move()

# class for the second type of enemy
class EnemyPlane2(BasePlane):
	def __init__(self,screen):
		# random intial spawning position
		self.x = randint(1,550)
		self.y = 0 - randint(1,50)

		self.screen = screen
		# load the image
		self.image = pygame.image.load('./planes/em2.gif').convert()
		
		self.bulletList = list()
		# define the initial direction
		self.direction = 'right'

		self.active = True

		self.dest_images = list()
		# load the destroying images
		self.dest_images.extend([
				pygame.image.load('./planes/enemy2explode1.gif').convert(),
				pygame.image.load('./planes/enemy2explode2.gif').convert(),
				pygame.image.load('./planes/em_final1.gif').convert()

			])

	#display the enemies
	def display(self,chance):
		self.screen.blit(self.image,(self.x,self.y))
		# shoot the bullets randomly
		self.shoot(chance,15)

		NoUseBullets = list()
		# clear the useless bullets
		if(len(self.bulletList)>0):
			for b in self.bulletList:
				if b.checkBullet() == True:
					NoUseBullets.append(b)
		
		if(len(NoUseBullets)>0):
			for i in NoUseBullets:
				self.bulletList.remove(i)
		# show bullets
		for b in self.bulletList:
			b.display()
			b.move()
	
	# different movement of enemy
	def move(self):
		if self.direction == 'right':
			self.x += 2
		if self.direction == 'left':
			self.x -= 2

		if self.x >= 545:
			self.direction = 'left'
		if self.x <= 5:
			self.direction = 'right'
		self.y += 1		
