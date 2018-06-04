'''

XIAOJIE XING
ID:

YE WANG
ID:

Final Project: Classic Raiden

'''
import pygame
import time
from random import*
from LoadMusic import*
from bullets import*
from heroPlane import*
from enemies import*
from boss import*
from math import*
from user import*
from graph import*
from breadth_first_search import*


pygame.init()

# size of window
Screen_W = 600
Screen_H = 900

# show on the top of window
pygame.display.set_caption("Classic Raiden")


CLOCK = pygame.time.Clock()

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
PINK = (255, 102, 153)
ORANGE = (255, 51, 0)
YELLOW = (255, 255, 102)
LIGHT_GREEN = (102, 255, 102)
GRASS_GREEN = (63, 255, 94)

# define size of fonts
font = pygame.font.SysFont(None,28)
font2 = pygame.font.SysFont(None,80)
font3 = pygame.font.SysFont(None,30)
font4 = pygame.font.SysFont(None,35)
font5 = pygame.font.SysFont(None,29)

# create the window
gameDisplay = pygame.display.set_mode([Screen_W,Screen_H])

player = None

# define keyboard
key_list = [pygame.K_a,
			pygame.K_b,
			pygame.K_c,
			pygame.K_d,
			pygame.K_e,
			pygame.K_f,
			pygame.K_g,
			pygame.K_h,
			pygame.K_i,
			pygame.K_j,
			pygame.K_k,
			pygame.K_l,
			pygame.K_m,
			pygame.K_n,
			pygame.K_o,
			pygame.K_p,
			pygame.K_q,
			pygame.K_r,
			pygame.K_s,
			pygame.K_t,
			pygame.K_u,
			pygame.K_v,
			pygame.K_w,
			pygame.K_x,
			pygame.K_y,
			pygame.K_z]


user_relations = Graph()
user_relation_list = list()
user_data = dict()

# display the score
def display_score(msg,color):
	screen_text = font.render(msg,True,color)
	gameDisplay.blit(screen_text,[5,5])

# algorithm for when should we add enemies
def add_enemies(em_list,num):
	for i in range(num):
		temp = randint(1,2)
		if temp == 1:
			enemy = EnemyPlane1(gameDisplay)
			em_list.append(enemy)
		elif temp == 2:
			enemy = EnemyPlane2(gameDisplay)
			em_list.append(enemy)

# check when to reset boss and how the boss loses its health
def check_boss_reset(boss,heroPlane,em_delay):
	for bullet in heroPlane.bulletList:
		if bullet.y >= boss.y and bullet.y <= boss.y + 364:
			if bullet.x >= boss.x and bullet.x <= boss.x + 242:
				boss.health -= 2
				heroPlane.bulletList.remove(bullet)


	if(boss.health <= 0):
			boss.exp = True
			bDown.play()
			boss.active = False
			bDown.play()

# display images when the boss down
def boss_explode(boss,boss_delay):
		if boss_delay >= 70 and boss_delay < 80:
			gameDisplay.blit(boss.dest_images[0],(boss.x,boss.y))
		elif boss_delay >= 60 and boss_delay < 70:
			gameDisplay.blit(boss.dest_images[1],(boss.x,boss.y))
		elif boss_delay >= 50 and boss_delay < 60:
			gameDisplay.blit(boss.dest_images[2],(boss.x,boss.y))
		elif boss_delay >= 40 and boss_delay < 50:
			gameDisplay.blit(boss.dest_images[3],(boss.x,boss.y))
		elif boss_delay >= 30 and boss_delay < 40:
			gameDisplay.blit(boss.dest_images[4],(boss.x,boss.y))
		elif boss_delay >= 20 and boss_delay < 30:
			gameDisplay.blit(boss.dest_images[5],(boss.x,boss.y))
		elif boss_delay >= 10 and boss_delay < 20:
			gameDisplay.blit(boss.dest_images[6],(boss.x,boss.y))
		elif boss_delay >= 1 and boss_delay < 10:
			gameDisplay.blit(boss.dest_images[7],(boss.x,boss.y))
		else:
			pass

