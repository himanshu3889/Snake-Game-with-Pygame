import pygame
from pygame.locals import *
import time
import random

SIZE = 25
BACKGROUND_COLOR = (41, 52, 94)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

# Food Class  ----------------------------
class Food:
    def __init__(self, parentScreen):
        self.parentScreen = parentScreen
        self.x = random.randint(1,WINDOW_WIDTH//SIZE-1)*SIZE
        self.y = random.randint(1,WINDOW_HEIGHT//SIZE-1)*SIZE

    def draw(self):
        color = 255, 0, 255
        pygame.draw.circle(self.parentScreen, color,(self.x,self.y),SIZE//2-2, SIZE//2-2)
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,WINDOW_WIDTH//SIZE-1)*SIZE
        self.y = random.randint(1,WINDOW_HEIGHT//SIZE-1)*SIZE



# Snake Class ------------------------
class Snake:
    def __init__(self, parentScreen):
        self.parentScreen = parentScreen
        self.direction = 'down'
        self.length = 1

        self.x = [SIZE]   # inital x size
        self.y = [SIZE]   # initial y size

    def moveLeft(self):
        if self.direction != 'right' :
            self.direction = 'left'

    def moveRight(self):
        if self.direction != 'left' :
            self.direction = 'right'

    def moveUp(self):
        if self.direction != 'down' :
            self.direction = 'up'

    def moveDown(self):
        if self.direction != 'up' :
            self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()

    def draw(self):
        radius = width = SIZE//2
        ## draw the head
        color , pos = (255, 0, 0) , (self.x[0],self.y[0])
        pygame.draw.circle(self.parentScreen, color,pos, radius, width)
        ## draw the body
        for i in range(1,self.length):
            color , pos = (255, 255, 0) , (self.x[i],self.y[i])
            pygame.draw.circle(self.parentScreen, color,pos, radius, width)
        pygame.display.flip()

    def increaseLength(self):
        self.length += 1
        self.x.append(-1)   # random value when move it grab the next block 
        self.y.append(-1)


# Game ---------------------------
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init()
        self.playBackgroundMusic()

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.food = Food(self.surface)
        self.food.draw()

    def renderBackground(self):
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.flip

    def playBackgroundMusic(self):
        pygame.mixer.music.load('resources/backgroundMusic.mp3')
        pygame.mixer.music.play(2, 0)

    def playSound(self, sound_name):
        if sound_name == "collision":
            sound = pygame.mixer.Sound("resources/collision.wav")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")
        pygame.mixer.Sound.play(sound)


    def snakeEatApple(self):
        if self.snake.x[0] == self.food.x and self.snake.y[0] == self.food.y :
            self.playSound("ding")
            self.snake.increaseLength()
            self.food.move()

    def isSnakeCollide(self):
        # Snake collide border
        if self.snake.x[0] <= 0 or self.snake.x[0] >= WINDOW_WIDTH or self.snake.y[0] <= 0 or self.snake.y[0] >= WINDOW_HEIGHT :
            self.playSound('collision')
            raise "Collision Occurred"

        # Snake collide itself-
        for i in range(3, self.snake.length):
            x1 , y1 = self.snake.x[0] , self.snake.y[0]
            x2 , y2 = self.snake.x[i] , self.snake.y[i]
            if x1 == x2 and y1 == y2 :
                self.playSound('collision')
                raise "Collision Occurred"


    def displayScore(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    def gameOver(self):
        self.renderBackground()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over!  Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, WINDOW_HEIGHT//2-50 ))
        line2 = font.render("Press Space to play again. Press Escape to Exit!", True, (255, 255, 255))
        self.surface.blit(line2, (200,WINDOW_HEIGHT//2))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def restartGame(self):
        self.snake = Snake(self.surface)
        self.food = Food(self.surface)


    def play(self):
        pygame.mixer.music.unpause()
        self.renderBackground()
        self.snake.walk()
        self.food.draw()
        self.displayScore()
        pygame.display.flip()
        # snake eating food 
        self.snakeEatApple()
        # snake colliding with itself and boundary
        self.isSnakeCollide()
    
    def pauseGame(self) :
        pygame.mixer.music.pause()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"   Game Paused !", True, (255, 255, 255))
        self.surface.blit(line1, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2-50))
        line2 = font.render("Press Space to Continue ", True, (255, 255, 255))
        self.surface.blit(line2, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 ))
        pygame.display.flip()


    def run(self):
        running = True
        isGamePause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_SPACE:
                        isGamePause = not isGamePause
                        if isGamePause:
                            self.pauseGame()

                    if not isGamePause:
                        if event.key == K_LEFT :
                            self.snake.moveLeft()

                        if event.key == K_RIGHT :
                            self.snake.moveRight()

                        if event.key == K_UP :
                            self.snake.moveUp()

                        if event.key == K_DOWN :
                            self.snake.moveDown()

                elif event.type == QUIT:
                    running = False
            try:
                if not isGamePause:
                    self.play()
                
            except Exception as e:
                self.gameOver()
                isGamePause = True
                self.restartGame()

            time.sleep(.22)

if __name__ == '__main__':
    game = Game()
    game.run()