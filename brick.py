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
#ball = pygame.draw.circle(screen, WHITE, (int(SCREENWIDTH/2),int(SCREENHEIGHT/2)), 5, 0)
BALLWIDTH = 10
ball = pygame.Rect(int(SCREENWIDTH/2), int(SCREENHEIGHT/2), BALLWIDTH, BALLWIDTH)

# Handle ball movement and animation
horizontal = 2
vertical = 2
velocity = [horizontal, vertical]

# Setup the bricks
WIDTH = 50
HEIGHT = 20
color = [BLACK, WHITE, RED, GREEN, PURPLE]
bricks = []
# Lays out bricks in 8x8 grid
for i in range(3, 11):
	for j in range(3, 11):
		newBrick = [pygame.Rect((i * WIDTH), (j * HEIGHT), WIDTH, HEIGHT), color[(random.randint(1, 5)-1)], None]
		bricks.append(newBrick)

# Function to check if the ball has hit a brick. NB This function has not been tested, although theoretically should work.
def ballHasHitBrick(ball, bricks):
	for b in bricks:
		if b[0].right = ball.left or b[0].left = ball.right or b[0].bottom = ball.top or b[0].top = ball.bottom:
			return True
	return False

if __name__ == '__main__':
	Run = True
	while Run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Run = False

		ball = ball.move(velocity)
		if ball.left < 0 or ball.right > SCREENWIDTH:
			velocity[0] = -velocity[0]
		if ball.top < 0 or ball.bottom > SCREENHEIGHT:
			velocity[1] = -velocity[1]

		# Enter code here. If ball hits left or right side of the brick, velocity[0] = -velocity[0]
		# Enter code here. If ball hits the top or bottom of the brick, velocity[1] = -velocity[1]

		screen.fill((20,50,150))

		# Bricks collision detection, if the ball hits a brick, the brick is removed.
		for b in bricks:
			if b[0].colliderect(ball):
				if b[0].right >= ball.left or b[0].left <= ball.right:
					velocity[0] = -velocity[0]
				if b[0].bottom >= ball.top or b[0].top <= ball.bottom:
					velocity[1] = -velocity[1]
				bricks.remove(b)
			pygame.draw.rect(screen, b[1], b[0])

		pygame.draw.rect(screen, WHITE, ball)
		pygame.draw.rect(screen, BLACK, player)

		pygame.display.flip()
		clock.tick(60)	
	pygame.quit()