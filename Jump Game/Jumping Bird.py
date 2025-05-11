import pygame, random, sys
from pygame.locals import *

#             R   G   B
RED       = (255,  0,  0)
WHITE     = (255,255,255)
BLACK     = (  0,  0,  0)
YELLOW    = (255,255,  0)
BLUE      = (  0,  0,255)
WOODCOLOR = (222,184,135)

WOODWIDTH = 80
WOODMEIGEN = 160
WIDTH = (WOODMEIGEN+WOODWIDTH)*5
HIGH = 700
target = int(WIDTH/3)
background = pygame.image.load("back.png")
background = pygame.transform.scale(background, (WIDTH, HIGH))
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bird.jpg")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.x = int(WIDTH/4)
        self.y = int(3*HIGH/4)
        self.v = 0
        self.a = 1
        self.radius = 15
    def move(self):
        self.y -= self.v
        self.v = self.v - self.a if self.v > -7 else -7
        if self.y >= HIGH + self.radius:
            self.y = HIGH + self.radius
    def trigger(self):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.v = 3
            self.y -= self.v
    def update(self):
        self.trigger()
        self.move()
        self.rect.x, self.rect.y = self.x, self.y

class Wood(pygame.sprite.Sprite):
    step = 1
    def __init__(self, x):
        super().__init__()
        self.score = 1
        split = random.random()
        while not (0.1 <= split <= 1-0.1-0.4):
            split = random.random()
        self.high1 = int(HIGH*split)
        self.high2 = int(HIGH*(1-split-0.4))

        self.image1 = pygame.Surface((WOODWIDTH, self.high1))
        self.image1.fill(WOODCOLOR)
        self.rect1 = self.image1.get_rect()
        self.rect1.topleft = (x, 0)

        self.image2 = pygame.Surface((WOODWIDTH, self.high2))
        self.image2.fill(WOODCOLOR)
        self.rect2 = self.image2.get_rect()
        self.rect2.bottomleft = (x, HIGH)

    def update(self):
        global score, group
        self.rect1.x -= Wood.step
        self.rect2.x = self.rect1.x
        if self.rect1.right < target and self.score:
            score += 1
            self.score = 0
        if self.rect1.left <= 0:
            last_wood = max(group, key= lambda wood:wood.rect1.right)
            new_x = last_wood.rect1.right + WOODMEIGEN
            new_wood = Wood(new_x)
            group.add(new_wood)
        if self.rect1.right < 0:
            self.kill()


class Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image1, sprite.rect1)
            surface.blit(sprite.image2, sprite.rect2)

def main():
    global DISPLAYSURF, fpsClock, FPS, score
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HIGH))
    pygame.display.set_caption('Jumping Bird')
    fpsClock = pygame.time.Clock()
    FPS = 80
    while True:
        score = 0
        RunGame()
        Pause()

def RunGame():
    global group
    hero = Hero()
    hero.x = target
    group = Group()
    for i in range(5):
        wood = Wood(WIDTH + i*(WOODMEIGEN+WOODWIDTH))
        group.add(wood)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        group.update()
        hero.update()
        test = CollisionTest(hero, group)
        if test:
            return
        DISPLAYSURF.blit(background, (0,0))
        group.draw(DISPLAYSURF)
        DISPLAYSURF.blit(hero.image, (hero.x, hero.y))
        WriteScore(score)
        fpsClock.tick(FPS)
        pygame.display.update()

def Pause():
    text = "碰撞发生"
    font = pygame.font.SysFont('楷体gb2312', 200)
    surface = font.render(text, True, BLACK)
    rect = surface.get_rect()
    rect.center = int(WIDTH/2), int(HIGH/2)
    DISPLAYSURF.blit(surface, rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        key = pygame.key.get_pressed()
        if key[K_SPACE]:
            return

def WriteScore(score):
    font = pygame.font.SysFont('楷体gb2312', 50)
    text = f'得分: {score}'
    surface = font.render(text, True, BLACK)
    rect = surface.get_rect()
    rect.topright = WIDTH, 0
    DISPLAYSURF.blit(surface, rect)

def CollisionTest(hero:Hero, wood_group:Group):
    for sprite in wood_group.sprites():
        test1 = hero.rect.colliderect(sprite.rect1)
        test2 = hero.rect.colliderect(sprite.rect2)
        if test1 or test2:
            return True
    return False

if __name__ == "__main__":
    main()