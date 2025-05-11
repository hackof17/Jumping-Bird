import pygame, sys
from pygame.locals import *
WIDTH, HIGH = 800, 640
#          R   G   B
RED =    (255,  0,  0)
WHITE =  (255,255,255)
BLACK =  (  0,  0,  0)
YELLOW = (255,255,  0)
BLUE =   (  0,  0,255)

class Hero:
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bird.jpg")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x = int(WIDTH/4)
        self.y = int(3*HIGH/4)
        self.v = 0
        self.a = 1
        self.radius = 15
    def update(self):
        self.y -= self.v
        self.v = self.v - self.a if self.v > -7 else -7
        if self.y >= HIGH + self.radius:
            self.y = HIGH + self.radius
    # def show(self):
    #     pygame.draw.circle(DISPLAYSURF, RED, (self.x, self.y), self.radius)
    #     # pygame.draw.line(DISPLAYSURF, YELLOW, (0, self.end + self.radius), (WIDTH, self.end + self.radius), 2)
    #     pygame.time.wait(50)
    def trigger(self):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.v = 3
            self.y -= self.v
    def move(self):
        self.trigger()
        self.update()
        self.rect.x, self.rect.y = self.x, self.y
        # self.show()

def main():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HIGH))
    pygame.display.set_caption("Jump Bull")
    fpsClock = pygame.time.Clock()
    FPS = 80
    hero = Hero()
    while True:
        DISPLAYSURF.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        hero.move()
        fpsClock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()