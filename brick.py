import os, pygame, random, math
from pygame.locals import *
pygame.init()

def waitForPlayerToPressKey():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: # pressing escape quits
					pygame.quit()
				return

# creates a function to draw text
def drawText(text, font, surface, x, y):
	textobj = font.render(text, 1, TEXTCOLOR)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)
	return textrect

# Based on pythagoras theorem, func to find the height given the base (x or horizontal) and hypoteneuse (ballspeed/velocity).
def pythag(x, speed):
	if speed**2 != x**2 + ballSpeed[1]**2:
		ballSpeed[1] = math.sqrt(speed**2 - x**2)
		return ballSpeed[1]
	else:
		return ballSpeed[1]

# Lays out bricks in 8x8 grid
def drawLevel():
	for i in range(3, 11):
		for j in range(3, 11):
			newBrick = [pygame.Rect((i * WIDTH), (j * HEIGHT), WIDTH, HEIGHT), color[(random.randint(1, 5)-1)], None]
			bricks.append(newBrick)

# Function to check if the ball has hit the paddle - Under construction - currently does not recognise side collisions.
def ballHasHitPaddle(ball, paddle):
	if (paddle.top - devy) <= ball.bottom <= (paddle.top + devy):
		if ball.right >= paddle.left and ball.left <= paddle.right:
			return True
	else:
		return False

# Function to check if the ball has hit a brick.
def ballHasHitBrick(ball, b):
	if (b[0].top - devy) <= ball.bottom <= (b[0].top + devy) or (b[0].bottom - devy) <= ball.top <= (b[0].bottom + devy):
		if ball.right >= b[0].left and ball.left <= b[0].right:
			return True
	elif (b[0].right - devx) <= ball.left <= (b[0].right + devx) or (b[0].left - devx) <= ball.right <= (b[0].left + devx):
		if ball.bottom >= b[0].top and ball.top <= b[0].bottom:
			return True
	else: 
		return False

# centre window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# basic pygame window stuff
SCREENWIDTH = 700
SCREENHEIGHT = 500
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("Brick")
clock = pygame.time.Clock()

# set up colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (205, 0, 115)

# Set up the Paddle
PADDLEWIDTH = 100
PADDLEHEIGHT = 20
player = pygame.Rect(int((SCREENWIDTH/2)-(PADDLEWIDTH/2)), int(SCREENHEIGHT-PADDLEHEIGHT), PADDLEWIDTH, PADDLEHEIGHT)
# Handle paddle horizontal movement (the paddle will never move vertically)
paddleSpeed = 5

# Set up the ball
BALLWIDTH = 10
ball = pygame.Rect(int(SCREENWIDTH/2), int(SCREENHEIGHT/2), BALLWIDTH, BALLWIDTH)

# Handle ball movement and deviation.
speed = 5
ballSpeed = [3, 3] # Values for x and y
ballSpeed[1] = pythag(ballSpeed[0], speed)
# Deviation for collision detection. Returns Int value.
devx = int(round(ballSpeed[0]/2))
devy = int(round((ballSpeed[1]/2)+0.6))

# set up fonts
font = pygame.font.SysFont(None, 36)
TEXTCOLOR = (255,255,255)

# Setup the bricks
WIDTH = 50
HEIGHT = 20
color = [BLACK, WHITE, RED, GREEN, PURPLE]
bricks = []

# Game's opening screen
drawText('Welcome to Brick!', font, screen, 250, 200)
drawText('Press any key to play or Esc to quit.', font, screen, 150, 280)
pygame.display.update()
waitForPlayerToPressKey()

