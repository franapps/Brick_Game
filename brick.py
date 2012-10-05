import os, pygame, random
from pygame.locals import *
pygame.init()

# center window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# basic pygame window stuff (background color needs to be set.)
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

# Draw the players paddle
PADDLEWIDTH = 100
PADDLEHEIGHT = 20
player = pygame.Rect(int((SCREENWIDTH/2)-(PADDLEWIDTH/2)), int(SCREENHEIGHT-PADDLEHEIGHT), PADDLEWIDTH, PADDLEHEIGHT)

# Draw the ball
BALLWIDTH = 10
ball = pygame.Rect(int(SCREENWIDTH/2), int(SCREENHEIGHT/2), BALLWIDTH, BALLWIDTH)

# Handle ball movement and animation
horizontal = 5
vertical = 5
ballSpeed = [horizontal, vertical]

# Handle paddle horizontal movement (the paddle will never move vertically)
paddleSpeed = 5

# set up fonts
font = pygame.font.SysFont(None, 36)
TEXTCOLOR = (255,255,255)

# creates a function to draw text
def drawText(text, font, surface, x, y):
	textobj = font.render(text, 1, TEXTCOLOR)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)

# Setup the bricks
WIDTH = 50
HEIGHT = 20
color = [BLACK, WHITE, RED, GREEN, PURPLE]
bricks = []
# Lays out bricks in 8x8 grid
def drawLevel():
	for i in range(3, 11):
		for j in range(3, 11):
			newBrick = [pygame.Rect((i * WIDTH), (j * HEIGHT), WIDTH, HEIGHT), color[(random.randint(1, 5)-1)], None]
			bricks.append(newBrick)

# Function to check if the ball has hit the paddle - Under construction
def ballHasHitPaddle(ball, paddle):
	if ball.bottom == paddle.top:
		return True
	else:
		return False

# Function to check if the ball has hit a brick.
def ballHasHitBrick(ball, b):
	if ball.bottom == b[0].top or ball.top == b[0].bottom:
		if ball.right >= b[0].left and ball.left <= b[0].right:
			return True
	elif ball.left == b[0].right or ball.right == b[0].left:
		if ball.bottom >= b[0].top and ball.top <= b[0].bottom:
			return True
	else: 
		return False

if __name__ == '__main__':
	Run = True
	lives = 3
	score = 0
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

		# Move the mouse cursor to match the paddle.
		pygame.mouse.set_pos(player.centerx, player.centery)

		# Ball bounces off the walls and ceiling, player loses a life when the ball hits the bottom of the screen.
		ball = ball.move(ballSpeed)
		if ball.left < 0 or ball.right > SCREENWIDTH:
			ballSpeed[0] = -ballSpeed[0]
		if ball.top < 0:
			ballSpeed[1] = -ballSpeed[1]
		if ball.bottom > SCREENHEIGHT:
			ballSpeed[1] = -ballSpeed[1]
			lives -= 1
		if ball.bottom == player.top:
			ballSpeed[1] = -ballSpeed[1]

		screen.fill((20,50,150))

		# Bricks collision detection, if the ball hits a brick, the brick is removed and the ball changes direction.
		for b in bricks:
			if ballHasHitBrick(ball, b):
				if b[0].right == ball.left or b[0].left == ball.right:
					ballSpeed[0] = -ballSpeed[0]
				elif b[0].bottom == ball.top or b[0].top == ball.bottom:
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
		drawText('Lives: %s' % (lives), font, screen, 150, 0)

		# Draw the ball and the paddle
		pygame.draw.rect(screen, WHITE, ball)
		pygame.draw.rect(screen, BLACK, player)

		pygame.display.flip()
		clock.tick(30)	
	pygame.quit()