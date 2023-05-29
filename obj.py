import pygame as pg
import os
import random
pg.mixer.init()
pg.init()

class Obj:
    def __init__(self, screen, color, x, y, WIDTH, HEIGHT):
        rectdetails = (x,y,WIDTH, HEIGHT)
        self.rec = pg.draw.rect(screen, color, rectdetails)

class Bird(pg.sprite.Sprite):
    def __init__(self, x,y ):
        pg.sprite.Sprite.__init__(self)
        
        
        self.images = []
        self.index = 0
        self.count = 0
        for num in range(1,4):
            image = pg.image.load(f'images/bird_frames/bird{num}.png')
            self.images.append(image)
        self.image = self.images[self.index ]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.press = False
        self.flying = False

    def update(self,screen, bggroundDone, game_run, list_music, ground_music):
        keys = pg.key.get_pressed()
        
        
        if self.flying:
            self.vel += .5
            
            if self.vel > 8:
                self.vel = 8
            if self.rect.y + self.image.get_height()+ bggroundDone.get_height()  < screen.get_height() or self.vel <0:
                self.rect.y += int(self.vel)
    
        #Jump
        if keys[pg.K_x] and not self.flying  and not game_run:
            self.flying = True
            game_run = True
        if keys[pg.K_x] and self.rect.y >int( screen.get_height() / 9) and self.press == False:
            self.press = True
            self.vel = -10
            x = random.choice(list_music)
            x.play()
        if not keys[pg.K_x]:
            self.press = False

        #animation handle   
        flap_cooldown = 10
        self.count +=1
        if self.count > flap_cooldown:
            self.count = 0
            self.index+=1
        if self.index >= len(self.images) :
            self.index =0
        self.image = self.images[self.index]

        #rotate bird
        
        self.image =  pg.transform.rotate(self.images[self.index],self.vel * -3)
        if self.vel == 8 :
            if  self.rect.y + self.image.get_height()+ bggroundDone.get_height()  > screen.get_height() -10:
                self.vel *= -1
                y = random.choice(ground_music)
                y.play()

            else:
                self.image = pg.transform.rotate(self.images[self.index], -44)
        # return game_run


class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, position):
        pg.sprite.Sprite.__init__(self)
        self.image  = pg.image.load("images/bg/pipe.png")
        self.rect = self.image.get_rect()
        self.pip_gap = 200
        
        if position ==1:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(self.pip_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y+ int(self.pip_gap/2)]
        self.scroll_speed = 5
        self.frequency = 1500  #millisecound
        self.last_pipe = pg.time.get_ticks()

    def update(self , winnig):
        if winnig:
            self.rect.x -= self.scroll_speed
        

class Button():
    def __init__(self,x,y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def draw(self, screen):
        action = False
        pos = pg.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                action = True
        
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
    

class Coin(pg.sprite.Sprite):
    def __init__(self,  x,y ):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/gamplay/coin.png')
        self.image = pg.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.rect.topright = [x, y]
    
    def update(self):
        # screen.blit(self.image, (self.rect.x,self.rect.y))
        self.rect.x -= 5


class Fire(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.images_bg = []
        self.images = []
        
        self.index = 0
        self.count = 0
        self.scale = 700
        self.s = 0
        for num in range(1,92):
            image = pg.image.load(f'images/green/frame_{num}s.gif')
            
            self.images_bg.append(image)
        for i in self.images_bg:
            image = pg.transform.scale(i, (self.scale,self.scale))
            self.images.append(image)
            self.scale -= 4
        self.image = self.images[self.index ]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    
    def update(self):
        x = False
        # if self.s ==91 :
        #     self.s =0
        self.count +=1
        flap_cooldown = 2
        if self.count > flap_cooldown:
            self.count = 0
            self.index+=1
            self.rect.y +=2
            self.rect.x +=2
        if self.index >= len(self.images) :
            self.index =0
            x  = True
            self.kill()
        self.image = self.images[self.index]

        return x