import pygame
import time

class User(object):
	def __init__(self,name,best):
		self.name = name

		self.best = best
		
		self.score = 0

	def update_score(self,curr_score):
		self.score = curr_score

	def update_best(self):
		if (self.score > int(self.best)):
			self.best = self.score
		else:
			pass