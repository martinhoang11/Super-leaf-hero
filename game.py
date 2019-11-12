import pyglet
import time
from math import sin,cos
from random import *


window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()
pyglet.media.sources.loader._have_ffmpeg = False

background_group = pyglet.graphics.OrderedGroup(0)
foreground_group = pyglet.graphics.OrderedGroup(1)
#may_sprite
cloud = pyglet.image.load("Unknown.png")

#player sprite
player = pyglet.image.load_animation("player.gif")
player_sprite = pyglet.sprite.Sprite(player, x=15,y=35,batch=batch,group=foreground_group)

#star_boss_sprite
star_boss = pyglet.image.load_animation('spoA2.gif_c200')
star_boss_sprite = pyglet.sprite.Sprite(star_boss, x=780, y = 50,batch=batch, group=foreground_group)
star_boss_miss = pyglet.image.load_animation('boss.gif')
star_boss_miss_sprite = pyglet.sprite.Sprite(
    star_boss_miss, x=720, y = 0,batch=None)

#la_sprite
la = pyglet.image.load("la.png")
la_sprite = pyglet.sprite.Sprite(
    la,player_sprite.x +100,player_sprite.y + 30,batch=None,group=foreground_group)
la_sprite.scale = 0.1

#bongbong_spirte
bongbong = pyglet.image.load('bongbong.png')
bongbong_spirte = pyglet.sprite.Sprite(
    bongbong, star_boss_sprite.x, star_boss_sprite.y + 10, batch=batch,group=foreground_group)

#boss_hp_sprite
boss_hp_empty = pyglet.image.load('empty.png')
boss_hp_half_half = pyglet.image.load('half-hlaf.png')
boss_hp_half = pyglet.image.load('half.png')
boss_hp_full = pyglet.image.load('full.png')
boss_hp_sprite = [pyglet.sprite.Sprite(boss_hp_full, x=800, y=730 , batch=batch,group=foreground_group),
                    pyglet.sprite.Sprite(boss_hp_half, x=800, y=730 , batch=None,group=foreground_group),
                    pyglet.sprite.Sprite(boss_hp_half_half, x=800, y=730 , batch=None,group=foreground_group),
                    pyglet.sprite.Sprite(boss_hp_empty, x=800, y=730 , batch=None,group=foreground_group)]
for i in boss_hp_sprite:
    i.scale = 0.6

#player_hp_sprite
player_hp = pyglet.image.load_animation('heart.gif')
player_hp_sprite = [pyglet.sprite.Sprite(player_hp, x=10, y=730 , batch=batch,group=foreground_group),
                    pyglet.sprite.Sprite(player_hp, x=50, y=730 , batch=batch,group=foreground_group),
                    pyglet.sprite.Sprite(player_hp, x=90, y=730 , batch=batch,group=foreground_group),
                    pyglet.sprite.Sprite(player_hp, x=130, y=730 , batch=batch,group=foreground_group),
                    pyglet.sprite.Sprite(player_hp, x=170, y=730 , batch=batch,group=foreground_group),]
for i in player_hp_sprite:
    i.scale = 0.15
player_sprite.scale = 0.1

#background Sprite
bground = pyglet.image.load_animation("background.gif")
bground_sprite = pyglet.sprite.Sprite(bground,batch=batch,group=background_group)
bground_sprite.scale = 2.99

#gloal variables
ban_la = False
ban_boss_miss = False
jump = False
player_hp = 5
boss_hp = 12
move_forward = True
move_back = False
arr = 4
arr_boss_hp = 1
end_game = False
timecount = 0

#label
label_boss = pyglet.text.Label(
    "HP: ", font_size=15, y=740, x=750, batch=batch,group=foreground_group)
label_boss_hp = pyglet.text.Label(
    "1", font_size=15,y=750, x=950, batch=None)
label_end_game = pyglet.text.Label(
    "You win !!!", font_size=20, y=400, x=400, batch=None,group=foreground_group)
label_lose_game = pyglet.text.Label(
    "You Lose !!!", font_size=20, y=400, x=400, batch=None,group=foreground_group)

#video
videopath = "ending_video.mp4"
source = pyglet.media.StreamingSource()
videoload = pyglet.media.load(videopath)
player = pyglet.media.Player()
player.queue(videoload)

#draw ground
img1 = pyglet.image.load("ground-clipart-1.jpg")
background_sprite = [pyglet.sprite.Sprite(img1,batch=batch,group=foreground_group),
                     pyglet.sprite.Sprite(img1, x=450,batch=batch,group=foreground_group),
                     pyglet.sprite.Sprite(img1, x=850,batch=batch,group=foreground_group),
                     pyglet.sprite.Sprite(img1, x=1250,batch=batch,group=foreground_group)]
for i in background_sprite:
    i.scale = 0.05
w = img1.width

#draw cloud
cloud_sprite = [pyglet.sprite.Sprite(cloud,x=600, y=650, batch=batch,group=foreground_group),
                pyglet.sprite.Sprite(cloud,x=800, y=490, batch=batch,group=foreground_group),
                     pyglet.sprite.Sprite(cloud, x=1200, y=525,batch=batch,group=foreground_group),
                     pyglet.sprite.Sprite(cloud, x=1000,y=590,batch=batch,group=foreground_group),
                     pyglet.sprite.Sprite(cloud, x=1450,y=580,batch=batch,group=foreground_group)]
