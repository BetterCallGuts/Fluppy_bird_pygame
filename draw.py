import pygame as pg
import random
import obj
import os
import time
pg.mixer.init()


jump   =pg.mixer.Sound(os.path.join('sound', 'jump1.wav'))
jump_2 =pg.mixer.Sound(os.path.join('sound', 'jump_2.wav'))
jump_3 =pg.mixer.Sound(os.path.join('sound', 'jump_3.wav'))
jump_4 =pg.mixer.Sound(os.path.join('sound', 'jump_4.wav'))
jump_5 =pg.mixer.Sound(os.path.join('sound', 'jump_5.wav'))
jump_6 =pg.mixer.Sound(os.path.join('sound', 'jump_6.wav'))
mian_song =pg.mixer.Sound(os.path.join('sound', 'main.mp3'))
coin_1 =pg.mixer.Sound(os.path.join('sound', 'coin_1.wav'))
coin_2 =pg.mixer.Sound(os.path.join('sound', 'coin_3.wav'))
coin_3 =pg.mixer.Sound(os.path.join('sound', 'coin_2.wav'))
die_sound =pg.mixer.Sound(os.path.join('sound', 'die_sound.wav'))


restart_button = pg.image.load(os.path.join('images', 'buttons', 'restart.png'))
list_music = [jump, jump_2, jump_3, jump_4]
ground_music = [jump_5, jump_6] 
bg = pg.image.load("images/bg/bg.png")
bg_ground = pg.image.load("images/bg/ground.png")
bg_pipe = pg.image.load("images/bg/pipe.png")

white = (255, 255, 255)
def ground_move(ground_scroll , scroll_speed):
    ground_scroll -= scroll_speed
    if abs(ground_scroll) >35:
        return 0
    return ground_scroll
# bg = pg.image.load("images/bg/bg.png")
# def bird_ground(screen, bird_group):

def score_counter(pass_pipe, bird_group, pip_group, score):
        if len(pip_group) > 0 :
            if bird_group.sprites()[0].rect.left > pip_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pip_group.sprites()[0].rect.right\
            and not pass_pipe:
                pass_pipe = True
            if pass_pipe:
                    if bird_group.sprites()[0].rect.left > \
                        pip_group.sprites()[0].rect.right:
                        score += 1
                        # print(score)
                        pass_pipe = False
        return score

def draw_textre(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


score = 0
def draw(screen,bgDone,  groudnbgDone, ground_scroll,
        bird_group, pip_group, frequency ,last_pipe,
        game_run, flappy, time_now, in_touch, pass_pipe, score_):
    

    screen.blit(bgDone, (0,0))
    if flappy.flying:
        if time_now - last_pipe > frequency:
            y = random.randint(int(screen.get_height() /9),screen.get_height() - groudnbgDone.get_height() - 300)
            btm_pipe = obj.Pipe(screen.get_width(), y, 1)
            top_pipe = obj.Pipe(screen.get_width(), y , -1)
            pip_group.add(btm_pipe)
            pip_group.add(top_pipe)
            if len(pip_group) > 0 :
                if bird_group.sprites()[0].rect.left > pip_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pip_group.sprites()[0].rect.right\
                and not pass_pipe:
                    pass_pipe = True
                if pass_pipe:
                    
                    if bird_group.sprites()[0].rect.left > \
                        pip_group.sprites()[0].rect.right:
                        score_ += 1
                        print(score_)
                        pass_pipe = False
    
    
    
    bird_group.draw(screen)
    bird_group.update(screen, groudnbgDone, game_run, list_music)
    

    if pg.sprite.groupcollide(bird_group, pip_group, False, False):
        flappy.flying = False

        in_touch = True
        
    if not in_touch:
        pip_group.update(True)

    pip_group.draw(screen)

    screen.blit( groudnbgDone, (ground_scroll,screen.get_height()-groudnbgDone.get_height()))

    pg.display.update()

def time_(tn,lp, fq):
    if tn - lp >fq:
        lp = tn
    return lp