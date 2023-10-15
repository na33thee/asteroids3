from pygame import *
from random import *

w, h = 700, 500
window = display.set_mode((w, h))

clock = time.Clock()

game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY
        self.sizeX = sizeX
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= w-self.sizeX:
            self.rect.x += self.speed        
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 30, 15)
        bullets.add(bullet)

ship = Player("rocket.png", 10, h-100, 65, 95, 8)
background = transform.scale(image.load("galaxy.jpg"), (w, h))

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global hearts
        if self.rect.y >= h:
            try:
                #hearts.pop(len(hearts)-1)
                hearts.pop(0)
            except:
                pass
            self.rect.y = 0
            self.rect.x = randint(0, w-self.sizeX)
            lost += 1

asteroids = sprite.Group()
for i in range(6):
    randpic = randint(1,2)
    if randpic == 1:
        pic = "asteroid.png"
    if randpic == 2:
        pic = "ufo.png"
    asteroid = Enemy(pic, randint(0, w-50), -40, 50, 50, randint(1,2))
    asteroids.add(asteroid)  

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
bullets = sprite.Group()
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.15)

font.init()
mainfont = font.Font("HFHourglass.ttf", 40)
r,g,b = 0,0,0
score = 0

from time import time as timer
num_fire = 0
reload_time = False

hearts = []
lives = 10
heart_X = 300
for i in range(lives):
    heart = GameSprite("heart.png", heart_X, 10, 40, 35, 0)
    hearts.append(heart)
    heart_X += 35


restart = GameSprite("restart.png", 240, 200, 222, 125, 0)
start = GameSprite("start.png", 240, 200, 222, 125, 0)
exit = GameSprite("exit.png", 5, 5, 50, 50, 0)
finish = True


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        #
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 10 and reload_time == False:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 10 and reload_time == False:
                    reload_time = True
                    reload_start = timer()
            if e.key == K_r:
                for a in asteroids:
                    a.rect.x = randint(0, 600)
                    a.rect.y = -100
                finish, lost, score = 0,0,0
                hearts = []
                lives = 10
                heart_X = 300
                for i in range(lives):
                    heart = GameSprite("heart.png", heart_X, 10, 40, 35, 0)
                    hearts.append(heart)
                    heart_X += 35
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x,y = e.pos
            if restart.rect.collidepoint(x,y):
                for a in asteroids:
                    a.rect.x = randint(0, 600)
                    a.rect.y = -100
                finish, lost, score = 0,0,0
                hearts = []
                lives = 10
                heart_X = 300
                for i in range(lives):
                    heart = GameSprite("heart.png", heart_X, 10, 40, 35, 0)
                    hearts.append(heart)
                    heart_X += 35
            if start.rect.collidepoint(x,y):
                finish = False
            if exit.rect.collidepoint(x,y):
                game = False

    if finish:
        window.blit(background, (0,0))
        start.draw()
        exit.draw()
    
    if not finish:
        window.blit(background, (0,0))
        score_text = mainfont.render("Killed: "+str(score), True, (255,255,255))
        lose_text = mainfont.render("Missed: "+str(lost), True, (255,255,255))
        window.blit(score_text, (5,10))
        window.blit(lose_text, (5,50))
        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()
        
        collides = sprite.groupcollide(bullets, asteroids, True, True)
        for c in collides:
            score += 1 
            pics = ["ufo.png", "asteroid.png"]
            asteroid = Enemy(pics[randint(0,1)], randint(0, w-50), -40, 50, 50, randint(1,2))
            asteroids.add(asteroid)  
        
        if sprite.spritecollide(ship, asteroids, False):
            restart.draw()
            lose = mainfont.render("YOU LOSE", True, (255,255,255))
            window.blit(lose, (220, 220))
            finish = True
        
        if reload_time:
            now_time = timer()
            if now_time - reload_start < 3:
                reloading = mainfont.render("RELOADING...", True, (0,255,0))
                window.blit(reloading, (200, 200))
            else:
                num_fire = 0
                reload_time = False
            
        for heart in hearts:
            heart.draw()

        if len(hearts) <= 0:
            restart.draw()
            lose = mainfont.render("YOU LOSE", True, (255,255,255))
            window.blit(lose, (220, 220))
            finish = True

        ship.draw()
        ship.update()
    display.update()
    clock.tick(144)