for i in cloud_sprite:
    i.scale = 0.1


@window.event
def on_draw():
    global timecount
    global arr_boss_hp
    global boss_hp
    window.clear()
    batch.draw()
    for i in range(10):
        x = randint(0,800)
        y = randint(0,600)
        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                ('v2i', (x, y)),
                ('c3B', (255, 255, 255)))
    timecount +=1
    if boss_hp == 8:
        boss_hp_sprite[0].batch = None
        boss_hp_sprite[1].batch = batch
    elif boss_hp == 4:
        boss_hp_sprite[1].batch = None
        boss_hp_sprite[2].batch = batch
    elif boss_hp == 0:
        boss_hp_sprite[2].batch = None
        boss_hp_sprite[3].batch = batch
    if boss_hp == 0:
        window.clear()
        window.switch_to()
        window.dispatch_events()
        player.play()
        player.get_texture().blit(-50,50)
#dieu khien nvat
@window.event
def on_key_press(key, modifiers):
    global jump
    global jump_status
    global ban_la
    if key == pyglet.window.key.UP and not jump:
        jump = True
        jump_status = "up"
    elif key == pyglet.window.key.LEFT:
        if player_sprite.x > 50:
            player_sprite.x-=50
    elif key == pyglet.window.key.RIGHT:
        player_sprite.x+=50
    elif key == pyglet.window.key.SPACE:
        la_sprite.batch = batch
        la_sprite.x = player_sprite.x + 100
        la_sprite.y = player_sprite.y + 30
        ban_la = True

def game_loop(_):
    global jump
    global jump_status
    global ban_la
    global move_forward
    global move_back
    global arr
    global arr_boss_hp
    global end_game
    global timecount
    global boss_hp

    #draw background
    for i in range(len(background_sprite)):
        background_sprite[i].x -= 7
        if background_sprite[i].x < -500:
            background_sprite[i].x = 1000

    #loop cloud
    for i in range(len(cloud_sprite)):
        cloud_sprite[i].x -= 3
        if cloud_sprite[i].x < -200:
            cloud_sprite[i].x = 1000

    #loop boss ban bong bong
    for i in range(500):
        if end_game == False:
            if 800 <= timecount <= 1400:
                bongbong_spirte.x -= 0.0096
                bongbong_spirte.y -= sin(bongbong_spirte.x)
            elif 1700 <= timecount <= 2200:
                bongbong_spirte.x -= 0.0125
                bongbong_spirte.y -= sin(bongbong_spirte.x)
            elif 2500 <= timecount <= 3200:
                bongbong_spirte.x -= 0.027
                bongbong_spirte.y -= sin(bongbong_spirte.x)
            else:
                bongbong_spirte.x -= 0.025
                bongbong_spirte.y -= sin(bongbong_spirte.x)
            if bongbong_spirte.x < -300:
                bongbong_spirte.x = star_boss_sprite.x
            if bongbong_spirte.y < 30:
                bongbong_spirte.y = 90
            if bongbong_spirte.y > 200:
                bongbong_spirte.y = 90

    #loop for boss move
    for i in range(1000):
        if star_boss_sprite.x > 601 and move_forward:
            star_boss_sprite.x -= 0.004
        if star_boss_sprite.x <= 601:
            move_forward = False
            move_back = True
        if star_boss_sprite.x < 800 and move_back:
            star_boss_sprite.x += 0.004
        if star_boss_sprite.x >= 800 :
            move_forward = True
            move_back = False



    #nhan vat jump
    if jump:
        if jump_status == "up":
            player_sprite.y += 50
        if jump_status == "down":
            player_sprite.y -= 8
        if player_sprite.y > 200:
            jump_status = "down"
        if player_sprite.y <= 35:
            jump = False

    #shoot la
    if ban_la and end_game == False:
        for i in range(3):
            la_sprite.x += 3
            if star_boss_sprite.x - 1 <= la_sprite.x <= \
                    star_boss_sprite.x + 1\
                    and star_boss_sprite.y - 100 <= la_sprite.y \
                        <= star_boss_sprite.y + 100:
                boss_hp -= 1
                la_sprite.batch = None

    #Tru live nhan vat
    if player_sprite.x -5 <= bongbong_spirte.x <= player_sprite.x + 5 \
            and player_sprite.y -30 <= bongbong_spirte.y <= \
            player_sprite.y + 30:
        player_hp_sprite[arr].batch = None
        arr -= 1

    #Player lose
    if arr == -1:
        end_game = True
        player_sprite.batch = None
        la_sprite.batch = None
        star_boss_sprite.batch = None
        bongbong_spirte.batch = None
        label_boss_hp.batch = None
        label_boss.batch = None
        label_lose_game.batch = batch
        arr = 1

    #Boss win
    # if arr_boss_hp == 3:
    #     end_game = True
    #     player_sprite.batch = None
    #     la_sprite.batch = None
    #     star_boss_sprite.batch = None
    #     bongbong_spirte.batch = None
    #     label_boss_hp.batch = None
    #     label_boss.batch = None
    #     label_end_game.batch = batch

pyglet.clock.schedule(game_loop)
pyglet.app.run()
