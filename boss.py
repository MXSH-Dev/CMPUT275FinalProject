import pygame
import time
from random import*
from LoadMusic import*
from bullets import*
from math import*
from enemies import BasePlane

#define colors
GREEN = (0, 255, 0)
RED = (255,0,0)

#create boss
class Boss(BasePlane):
	"""docstring for Boss"""
	def __init__(self, screen):

		#the total health of boss
		self.health = 250
		#the location of boss when it is born
		self.x = 175
		self.y = -400

		self.screen = screen

		self.direction = 'right'

		#images of boss when its health is above 100
		self.image0 = pygame.image.load('./planes/boss0.gif').convert()
		self.image1 = pygame.image.load('./planes/boss1.gif').convert()
		self.image2 = pygame.image.load('./planes/boss2.gif').convert()
		self.image3 = pygame.image.load('./planes/boss3.gif').convert()
		self.image4 = pygame.image.load('./planes/boss4.gif').convert()
		self.image5 = pygame.image.load('./planes/boss5.gif').convert()
		self.image6 = pygame.image.load('./planes/boss6.gif').convert()
		#images of boss when its health is below 100
		self.imagef0 = pygame.image.load('./planes/boss0F.gif').convert()
		self.imagef1 = pygame.image.load('./planes/boss1F.gif').convert()
		self.imagef2 = pygame.image.load('./planes/boss2F.gif').convert()
		self.imagef3 = pygame.image.load('./planes/boss3F.gif').convert()
		self.imagef4 = pygame.image.load('./planes/boss4F.gif').convert()
		self.imagef5 = pygame.image.load('./planes/boss5F.gif').convert()
		self.imagef6 = pygame.image.load('./planes/boss6F.gif').convert()

		self.bulletList1 = list()
		self.missileList = list()

		self.active = False

		self.exp = False

		self.dest_images = list()
		#images of boss when it is destroyed
		self.dest_images.extend([
			pygame.image.load('./planes/d1.gif').convert(),
			pygame.image.load('./planes/d2.gif').convert(),
			pygame.image.load('./planes/d3.gif').convert(),
			pygame.image.load('./planes/d4.gif').convert(),
			pygame.image.load('./planes/d5.gif').convert(),
			pygame.image.load('./planes/d6.gif').convert(),
			pygame.image.load('./planes/d7.gif').convert(),
			pygame.image.load('./planes/d8.gif').convert()
			])

	#display the boss
	def display(self,delay,hx,hy,radius):
		if(self.health >= 100):
			# line that show the boss's health
			pygame.draw.line(self.screen,GREEN,(self.x, self.y-4),(self.x + self.health, self.y-4),2)
			#count for displaying the several images of boss above 100
			if(delay <= 60 and delay >55):
				self.screen.blit(self.image0,(self.x,self.y))
			elif(delay <= 55 and delay >50):
				self.screen.blit(self.image1,(self.x,self.y))				
			elif(delay <= 50 and delay > 45):
				self.screen.blit(self.image2,(self.x,self.y))
			elif(delay <= 45 and delay > 40):
				self.screen.blit(self.image3,(self.x,self.y))
			elif(delay <= 40 and delay > 35):
				self.screen.blit(self.image4,(self.x,self.y))
			elif(delay <= 35 and delay > 30):
				self.screen.blit(self.image5,(self.x,self.y))
			elif(delay <= 30 and delay > 25):
				self.screen.blit(self.image6,(self.x,self.y))
			elif(delay <= 25 and delay > 20):
				self.screen.blit(self.image5,(self.x,self.y))
			elif(delay <= 20 and delay > 15):
				self.screen.blit(self.image4,(self.x,self.y))
			elif(delay <= 15 and delay > 10):
				self.screen.blit(self.image3,(self.x,self.y))
			elif(delay <= 10 and delay > 5):
				self.screen.blit(self.image2,(self.x,self.y))
			elif(delay <= 5 and delay > 0):
				self.screen.blit(self.image1,(self.x,self.y))			
		# count for displaying the several images of boss below 100
		elif(self.health < 100):
			pygame.draw.line(self.screen,RED,(self.x, self.y-4),(self.x + self.health, self.y-4),2)
			if(delay <= 60 and delay >55):
				self.screen.blit(self.imagef0,(self.x,self.y))
			elif(delay <= 55 and delay >50):
				self.screen.blit(self.imagef1,(self.x,self.y))				
			elif(delay <= 50 and delay > 45):
				self.screen.blit(self.imagef2,(self.x,self.y))
			elif(delay <= 45 and delay > 40):
				self.screen.blit(self.imagef3,(self.x,self.y))
			elif(delay <= 40 and delay > 35):
				self.screen.blit(self.imagef4,(self.x,self.y))
			elif(delay <= 35 and delay > 30):
				self.screen.blit(self.imagef5,(self.x,self.y))
			elif(delay <= 30 and delay > 25):
				self.screen.blit(self.imagef6,(self.x,self.y))
			elif(delay <= 25 and delay > 20):
				self.screen.blit(self.imagef5,(self.x,self.y))
			elif(delay <= 20 and delay > 15):
				self.screen.blit(self.imagef4,(self.x,self.y))
			elif(delay <= 15 and delay > 10):
				self.screen.blit(self.imagef3,(self.x,self.y))
			elif(delay <= 10 and delay > 5):
				self.screen.blit(self.imagef2,(self.x,self.y))
			elif(delay <= 5 and delay > 0):
				self.screen.blit(self.imagef1,(self.x,self.y))

		# shoot the bullets and missiles
		self.shoot(hx,hy,radius)

		#list that stores the bullets which goes out of the boundary
		NoUseBullets1 = list()

		# append the out-of-boundary bullets into the nousebullets1 list
		if(len(self.bulletList1)>0):
			for b in self.bulletList1:
				if b.checkBullet() == True:
					NoUseBullets1.append(b)
		#remove the out-of-boundary bullets from the bulletlist1
		if(len(NoUseBullets1)>0):
			for i in NoUseBullets1:
				self.bulletList1.remove(i)

		# display the bullets and make the bullets move
		for b in self.bulletList1:
			b.display()
			b.move()

		# make the missiles move
		for m in self.missileList:
			m.move(hx,hy)

	# make the boss move based on the location of hero plane
	def move(self,heroX):
		# let the boss appear from the top
		if(self.y <25):
			self.y += 3
		else:
			if(heroX < 270):
				self.x += 3
				if(self.x >350):
					self.x =350
			else:
				self.x -= 3
				if(self.x <0):
					self.x = 0
	# shoot the bullet and missiles
	def shoot(self,hx,hy,radius):
		check = randint(1,150)
		if check == 100:
			for i in range(7):
				newBullet = BossBullet1(self.screen,self.x,self.y,i+1)
				self.bulletList1.append(newBullet)
		# add missiles when the boss health is below 100
		if check == 10 and self.health < 101: 
			newBullet = Missile(self.screen,self.x,self.y,hx,hy,radius)
			self.missileList.append(newBullet)