while True:
	Run = True
	lives = 3
	score = 0
	pause = False
	moveLeft = moveRight = False
	drawLevel()
	# Run game loop
	while Run:
		for event in pygame.event.get():
			# handles quit event
			if event.type == pygame.QUIT:
				Run = False
			# Handles keybindings
			if event.type == KEYDOWN:
				if event.key == K_LEFT or event.key == ord('a'):
					moveRight = False
					moveLeft = True
				if event.key == K_RIGHT or event.key == ord('d'):
					moveRight = True
					moveLeft = False
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					Run = False
				if event.key == K_SPACE:
					pause = True
				if event.key == K_LEFT or event.key == ord('a'):
					moveLeft = False
				if event.key == K_RIGHT or event.key == ord('d'):
					moveRight = False
		# Handles control using the mouse
			if event.type == MOUSEMOTION:
				# If the mouse moves, move the paddle where the cursor is.
				player.move_ip(event.pos[0] - player.centerx, 0)

		# Move the paddle left and right.
		if moveLeft and player.left > 0:
			player.move_ip(-1 * paddleSpeed, 0)
		if moveRight and player.right < SCREENWIDTH:
			player.move_ip(paddleSpeed, 0)

		# Stop the paddle from moving off screen
		if player.left < 0:
			player.left = 0
		if player.right > SCREENWIDTH:
			player.right = SCREENWIDTH

		# Move the mouse cursor to match the paddle.
		pygame.mouse.set_pos(player.centerx, player.centery)

		# Ball bounces off the walls and ceiling, player loses a life when the ball hits the bottom of the screen.
		ball = ball.move(ballSpeed)
		if ball.left < 0 or ball.right > SCREENWIDTH:
			ballSpeed[0] = -ballSpeed[0]
		if ball.top < 0:
			ballSpeed[1] = -ballSpeed[1]
		if ball.bottom > SCREENHEIGHT:
			lives -= 1
			ball.centerx = int(SCREENWIDTH/2)
			ball.centery = int(SCREENHEIGHT/2)
			pause = True
		if ballHasHitPaddle(ball, player): 
			if (player.top - devy) <= ball.bottom <= (player.top + devy):
				if player.left <= ball.centerx <= (player.centerx - 25):
					ballSpeed[0] = -3
					ballSpeed[1] = pythag(ballSpeed[0], speed)
				if (player.centerx - 25) <= ball.centerx < player.centerx:
					ballSpeed[0] = -1
					ballSpeed[1] = pythag(ballSpeed[0], speed)
				if player.centerx < ball.centerx <= (player.centerx + 25):
					ballSpeed[0] = 1
					ballSpeed[1] = pythag(ballSpeed[0], speed)
				if (player.centerx + 25) <= ball.centerx <= player.right:
					ballSpeed[0] = 3
					ballSpeed[1] = pythag(ballSpeed[0], speed)
				ballSpeed[1] = -ballSpeed[1]

		screen.fill((20,50,150))

		# Bricks collision detection, if the ball hits a brick, the brick is removed and the ball changes direction.
		for b in bricks:
			if ballHasHitBrick(ball, b):
				if (b[0].right - devx) <= ball.left <= (b[0].right + devx) or (b[0].left - devx) <= ball.right <= (b[0].left + devx):
					ballSpeed[0] = -ballSpeed[0]
				elif (b[0].top - devy) <= ball.bottom <= (b[0].top + devy) or (b[0].bottom - devy) <= ball.top <= (b[0].bottom + devy):
					ballSpeed[1] = -ballSpeed[1]
				else:
					None
				bricks.remove(b)
				score += 100
			pygame.draw.rect(screen, b[1], b[0])

		# Every 5000 points the player gains an extra life
		if score != 0 and score % 5000 == 0:
			lives += 1
			score += 1

		# Draw the no. of lives and current score on the screen
		drawText('Score: %s' % (score), font, screen, 10, 0)
		drawText('Lives: %s' % (lives), font, screen, 200, 0)

		# Draw the ball and the paddle
		pygame.draw.rect(screen, WHITE, ball)
		pygame.draw.rect(screen, BLACK, player)

		# Pause Loop.
		while pause == True:
			drawText('PAUSED', font, screen, int((SCREENWIDTH/2)-50), int((SCREENHEIGHT/2)-7))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pause = False
					Run = False
				if event.type == KEYUP:
					if event.key == K_ESCAPE:
						pause = False
						Run = False
					if event.key == K_SPACE:
						pause = False
			if lives == 0:
				break

		if lives == 0 or len(bricks) == 0:
			Run = False

		pygame.display.flip()
		clock.tick(60)

	if lives == 0:
		screen.fill((20,50,150))
		drawText('GAME OVER, YEAH', font, screen, 250, 200)
		drawText('Press any key to play again or Esc to quit.', font, screen, 100, 240)
		pygame.display.update()
		waitForPlayerToPressKey()
	elif len(bricks) == 0:
		drawText('You Won!', font, screen, 250, 200)
		drawText('Press any key to play again or Esc to quit.', font, screen, 100, 240)
		pygame.display.update()
		waitForPlayerToPressKey()
	else:
		break
pygame.quit()