# check when to reset boss missiles 
def check_missile_reset(hb_list,m_list):
	if(len(hb_list)>0 and len(m_list)>0):
		# check hero plane bullets whether collide with boss missiles
		for b in hb_list:
			for m in m_list:
				if b.y >= int(m.y1-m.radius) and b.y <= int(m.y1 + m.radius):
					if b.x >= int(m.x1-m.radius)-3 and b.x <= int(m.x1+m.radius)+3:
						hb_list.remove(b)
						mDown.play()
						m_list.remove(m)

	# set the limit of missiles
	if len(m_list) > 6:
		m_list.pop(0)

# check when should we reset enemies
def check_em_reset(em_list,heroPlane,em_delay):
	# if enemies go out of boundary
	for i in em_list:
		if(i.y >= 900):
			i.active = False
		
		# if beroplane bullet collide with enemies
		for bullet in heroPlane.bulletList:
			if bullet.y >= i.y and bullet.y <= i.y+60:
				if bullet.x >= i.x and bullet.x <= i.x+42:
					i.active = False

					ed_sound.play()

					if em_delay >= 35 and em_delay < 60:
						gameDisplay.blit(i.dest_images[0],(i.x,i.y))
					elif em_delay < 35 and em_delay >= 10:
						gameDisplay.blit(i.dest_images[1],(i.x,i.y))
					elif em_delay < 10:
						gameDisplay.blit(i.dest_images[2],(i.x,i.y))

					heroPlane.bulletList.remove(bullet)
					heroPlane.score += 10

# dispaly the images of destroying hero plane
def hero_exp(heroPlane,hero_delay):
	hd_sound.play()
	if hero_delay > 25 and hero_delay < 15:
		gameDisplay.blit(heroPlane.dest_images[0],(heroPlane.x,heroPlane.y))
	elif hero_delay < 15 and hero_delay > 5:
		gameDisplay.blit(heroPlane.dest_images[1],(heroPlane.x,heroPlane.y))
	elif hero_delay < 5:
		gameDisplay.blit(heroPlane.dest_images[2],(heroPlane.x,heroPlane.y))

	if hero_delay == 0:
		heroPlane.reset()

