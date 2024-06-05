import pygame, sys, random, time, math


pygame.init()

font_size = 36
font = pygame.font.SysFont('monospace', font_size)

game_over = False
back_img = 'img/space_1.jpg'
width = (1280)
height = (720)
player_size = [60, 75]
centeral_pos = [width / 2, height - (height / 4)]
player_pos = [int(centeral_pos[0]), int(centeral_pos[1])]
lives = 5
live = pygame.image.load('img/hit2.png')
live_pos = 200
score = 0
text_gameover = 'GAME OVER'
label_gameover = font.render(text_gameover, 1, (255, 255, 255))
sencetivityCof = 8   # tune speed of player by x
accelerationCofLef = 0
accelerationCofRig = 0
acceleration = 0

accelCountR = 0
accelCountL = 0

spaceShip = 'img/spaceShip.png'
spaceShip = pygame.image.load(spaceShip)
spaceShip = pygame.transform.scale(spaceShip, (player_size[0], player_size[1]))

enemy_size = [75, 75]
enemy_pos = [random.randint(0, width - enemy_size[0]), 0]
enemy_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
enemy_list = [enemy_pos]
enemy_quantity = 10
player_colour = (255, 51, 153)
speed = 5
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


enemyShip1 = 'img/enemySh1.png'
enemyShip1 = pygame.image.load(enemyShip1)
enemyShip1 = pygame.transform.scale(enemyShip1, (enemy_size[0], enemy_size[1]))

enemyShip2 = 'img/enemySh2.png'
enemyShip2 = pygame.image.load(enemyShip2)
enemyShip2 = pygame.transform.scale(enemyShip2, (enemy_size[0], enemy_size[1]))

