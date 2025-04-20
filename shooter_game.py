from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-15/2, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    life = 2
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0
        if self.life == 0:
            self.kill()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

width = 700
height = 500
display.set_caption("SHOOTER")
window = display.set_mode((width, height))
background = transform.scale(image.load("galaxy.jpg"), (width, height))

player = Player('rocket.png', width / 2 - 30, height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(80, width - 80), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

lost_sound = mixer.Sound('kick.ogg')
win_sound = mixer.Sound('money.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

game = True
finish = False
clock = time.Clock()
FPS = 60

score = 0
lost = 0
max_score = 100
max_lost = 3

num_fire = 0
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_sound.play()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        if lost >= max_lost:
            finish = True
            window.blit(lose, (width / 2 - 150, height / 2 - 50))
            lost_sound.play()

        if score >= max_score:
            finish = True
            window.blit(win, (width / 2 - 150, height / 2 - 50))
            win_sound.play()

        text_score = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        text_lost = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255)) 
        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 660))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        collides = sprite.groupcollide(asteroids, bullets, False, True)
        for c in collides:
            c.life -= 1
            if len(asteroids) < 3:
                asteroid = Asteroid('asteroid.png', randint(80, width - 80), -40, 80, 50, randint(1,7))
                asteroids.add(asteroid)
                
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (width / 2 - 150, height / 2 - 50))
            lost_sound.play()
        
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        rel_time = 0
        rel_time = False
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(5000)
        player = Player('rocket.png', width / 2 - 30, height - 100, 80, 100, 10)

        monsters = sprite.Group()
        for i in range(5):
            monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        
        asteroids = sprite.Group()
        for i in range(3):
            asteroid = Asteroid('asteroid.png', randint(80, width - 80), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)
    
    display.update()
    clock.tick(FPS)