# game loop
def gameLoop():
	# backgound image
	back_gorund = pygame.image.load('./bg/galx2.jpg').convert()
	intro_bg = pygame.image.load('./bg/galx3.jpg').convert()

	# initialize the state
	state = 0
	user_name = ''
	friend_name = ''

	# play the backgound  music
	pygame.mixer.music.play(-1)

	# create the hero plane
	heroPlane = HeroPlane(gameDisplay)

	changeX= 0
	changeY= 0

	# delays for displaying animations
	hero_delay = 25
	em_delay = 60

	index = 0
	boss_delay = 80
	
	# enemies list
	em_list = list()
	add_enemies(em_list,6)
	chance = 100
	
	boss_list = list()
	boss_list.append(Boss(gameDisplay))

	adding_friends = False

	# check if we need to research the graph and data dict
	check_list = True
	friend_score = list()
	index = 0
	check_friend = False

	# the initial state
	while state ==0:
		for event in pygame.event.get():
			# quit the game
			if event.type == pygame.QUIT:
				state = -1
			if event.type == pygame.KEYDOWN:
				# go to the next state
				if event.key == pygame.K_RETURN:
					state = 1
				# ESC to quit
				if event.key == pygame.K_ESCAPE:
					state = -1
		# display the background
		gameDisplay.blit(intro_bg,(0,0))

		# display the start information
		intro_txt = 'Classic Raiden'
		screen_msg = font2.render(intro_txt,True,WHITE)
		gameDisplay.blit(screen_msg,[100,200])

		login_txt = 'Press Enter to Login'
		font4.set_italic(True)
		font4.set_bold(True)
		login_msg = font4.render(login_txt,True,WHITE)
		gameDisplay.blit(login_msg,[180,290])

		esc_txt = 'Press Esc to Quit'
		font.set_italic(True)
		esc_msg = font.render(esc_txt,True,WHITE)
		gameDisplay.blit(esc_msg,[225,325])

		how_title = "How to Play:"
		how_msg = font.render(how_title,True,WHITE)
		gameDisplay.blit(how_msg,[10,580])

		shoot_txt = "Press Space Bar to shoot"
		shoot_msg = font.render(shoot_txt,True,WHITE)
		gameDisplay.blit(shoot_msg,[10,610])

		move_txt = "Press Up Down and Left Right keys to move"	
		move_msg = font.render(move_txt,True,WHITE)
		gameDisplay.blit(move_msg,[10,640])

		pygame.display.update()
		CLOCK.tick(70)

	# login state
	while state == 1:

		load_user = False
		# background
		gameDisplay.blit(intro_bg,(0,0))

		# teach player how to log in 
		login_txt = 'Please Enter Your Name and Press Enter'
		font3.set_bold(True)
		login_msg = font3.render(login_txt,True,WHITE)
		gameDisplay.blit(login_msg,[65,240])

		esc_txt = 'Press Esc to Quit'
		font.set_italic(True)
		esc_msg = font.render(esc_txt,True,WHITE)
		gameDisplay.blit(esc_msg,[195,360])

		# the input rectangle
		pygame.draw.rect(gameDisplay,WHITE,[150, 300, 300, 50])


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				state = -1
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if len(user_name)< 1:
						pass
					else:
						adding_friends = True
						load_user = True
				elif event.key == pygame.K_ESCAPE:
					state = -1
				# delete letter
				elif event.key == pygame.K_BACKSPACE:
					user_name = user_name[:-1]
				# set the limit of user name and change to corresponding string
				elif event.key in key_list:
					if len(user_name) < 12:
						user_name += event.unicode

		# convert to only upper case letters
		user_name = user_name.upper()
		# display the user name
		name_msg = font4.render(user_name,True,BLACK)
		font4.set_bold(False)
		gameDisplay.blit(name_msg,[165,313])

		if(load_user == True):
			# if user in data base, load user information
			if user_name in user_data:
				player = User(user_name,user_data[user_name])
			else:
			# if user not in data base, add into data base
				player = User(user_name,0)
				user_relations.add_vertex(user_name)
				user_relations.add_edge((user_name,user_name))
				global user_relation_list
				user_relation_list.append((user_name,user_name))
				user_data[user_name] = 0

			state = 2

		pygame.display.update()
		CLOCK.tick(70)
	
	while adding_friends == True:
		while state == 2:
			gameDisplay.blit(intro_bg,(0,0))

			friends = set()

			# use bsf to iter through the graph of current player relations to determine the
			# friend zone list
			if(check_list == True):
				friends = set(breadth_first_search(user_relations,player.name).keys())
				for friend in friends:
					friend_score.append((friend,int(user_data[friend])))
				friend_score = set(friend_score)
				friend_score = list(friend_score)
				friend_score = sorted(friend_score,key = lambda x:x[1])
				friend_score = list(reversed(friend_score))
				check_list = False

			title = "Top Players in Your Friend Zone"
			title_msg = font4.render(title,True,WHITE)
			font4.set_bold(True)
			gameDisplay.blit(title_msg,[80,35])

			# print top 9 best scores in the friend zone on to screen
			for index in range(min(len(friend_score),9)):
				txt = "{}.   {}     {}".format(index+1,friend_score[index][0],friend_score[index][1])
				txt_msg = font5.render(txt,True,WHITE)
				font5.set_bold(True)
				gameDisplay.blit(txt_msg,[170,75+28*index])
				# print(txt)

			my_txt = "Your Best Score: {}".format(player.best)
			my_msg = font3.render(my_txt,True,WHITE)
			gameDisplay.blit(my_msg,[145,355])		

			chg = 'Press Space bar to Add New Friend'
			chg_msg = font4.render(chg,True,WHITE)
			gameDisplay.blit(chg_msg,[20,550])

			start = "Press Enter to Start New Game"
			start_msg = font4.render(start,True,WHITE)
			gameDisplay.blit(start_msg,[20,590])

			back = "Press ESC to Quit"
			back_msg = font4.render(back,True,WHITE)
			gameDisplay.blit(back_msg,[20,630])


			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					state = -1
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						state +=2
					elif event.key == pygame.K_ESCAPE:
						state =-1
					elif event.key == pygame.K_SPACE:
						state += 1


			pygame.display.update()
			
			CLOCK.tick(70)


		while state == 3:
			gameDisplay.blit(intro_bg,(0,0))
			added_firend = False

			add_txt = 'Please Enter Friend\'s name and Press Enter'
			font3.set_bold(True)
			add_msg = font3.render(add_txt,True,WHITE)
			gameDisplay.blit(add_msg,[37,240])

			esc_txt = 'Press Esc to Quit'
			font.set_italic(True)
			esc_msg = font.render(esc_txt,True,WHITE)
			gameDisplay.blit(esc_msg,[215,360])

			pygame.draw.rect(gameDisplay,WHITE,[150, 300, 300, 50])

			# read in friend name, only upper case allowed
			# system automatically changes lower case to upper case
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					state = -1
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						if len(friend_name)< 1:
							pass
						else:
							check_friend = True
					elif event.key == pygame.K_ESCAPE:
						state = -1
					elif event.key == pygame.K_BACKSPACE:
						friend_name = friend_name[:-1]
					elif event.key == pygame.K_SPACE:
						state = 2
					elif event.key in key_list:
						if len(friend_name) < 12:
							friend_name += event.unicode

			friend_name = friend_name.upper()
			name_msg = font4.render(friend_name,True,BLACK)
			font4.set_bold(False)
			gameDisplay.blit(name_msg,[165,313])

			if(check_friend == True):
				# if friend name in database, add relation to graph and database
				if user_relations.is_vertex(friend_name) == True:
					user_relations.add_edge((player.name,friend_name))
					user_relations.add_edge((friend_name,player.name))
					# global user_relation_list
					user_relation_list.append((player.name,friend_name))
					check_list = True
					added_firend = True
				else:
				# if friend name not in database, show error message
					err_txt = 'Invalid Name, Try Again'
					err_msg = font.render(err_txt,True,WHITE)
					gameDisplay.blit(err_msg,[195,270])

			if(added_firend == True):
			# display add friend success
				txt = 'Friend Added, Press Space to Go Back'
				msg = font.render(txt,True,WHITE)
				gameDisplay.blit(msg,[135,270])


			pygame.display.update()
			
			CLOCK.tick(70)
		if(state != 2 and state != 3):
			# print(friend_score)
			user_relation_list = set(user_relation_list)
			user_relation_list = list(user_relation_list)
			adding_friends = False


	# let's start the game!
	while state == 4:

		check_friend = False

		for event in pygame.event.get():
			# quit
			if event.type == pygame.QUIT:
				state = -1

			# control the heroplane
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					changeX = -5
				elif event.key == pygame.K_RIGHT:
					changeX = 5
				if event.key == pygame.K_UP:
					changeY = -5
				elif event.key == pygame.K_DOWN:
					changeY = 5
				
				if event.key == pygame.K_SPACE:
					heroPlane.shoot()
			# move the plane continuously
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					changeX = 0
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					changeY = 0

		# display the background
		gameDisplay.blit(back_gorund,(0,0))
		# check whether the heroplane is down
		check_hero_reset(em_list,heroPlane,boss_list[0])

		# if the hero plane is down, display the destroying images
		if(heroPlane.active == False):
			hero_exp(heroPlane,hero_delay)

		# if runing out of lives, go next state
		if heroPlane.check_end() == True:
				state = 5
		
		# when the hero plane is active
		if(heroPlane.active):
			heroPlane.moveHorz(changeX)
			heroPlane.moveVert(changeY)
			heroPlane.checkBound()
			heroPlane.display(em_delay)

		# when should the boss spawn
		if(heroPlane.score % 500 == 0 and heroPlane.score != 0):
			boss_list[0].active = True

		# if the boss is active
		if(boss_list[0].active):
			# display the boss
			boss_list[0].display(em_delay,heroPlane.x+45,heroPlane.y+35,8)
			# let the boss move
			boss_list[0].move(heroPlane.x)
			# check when should we reset boss missiles
			check_missile_reset(heroPlane.bulletList,boss_list[0].missileList)
			# check when should we reset boss
			check_boss_reset(boss_list[0],heroPlane,em_delay)
			chance = 500

		# if the boss is  exploding
		if(boss_list[0].exp):
			# display the destroying images
			boss_explode(boss_list[0],boss_delay)
			if(boss_delay <2):
				boss_list = list()
				boss_list.append(Boss(gameDisplay))
				chance = 100
				# calculate for the score after killing a boss
				heroPlane.score += (500 - (heroPlane.score % 500))+10

		# check the when to reset enemies
		check_em_reset(em_list,heroPlane,em_delay)

		# let the enemies move and shoot and display
		for plane in em_list:
			if plane.active:
				plane.move()
				plane.display(chance)
			else:
				# enemy respawn count depends on players current score, thus
				# the game difficulty changes as player gaining more score
				em_list.remove(plane)
				value = int (heroPlane.score / 1000)
				if(value > 0 and value < 3):
					add_enemies(em_list,min(randint(1,value),2))
				elif(value >3):
					add_enemies(em_list,min(randint(1,value),3))
				else:
					add_enemies(em_list,1)

		# display the score
		display_score("Score: {}".format(heroPlane.score),WHITE)
		# display the lives
		life_txt = "Lives: {}".format(heroPlane.life)
		life_msg= font.render(life_txt,True,WHITE)
		gameDisplay.blit(life_msg,[500,5])

		# delay for animations
		if hero_delay ==0:
			hero_delay = 35
		hero_delay -= 1

		if em_delay == 0:
			em_delay = 60
		em_delay -= 1

		if boss_list[0].health <= 2:
			boss_delay -= 1
		if boss_delay == 0:
			boss_delay = 80

		pygame.display.update()
		CLOCK.tick(70)

	# final state
	while state == 5:
		# display background
		gameDisplay.blit(intro_bg,(0,0))

		# update the best score compared with current score
		if(player.score == 0):
			player.update_score(heroPlane.score)
			player.update_best()
			user_data[player.name] = player.best

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				state = -1
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					state = -1

		# display information about the user 
		go_txt = "Game Over"
		go_msg = font2.render(go_txt,True,WHITE)
		gameDisplay.blit(go_msg,[150,200])

		ys_txt = "Your Score: {}".format(heroPlane.score)
		ys_msg = font4.render(ys_txt,True,WHITE)
		gameDisplay.blit(ys_msg,[200,280])

		bs_txt = "Your Best: {}".format(player.best)
		bs_msg = font4.render(bs_txt,True,WHITE)
		gameDisplay.blit(bs_msg,[200,320])

		qt_txt = "Press Esc to Quit"
		qt_msg = font.render(qt_txt,True,WHITE)
		gameDisplay.blit(qt_msg,[230,350])

		pygame.display.update()
		CLOCK.tick(70)

	# quit state
	if state == -1:
		pygame.quit()

