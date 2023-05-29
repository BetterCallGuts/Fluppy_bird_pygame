import pygame as pg
import sys
import draw
import pygame.locals
import obj
import random
import os
# from draw import white
class Game:
    def __init__(self, FPS, WIDTH, HEIGHT, Caption = "game"):
        pg.init()
        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.Caption = Caption
        pg.display.set_caption(self.Caption)
        draw.mian_song.play()
    def run(self, score=0 , highst_score = 0 , coin_counter = 0):
        fontpixel = os.path.join('Font', 'Grand9K Pixel.ttf')
        bgDone = pg.transform.scale(draw.bg,(self.screen.get_width(), self.screen.get_height()))
        groudnbgDone = pg.transform.scale(draw.bg_ground,((self.screen.get_width()+40,100) ))
        ground_scroll = 0
        scroll_speed = 5
        game_run = False
        # groudnbgDone.
        run = True
        pass_pipe = False
        k = obj.Pipe(3,3,3)
        bird_group = obj.pg.sprite.Group()
        pip_group  = obj.pg.sprite.Group()
        coin_group = obj.pg.sprite.Group()
        fire_red_group=obj.pg.sprite.Group()
        
        
        
        
        coin_counter_img = pg.transform.scale(
        pg.image.load('images/gamplay/coin.png'), (40,40))
        coin_rect = coin_counter_img.get_rect()
        coin_rect.topright = (self.screen.get_width() - 100,20)
        


        flappy = obj.Bird(int(self.screen.get_width()/6) , int(self.screen.get_height()/2))
        in_touch = False
        
        # print(btm_pipe.rect.bottomleft)
        
        bird_group.add(flappy)
        die = False
        # x = pg.font.get_fonts([fontpixel])
        font = pg.font.Font(fontpixel, 50)
        coin_music = [draw.coin_1, draw.coin_2, draw.coin_3]
        button_restart = obj.Button(int(self.screen.get_width() /2)-50, int(self.screen.get_height()/2 )-50, draw.restart_button)
        
        one = True
        # flappy.f

        while run:
            self.clock.tick(self.FPS)
            
            self.screen.blit(bgDone, (0,0))
            fire_red_group.draw(self.screen)
            pip_group.draw(self.screen)
            bird_group.draw(self.screen)
            bird_group.update(self.screen, groudnbgDone, game_run, draw.list_music, draw.ground_music)
            coin_group.draw(self.screen)
            if len(pip_group) > 0 :
                if bird_group.sprites()[0].rect.left > pip_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pip_group.sprites()[0].rect.right\
                and not pass_pipe:
                    pass_pipe = True
                if pass_pipe:
                    if bird_group.sprites()[0].rect.left > pip_group.sprites()[0].rect.right:
                        pass_pipe = False
                        score += 1
                        
                        # print(score)
            draw.draw_textre(self.screen,f"Score : {str(score)}",font, draw.white, int(self.screen.get_width() / 2) - 100, 0)
            if score > highst_score:
                highst_score = score
            draw.draw_textre(self.screen, f"HS: {str(highst_score)}",font, draw.white, 5, 0)
            draw.draw_textre(self.screen, f"{str(coin_counter)}",font, draw.white, self.screen.get_width() - 70, 0)

            if len(pip_group) > 0:
                if pip_group.sprites()[0].rect.right <0:
                    pip_group.sprites()[0].kill()
    

            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    run = False
                    pg.quit
                    sys.exit()


            time_now = pg.time.get_ticks()

            if flappy.flying:

                if time_now - k.last_pipe > k.frequency:
                    y = random.randint(int(self.screen.get_height() /9),self.screen.get_height() - groudnbgDone.get_height() - 300)
                    btm_pipe = obj.Pipe(self.screen.get_width(), y, 1)
                    top_pipe = obj.Pipe(self.screen.get_width(), y , -1)
                    coin     = obj.Coin(self.screen.get_width() + int(top_pipe.image.get_width()-15),y )
                    pip_group.add(btm_pipe)
                    pip_group.add(top_pipe)
                    coin_group.add(coin)
                    


            self.screen.blit( groudnbgDone, (ground_scroll, self.screen.get_height()-groudnbgDone.get_height()))
            if len(coin_group) > 0:
                if coin_group.sprites()[0].rect.right <30:
                    coin_group.sprites()[0].kill()
                    
            if pg.sprite.groupcollide(bird_group, coin_group, False, False):
                d = random.choice(coin_music)
                d.play()
                coin_group.sprites()[0].kill()
                coin_counter += 1

            if pg.sprite.groupcollide(bird_group, pip_group, False, False):
                flappy.flying = False
                if not die:
                    draw.die_sound.play()
                    die = True

                in_touch = True
                if button_restart.draw(self.screen):
                    self.run(highst_score=highst_score, coin_counter=coin_counter)

            if not in_touch:
                pip_group.update(True)
                coin_group.update()
            
            k.last_pipe =draw.time_(time_now,k.last_pipe, k.frequency)


            if flappy.flying:
                # draw.mian_song.play()
                ground_scroll = draw.ground_move(ground_scroll, scroll_speed)

            self.screen.blit(coin_counter_img, (coin_rect))

            pg.display.update()


if __name__ == "__main__":
    game = Game(60, 0,0,"fluppybird")
    game.run()