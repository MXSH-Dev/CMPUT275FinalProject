import pygame
import time
from random import*
from LoadMusic import*
from math import*

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255, 102, 153)
ORANGE = (255, 51, 0)
YELLOW = (255, 255, 102)
LIGHT_GREEN = (102, 255, 102)


# class for the bullet of boss
class BossBullet1(object):
	"""docstring for BossBullet"""
	def __init__(self,screen,x,y,angle):
		# the location of the start of bullets
		self.x = x + 125 
		self.y = y + 364
		# different directions
		self.angle = angle
		self.screen = screen

	# how the bullets move
	def move(self):
		#totally 7 directions
		if(self.angle == 1):
			self.y -= 2
			self.x -= 2
		elif(self.angle == 2):
			self.x -= 3
		elif(self.angle == 3):
			self.x -= 2
			self.y += 2
		elif(self.angle == 4):
			self.y += 3
		elif(self.angle == 5):
			self.x += 2
			self.y += 2
		elif(self.angle == 6):
			self.x += 3
		elif(self.angle == 7):
			self.x += 2
			self.y -= 2

	# display the bullets
	def display(self):
		pygame.draw.polygon(self.screen,YELLOW,[[self.x,self.y],[self.x-5,self.y+8],[self.x+5,self.y+8]],1)
		pygame.draw.polygon(self.screen,YELLOW,[[self.x-5,self.y+4],[self.x,self.y+12],[self.x+5,self.y+4]],1)

	# check bullets whether they are out of boundary
	def checkBullet(self):
		if(self.y < 0 or self.y > 900 or self.x <0 or self.x > 600):
			return True
		else:
			return False

# class for missile of boss
class Missile(object):
	def __init__(self,screen,x1,y1,x,y,radius):
		# the location of the start of missiles
		self.x1 = x1 + 125
		self.y1 = y1 + 364

		# the location of hero plane
		self.x = x
		self.y = y

		self.screen = screen

		# the speed of missiles
		self.section = 2
		# the size  of missiles
		self.diameter = 2*radius
		self.radius = radius
		# use the mahanttan distance to calculate the disatance between heroplane and missile
		self.distance = sqrt(pow(self.x1-self.x,2)+pow(self.y1-self.y,2))
		# opposite over hypotenuse
		self.sina = (self.y1-self.y)/self.distance
		# adjacent over hypotenuse
		self.cosa = (self.x-self.x1)/self.distance
		# find the angle between the hypotenuse and x-axis
		self.angle = atan2(self.y-self.y1,self.x-self.x1)
		# change to degrees
		self.d_angle = degrees(self.angle)

	# how to move the missiles
	def move(self,x,y):
		# update the  location of hero plane
		self.x = x
		self.y = y
		# caculate the current location of missile
		self.x1 = self.x1 + self.section * self.cosa
		self.y1 = self.y1 - self.section * self.sina
		# update the shortest distance
		self.distance = sqrt(pow(self.x1-self.x,2)+pow(self.y1-self.y,2))
		# update angles
		self.sina = (self.y1-self.y)/self.distance
		self.cosa = (self.x-self.x1)/self.distance
		self.angle = atan2(self.y-self.y1,self.x-self.x1)
		self.d_angle = degrees(self.angle)
		# display the missile
		# pygame.draw.circle(self.screen,BLACK,[int(self.x1-self.diameter),int(self.y1-self.radius)],self.radius)
		# pygame.draw.circle(self.screen,WHITE,[int(self.x1-self.diameter),int(self.y1-self.radius)],self.radius-3)
		pygame.draw.circle(self.screen,BLACK,[int(self.x1),int(self.y1)],self.radius)
		pygame.draw.circle(self.screen,WHITE,[int(self.x1),int(self.y1)],self.radius-3)


# class for hero bullets
class HeroBullet(object):
	def __init__(self,screen,x,y):
		# the location of the start of bullet
		self.x = x+27
		self.y = y-5

		self.screen = screen

	# move straight up
	def move(self):
		self.y -=6

	# display the bullet
	def display(self):
		pygame.draw.ellipse(self.screen,ORANGE,[self.x,self.y,8,16],3)
		pygame.draw.circle(self.screen,YELLOW,[self.x+4,self.y+6],3)

	# check the bullet whether is out of boundary
	def checkBullet(self):
		if(self.y < 0):
			return True
		else:
			return False

# class for enemy bullet
class EmBullet(object):
	def __init__(self,screen,x,y):
		# the location of the start of bullet
		self.x = x+25
		self.y = y+52

		self.screen = screen

	# move straight down
	def move(self):
		self.y += 4

	# display the bullet
	def display(self):
		pygame.draw.polygon(self.screen,LIGHT_GREEN,[[self.x-4,self.y],[self.x+4,self.y],[self.x,self.y+10]],2)

	# check the bullet whether is out of boundary
	def checkBullet(self):
		if(self.y > 900):
			return True
		else:
			return False