def read_graph_undirected(user_relations,user_data,relations_file,data_file,user_relation_list):
	data = open(data_file,'r').readlines()
	for line in data:
		line = line.split()
		if line[0] == 'V':
			user_relations.add_vertex(line[1])
			user_data[line[1]] = line[2]

	relations = open(relations_file,'r').readlines()
	for line in relations:
		line = line.split()
		if line[0] == 'E':
			user_relation_list.append((line[1],line[2]))
			user_relations.add_edge((line[1],line[2]))
			user_relations.add_edge((line[2],line[1]))

def save_file(user_relation_list,user_data,userData,userRelations):
	relations = open(userRelations,'w')
	for i in user_relation_list:
		relations.write("E ")
		relations.write("%s " % str(i[0]))
		relations.write("%s\n" % str(i[1]))
	relations.close()

	d_list = list()

	for key in user_data:
		temp = (key,user_data[key])
		d_list.append(temp)

	data = open(userData,'w')
	for j in d_list:
		data.write('V ')
		data.write("%s " % str(j[0]))
		data.write("%s\n" % str(j[1]))
	data.close()



		
if __name__ == "__main__":

	# read previous user information from database
	read_graph_undirected(user_relations,user_data,'userRelations.txt','userData.txt',user_relation_list)

	# run game
	gameLoop()

	# save user profile at end of game
	save_file(user_relation_list,user_data,'userData.txt','userRelations.txt')

	quit()