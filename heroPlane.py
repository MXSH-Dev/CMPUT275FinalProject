import pygame
import time
from random import*
from LoadMusic import*
from bullets import*
from enemies import BasePlane

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255, 102, 153)
ORANGE = (255, 51, 0)
YELLOW = (255, 255, 102)
LIGHT_GREEN = (102, 255, 102)
# size of window
Screen_W = 600
Screen_H = 900

# check when the hero plane is destroyed
def check_hero_reset(em_list,heroPlane,boss):
	for em in em_list: # collide with enemies
		if(em.y+60 >= heroPlane.y and em.y <= heroPlane.y):
			if(heroPlane.x+60 > em.x and heroPlane.x +60 <em.x+50):
				em.reset()
				heroPlane.active = False
			elif(heroPlane.x < em.x+50 and heroPlane.x > em.x):
				em.reset()
				heroPlane.active = False
			elif(heroPlane.x +30 <= em.x+50 and heroPlane.x+30 >= em.x):
				em.reset()
				heroPlane.active = False		
		if(heroPlane.y+50 >= em.y and heroPlane.y <= em.y):
			if(heroPlane.x+60 > em.x and heroPlane.x +60 <em.x+50):
				em.reset()
				heroPlane.active = False
			elif(heroPlane.x < em.x+50 and heroPlane.x > em.x):
				em.reset()
				heroPlane.active = False
			elif(heroPlane.x +30 <= em.x+50 and heroPlane.x+30 >= em.x):
				em.reset()
				heroPlane.active = False
		# collide with enemies' bullets	
		for bullet in em.bulletList:
			if bullet.y+10 >= heroPlane.y and bullet.y+10 <= heroPlane.y+50:
				if bullet.x >= heroPlane.x and bullet.x <= heroPlane.x+52:
					heroPlane.active = False
					em.bulletList.remove(bullet)
	
	if boss.active:
		# collide with boss
		if(boss.y+330 >= heroPlane.y and boss.y <= heroPlane.y):
			if(heroPlane.x+60 > boss.x and heroPlane.x +60 <boss.x+250):
				heroPlane.active = False
			elif(heroPlane.x < boss.x+250 and heroPlane.x > boss.x):
				heroPlane.active = False
			elif(heroPlane.x +30 <= boss.x+250 and heroPlane.x+30 >= boss.x):
				heroPlane.active = False		
		if(heroPlane.y+50 >= boss.y and heroPlane.y <= boss.y):
			if(heroPlane.x+60 > boss.x and heroPlane.x +60 <boss.x+250):
				heroPlane.active = False
			elif(heroPlane.x < boss.x+250 and heroPlane.x > boss.x):
				heroPlane.active = False
			elif(heroPlane.x +30 <= boss.x+250 and heroPlane.x+30 >= boss.x):
				heroPlane.active = False
		# collide with boss bullets
		for b in boss.bulletList1:
			if b.y + 12 >= heroPlane.y and b.y + 12 <= heroPlane.y +50:
				if b.x -5 >= heroPlane.x and b.x + 5 <= heroPlane.x + 60:
					heroPlane.active = False
					boss.bulletList1.remove(b)
		# collide with boss missiles
		for m in boss.missileList:
			if int(m.y1) >= heroPlane.y and int(m.y1) <= heroPlane.y+50:
				if int(m.x1) >= heroPlane.x and int(m.x1) <= heroPlane.x+60:
					heroPlane.active = False
					boss.missileList.remove(m)

# class for hero plane
class HeroPlane(BasePlane):
	def __init__(self,screen):
		# spawning location
		self.x = int(Screen_W/2-30)
		self.y = 850

		self.screen = screen
		# total lives for hp
		self.life = 3
		# load images
		self.image1 = pygame.image.load("./planes/hp1.gif").convert()
		self.image2 = pygame.image.load("./planes/hp2.gif").convert()
		self.image3 = pygame.image.load("./planes/hp3.gif").convert()
		self.image4 = pygame.image.load("./planes/hp4.gif").convert()
		self.image5 = pygame.image.load("./planes/hp5.gif").convert()

		self.bulletList = list()

		# initial score
		self.score = 0

		self.active = True

		self.dest_images = list()
		# destroying images
		self.dest_images.extend([
				pygame.image.load('./planes/heroexplode1.gif').convert(),
				pygame.image.load('./planes/heroexplode2.gif').convert(),
				pygame.image.load('./planes/h_final1.gif').convert()

			])
	
	# display the hero plane
	def display(self,delay):
		# count for different images of hero plane
		if(delay <= 60 and delay >54):
			self.screen.blit(self.image1,(self.x,self.y))
		elif(delay <= 54 and delay >48):
			self.screen.blit(self.image2,(self.x,self.y))				
		elif(delay <= 48 and delay > 42):
			self.screen.blit(self.image3,(self.x,self.y))
		elif(delay <= 42 and delay > 36):
			self.screen.blit(self.image4,(self.x,self.y))
		elif(delay <= 36 and delay > 30):
			self.screen.blit(self.image5,(self.x,self.y))
		elif(delay <= 30 and delay > 24):
			self.screen.blit(self.image5,(self.x,self.y))
		elif(delay <= 24 and delay > 18):
			self.screen.blit(self.image4,(self.x,self.y))
		elif(delay <= 18 and delay > 12):
			self.screen.blit(self.image3,(self.x,self.y))
		elif(delay <= 12 and delay > 6):
			self.screen.blit(self.image2,(self.x,self.y))
		elif(delay <= 6 and delay > 0):
			self.screen.blit(self.image1,(self.x,self.y))


		NoUseBullets = list()

		# clear the useless bullets
		if(len(self.bulletList)>0):
			for b in self.bulletList:
				if b.checkBullet() == True:
					NoUseBullets.append(b)
		
		if(len(NoUseBullets)>0):
			for i in NoUseBullets:
				self.bulletList.remove(i)

		# display and move bullets
		for b in self.bulletList:
			b.display()
			b.move()

	# move horizontally
	def moveHorz(self,changeX):
		self.x +=changeX

	# move vertically
	def moveVert(self,changeY):
		self.y +=changeY

	# cant move out of boundary
	def checkBound(self):
		if(self.x <= 0):
			self.x =0
		elif(self.x >= 540):
			self.x = 540

		if(self.y <=0):
			self.y =0
		elif(self.y >=840):
			self.y = 840

	# shoot bullets
	def shoot(self):
		hb_sound.play()
		newBullet = HeroBullet(self.screen,self.x,self.y)
		self.bulletList.append(newBullet)

	# reset the heroplane
	def reset(self):
		self.x = int(Screen_W/2-30)
		self.y = 850
		if self.life > 0:
			self.life -=1

		self.active = True
	
	# check whether game over
	def check_end(self):
		if self.life <= 0:
			return True
		else:
			return False
