import pygame
import os
import time
# game initialization done
pygame.init()

screen_width = 800
screen_height = 480
edge = 3
# open windon on the screen
win = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("First Game")

# Paths
current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'Images') # The resource folder path
#image_path = os.path.join(resource_path, 'images') # The image folder path

#Sound effects
#bulletSound = pygame.mixer.Sound(os.path.join(resource_path, "bullet.wav"))
#hitSound = pygame.mixer.Sound(os.path.join(resource_path, "hit.wav"))
music = pygame.mixer.music.load(os.path.join(resource_path, "music.mp3")) 

pygame.mixer.music.play(-1)
#Images
walkRight = []
for i in range(1,10):
	walkRight.append(pygame.image.load(os.path.join(resource_path, f'R{int(i)}.png')))
walkLeft = []
for i in range(1,10):
	walkLeft.append(pygame.image.load(os.path.join(resource_path, f'L{int(i)}.png')))
bg = pygame.image.load(os.path.join(resource_path, 'bg.jpg'))
char = pygame.image.load(os.path.join(resource_path,'standing.png'))


fps = 27
clock = pygame.time.Clock()


score = 0

# Player object pepe
class player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)

	def draw(self, win):

		win.blit(bg, (0,0))
		if self.walkCount + 1 >= 27:
			self.walkCount = 0
		

		if not(self.standing):
			if self.left:
				win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1

			elif self.right:
				win.blit(walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1

		else:
			if self.right:
				win.blit(walkRight[0], (self.x, self.y))
			else:
				win.blit(walkLeft[0], (self.x, self.y))
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		#pygame.draw.rect(win, (0,0,0), self.hitbox, 2)

	def hit(self):
		self.x  = 300
		self.y = 410
		self.walkCount = 0
		font1 = pygame.font.SysFont('comicsans', 100)
		text = font1.render('-50', 1, (255,0,0))
		win.blit(text, (screen_width/2 - (text.get_width()/2), 200))
		pygame.display.update()
		i = 0
		while i < 100:
			pygame.time.delay(1)
			i += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					i = 301
					pygame.quit()

class projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 9 * facing

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
	walkRight = []
	for i in range(1,12):
		walkRight.append(pygame.image.load(os.path.join(resource_path, f'R{int(i)}E.png')))
	walkLeft = []
	for i in range(1,12):
		walkLeft.append(pygame.image.load(os.path.join(resource_path, f'L{int(i)}E.png')))

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, self.end]
		self.walkCount = 0
		self.vel = 3
		self.hitbox = (self.x + 17, self.y + 12, 31, 57)
		self.health = 10
		self.visible = True


	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount + 1 >= 33:
				self.walkCount = 0

			if self.vel > 0:
				win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
			else:
				win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
				self.walkCount += 1
			#HP bar
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
			pygame.draw.rect(win, (0,130,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))
			#Updates hitbox coordinates
			self.hitbox = (self.x + 17, self.y + 2, 31, 57)
			#Draws hitbox
			#pygame.draw.rect(win, (0,0,0), self.hitbox, 2)

		

	def move(self):
		if self.vel > 0:
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0
		else:
			if self.x + self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0
	def hit(self):
		if self.health - 1 > 0:
			self.health -= 1
		else:
			self.visible = False
		#print("hit")		

def redrawGameWindow():
	win.blit(bg, (0,0))
	pepe.draw(win)
	jose.draw(win)
	text = font.render("Score:  " + str(score), 1, (0,0,0))
	win.blit(text, (670, 20))
	for bullet in bullets:
		bullet.draw(win)

	pygame.display.update()

# Main loop
font = pygame.font.SysFont('comicsans', 30, True)
pepe = player(300,410, 64, 64)
jose = enemy(100, 410, 64, 64, 450)
shootLoop = 0
hitLoop = 0
bullets = []
run = True

while run:
	if jose.visible:
		clock.tick(fps)


		if hitLoop > 0:
			hitLoop += 1
		if hitLoop > 20:
			hitLoop = 0
		if jose.visible:
				if pepe.hitbox[1]  < jose.hitbox[1] + jose.hitbox[3] and pepe.hitbox[1] > jose.hitbox[1]:
					if pepe.hitbox[0] > jose.hitbox[0] and pepe.hitbox[0] < jose.hitbox[0] + jose.hitbox[2]:
						if hitLoop == 0:
							#hitSound.play()
							pepe.hit()
							score -= 50
							hitLoop = 1


		if shootLoop > 0:
			shootLoop += 1
		if shootLoop > 3:
			shootLoop = 0

		#pygame.time.delay(0) #ms

		#Checking for events - clicks, movement of mouse, keys clicked...
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for bullet in bullets:
			if jose.visible:
				if bullet.y - bullet.radius < jose.hitbox[1] + jose.hitbox[3] and bullet.y + bullet.radius > jose.hitbox[1]:
					if bullet.x + bullet.radius > jose.hitbox[0] and bullet.x - bullet.radius < jose.hitbox[0] + jose.hitbox[2]:
						#hitSound.play()
						jose.hit()
						score += 10
						bullets.pop(bullets.index(bullet))

			if bullet.x < screen_width and bullet.x > 0:
				bullet.x  += bullet.vel
			else:
				bullets.pop(bullets.index(bullet))

		#Moving
		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE] and shootLoop == 0:
			#bulletSound.play()
			if pepe.left:
				facing = -1

			else:
				facing = 1

			if len(bullets) < 5:
				bullets.append(projectile(round(pepe.x + pepe.width // 2), round(pepe.y + pepe.height // 2), 6, (255,0,0), facing))
				
			shootLoop = 1

		if keys[pygame.K_RIGHT] and pepe.x < (screen_width - pepe.width - edge):
			pepe.x += pepe.vel
			pepe.right = True
			pepe.left = False
			pepe.standing = False

		elif keys[pygame.K_LEFT] and pepe.x > edge:
			pepe.x -= pepe.vel
			pepe.left = True
			pepe.right = False
			pepe.standing = False

		else:
			pepe.standing = True
			pepe.walkCount = 0
		#Jumping
		if not (pepe.isJump):
			"""if keys[pygame.K_UP] and y > edge:
				y -= vel
			if keys[pygame.K_DOWN] and y < (screen_height - height - edge):
				y += vel"""
			if keys[pygame.K_UP]:
				pepe.isJump = True
				pepe.right = False
				pepe.left = False
				pepe.walkCount = 0
		else:
			if pepe.jumpCount >= -10:
				neg = 1
				if pepe.jumpCount < 0:
					neg = -1
				pepe.y -= (pepe.jumpCount **2) * 0.4 * neg
				pepe.jumpCount -= 1
			else:
				pepe.isJump = False
				pepe.jumpCount = 10

		#You don't want to draw stuff in the main loop - neater with function

		"""win.fill((0,0,0))
		pygame.draw.rect(win, (255, 0, 0), (x,y, width, height))
		pygame.display.update()"""

		redrawGameWindow()
	else:
		run = False
else:
	win.fill((0,0,0))
	big_font = pygame.font.SysFont('comicsans', 90, True)
	txt1 = big_font.render("YOU WON!", 1, (255,255,255))
	txt2 = big_font.render("Your score is: " + str(score), 1, (255,255,255))

	win.blit(txt1, (screen_width/2 - txt1.get_width()/2, screen_height/2 - 50))
	win.blit(txt2, (screen_width/2 - txt2.get_width()/2, screen_height/2 + 50))
	pygame.display.update()
	time.sleep(3)

	pygame.quit()