import pygame
import random
import os
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

WIDTH = 500
HEIGHT = 600

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The GODTONE Game")

clock = pygame.time.Clock()  # 時間管理操控

# Load images
background_img = pygame.image.load(os.path.join("img","background.jpg")).convert()
rock_img = pygame.image.load(os.path.join("img","rock2.jpg")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.jpg")).convert()
player_mini_image = pygame.transform.scale(player_img, (20,30))
player_mini_image.set_colorkey(WHITE)

pygame.display.set_icon(player_mini_image)

expl_anim = {}
expl_anim["lg"] = []
expl_anim["sm"] = []
expl_anim["player"] = []

for i in range(9):
    expl_img = pygame.image.load((os.path.join("img", f"player_expl{i}.png"))).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img, (75,75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img, (30, 30)))

    player_expl_img = pygame.image.load((os.path.join("img", f"expl{i}.png"))).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim["player"].append(player_expl_img)

poer_imgs = {}

brocolli = pygame.image.load(os.path.join("img","gun.png")).convert()
pork = pygame.image.load(os.path.join("img","shield.png")).convert()

poer_imgs["shield"] = brocolli
poer_imgs["gun"] = pork


shoot_sound = pygame.mixer.Sound(os.path.join("sound","AnyConv.com__shooting.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound","AnyConv.com__一爹.wav"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","AnyConv.com__expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","AnyConv.com__expl1.wav"))
]
shield_sound = pygame.mixer.Sound(os.path.join("sound","AnyConv.com__辰辰聲音.wav"))
ending_sound = pygame.mixer.Sound(os.path.join("sound", "AnyConv.com__ending_sound.wav"))

pygame.mixer.music.load(os.path.join("sound", "AnyConv.com__bgm.wav"))
pygame.mixer.music.set_volume(1.0)

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()  # 碰撞一次 就補上一顆
    all_sprites.add(r)  # 加進去
    rocks.add(r)  # 加回石頭群組 去跟子彈一起判斷

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y ,BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i
        img_rect.y = y

        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "CHALLENGE OF ASIAGODTONE ", 36, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Left or Right key to move; whitespace to shoot", 24, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press ENTER to start", 18, WIDTH / 2, HEIGHT*3/4)
    pygame.display.update()

    waiting = True
    while(waiting):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    return False

background_img = pygame.transform.scale(background_img,(500,600))
rock_img = pygame.transform.scale(rock_img,(random.randrange(60,100),random.randrange(60,100)))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(player_img,(60,50))
        self.image.set_colorkey(WHITE)
        self.radius = 20
        self.rect = self.image.get_rect()  #定位圖片 框起來 設定屬性
        self.rect.centerx = WIDTH/2  #在中央
        self.rect.bottom = HEIGHT-10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if  self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2  # 在中央
            self.rect.bottom = HEIGHT - 10

        key_pressed = pygame.key.get_pressed()  # return boolean of each key
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:

                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

            if self.gun >= 2 :
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)

                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2 , HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite): #內建類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image_ori = rock_img
        self.image_ori.set_colorkey(WHITE)
        self.image = self.image_ori.copy()

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85 / 2)
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(7,13)           #垂直速度
        self.speedx = random.randrange(-5, 5)

        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)

        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: #重新給予屬性
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(10, 20)  # 垂直速度
            self.speedx = random.randrange(-5, 5)

class Bullet(pygame.sprite.Sprite): #內建類別
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(bullet_img, (40, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = poer_imgs[self.type]
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    new_rock()

score = 0
pygame.mixer.music.play(-1)

show_init = True
running = True

# Game loop
while(running):
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(8):
            new_rock()

        score = 0

    clock.tick(FPS)  # 1 sec 最多被執行60次
     #get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update game
    all_sprites.update()  #執行群組裡面每個物件的update 函式
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # 兩個都消失
    for hit in hits:
        score += hit.radius
        expl = Explosion(hit.rect.center,"lg")
        all_sprites.add(expl)

        if random.random() > 0.8:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)

        new_rock()

    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) #撞到就刪掉
    for hit in hits:
        new_rock()
        player.health -= hit.radius

        if player.health <= 0:
            die = Explosion(player.rect.center, "player")
            all_sprites.add(die)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    hits = pygame.sprite.spritecollide(player, powers, True)  # 撞到就刪掉
    for hit in hits:
        if hit.type == "shield":
            ending_sound.play()
            player.health += 35
            if player.health > 100:
               player.health = 100

        if hit.type == "gun" :
            player.gunup()
            shield_sound.play()

    if player.lives == 0 and not(die.alive()):
        show_init = True

    #show image
    screen.fill(BLACK) #R G B
    screen.blit(background_img, (0,0))

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_image, WIDTH - 100, 15)
    pygame.display.update()

pygame.quit()