boom = pygame.image.load('img/booms.png')
boom = pygame.transform.scale(boom, (2048//5, 1488//5))

enemy_scins = [enemyShip1, enemyShip2]



class Background(pygame.sprite.Sprite):
    
    def __init__(self, imageFile, location):
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load(imageFile)
    	self.rect = self.image.get_rect()
    	self.rect.left, self.rect.top = location
    	self.image = pygame.transform.scale(self.image, (width, height))

bg = Background(back_img, [0,0])

# class spriteSheet:
# 	def __init__(self, filename, clos, raws):
# 		self.sheet = pygame.image.load(filename)
# 		self.cols = cols
# 		self.raws = raws
# 		self.totalCellCount = cols*raws

# 		self.rect=self.sheet.get_rect()
# 		w = self.cellWidth = self.rect.width / cols
# 		h = self.cellHeight = self.rect.height / raws
# 		hw, hh =self.cellCenter = (w/2, h/2)

# 		self.cells = list([])

def show_fps(screen, clock):
    fps_overlay = font.render(str(round(clock.get_fps())), True, (255, 255, 255))
    screen.blit(fps_overlay, (0, 0))

def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < enemy_quantity and delay < 0.1:
		x_pos = random.randint(0, width - enemy_size[0])
		y_pos = 0
		enemy_list.append([int(x_pos), int(y_pos)])

def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		# r = random.randint(0, 1)
		# pygame.draw.rect(screen, enemy_colour, (enemy_pos[0], enemy_pos[1], enemy_size[0], enemy_size[1]))
		screen.blit(enemy_scins[1], (enemy_pos[0], enemy_pos[1]))

def update_enemy_pos(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < height:
			enemy_pos[1] += speed

		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return enemy_pos
	return False

def reDraw():
	show_fps(screen, clock)	
	draw_enemies(enemy_list)
	# pygame.draw.rect(screen, player_colour, (player_pos[0], player_pos[1], player_size[0], player_size[1]))
	screen.blit(spaceShip, (player_pos[0], player_pos[1]))
	pygame.display.update()

		

def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size[0])) or (p_x >= e_x and p_x < (e_x + enemy_size[0])):
		if (e_y >= p_y and e_y < (p_y + player_size[1])) or (p_y >= e_y and p_y < (e_y + enemy_size[1])):
			return True
	return False


def spriteSheetCount():
	c = 8
	r = 6

	totalval = 42
	height = 1488 #/ 6 -->  height of one cell 248
	width = 2048 # / 8 --> widt of one cell  
	hCell = 248 // 5
	wCell =  256 // 5
	cords = []
	x = 0
	y = 0

	for i in range(totalval):
		x += wCell
		if x == width:
			x = 0
			y += hCell
		yield x,y



while not game_over:
	for event in pygame.event.get():
		# print(event)
		if event.type == pygame.QUIT:
			sys.exit()


		# if event.type == pygame.KEYDOWN:

		# 	x = player_pos[0]
		# 	y = player_pos[1]

		# 	if event.key == pygame.K_LEFT:
		# 		if player_pos[0] <= 0:
		# 			pass
		# 		else:
		# 			x -= player_size[0]
		# 	elif event.key == pygame.K_RIGHT:
		# 		if player_pos[0] >= width - player_size[0]:
		# 			pass
		# 		else:
		# 			x += player_size[0]
		# 	player_pos = [x, y]


	x = player_pos[0]
	y = player_pos[1]		
	keys = pygame.key.get_pressed()
	

	if keys[pygame.K_LEFT] and x > 0 + player_size[1]:
		
	# 	if accelerationCofLef < 3.7:
	# 		accelerationCofLef = accelCountL * (accelCountL + 1 ) / 200
	# 		accelerationCofRig = accelCountR * (accelCountR + 1 ) / 200
	# 		accelCountL += 1
	# 		accelCountR -= 1			
	# 	x -= (player_size[0] / (sencetivityCof - accelerationCofLef))
			if acceleration > -3.7:
				acceleration = -accelCountL **2 / 100
				accelCountL -= 1		
			x -= (player_size[0] / (sencetivityCof + acceleration))


	elif keys[pygame.K_RIGHT] and x < width - player_size[1]:
	# 	if accelerationCofRig < 3.7:
	# 		accelerationCofRig = accelCountR * (accelCountR + 1 ) / 200
			
	# 		accelerationCofLef = accelCountL * (accelCountL + 1 ) / 200	
	# 		accelCountR += 1
	# 		accelCountL -= 1	
	# 	x += (player_size[0] / (sencetivityCof - accelerationCofRig))

		if acceleration < 3.7:
			acceleration = accelCountL **2 / 100
			accelCountL += 1
			
		x += (player_size[0] / (sencetivityCof - accelerationCofRig))

	

		



	elif not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
		pass
		# accelerationCofLef = 0
		# accelerationCofRig = 0
		# accelCountL = 0
		# accelCountR = 0



	# print(acceleration)
		
	player_pos = [x, y]
	
	screen.fill([255, 255, 255])
	screen.blit(bg.image, bg.rect)		

	drop_enemies(enemy_list)
	score = update_enemy_pos(enemy_list, score)
	text = 'Score:' + str(score)
	label = font.render(text, 1, (255, 255, 255))
	screen.blit(label, (width - 250, height -100))

	for i in range(lives):
		screen.blit(live, (live_pos, 100))
		live_pos += 27

	live_pos = 200


	if score == 25:
		back_img = 'img/space_2.jpg'
		bg = Background(back_img, [0,0])
		speed += 0.2
		
	elif score == 100:
		back_img = 'img/space_3.jpg'
		bg = Background(back_img, [0,0])
		speed += 0.6
		enemy_quantity += 2
	elif score == 150:
		enemy_quantity += 6

	# print(score)

	if collision_check(enemy_list, player_pos):
		CurPos = collision_check(enemy_list, player_pos)
		readyTo = enemy_list.index(CurPos)
		if lives == 0:
			text_gameover_rect = label_gameover.get_rect()
			text_gameover_rect.center = (width // 2, height // 2)
			bg_colour = (81, 0, 0)
			screen.fill((bg_colour))
			screen.blit(label_gameover, text_gameover_rect)
			pygame.display.flip()
			pygame.time.delay(3000)
			game_over = True
			continue
		else:
			
			lives = lives - 1
			for enemy in CurPos:
				x = CurPos[enemy][0]
				y = CurPos[enemy][1]
				animations = spriteSheetCount()
				# print(x, y)
				for anim in animations:
					r,c = anim
					screen.blit(boom, (x, y), (r, c, 51, 50))
				enemy_list.pop(readyTo)



			# enemy_list.clear()



	
	
	clock.tick(60)
	reDraw()