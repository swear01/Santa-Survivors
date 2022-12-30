import pygame
from pygame.locals import * # CONSTS
from math import cos, sin, pi, dist, inf, atan
from numpy import array
from numpy.linalg import norm
from .enemy import Enemy
from main import width


class Weapon:
    def __init__(self, name, player, 
        atk=10, reload=1, b_speed=70, b_hp=1,b_amt=1):
        self.name = name
        self.player = player
        self.cooldown = reload
        self.reload = reload
        self.atk = atk
        self.b_speed = b_speed
        self.b_hp = b_hp
        self.b_amt = b_amt


    def shoot(self, pos, enemies):
        if self.name == 'test':
            bullets = pygame.sprite.Group()
            for i in range(self.b_amt):
                angle = 2*i*pi/self.b_amt
                vec = (self.b_speed*cos(angle),self.b_speed*sin(angle))
                bullets.add(Bullet(pos, vec, self.player, color='#0000ff', hp=self.b_hp, atk=self.atk, kind='normal'))
            return bullets

        if self.name == 'autoaim':
            nearest_enemy = Enemy.nearest_enemy(pos, enemies)
            vec = nearest_enemy.pos-self.player.pos
            vec *= self.b_speed/norm(vec)
            return Bullet(pos, vec, self.player, color='#ff00ff', hp=self.b_hp, atk=self.atk, kind='autoaim')
 
BULLET_MAX_DIST = 400           

class Bullet(pygame.sprite.Sprite, Weapon):
    def __init__(self, pos, vec, player, color,
        hp, atk, kind):
        super().__init__()
        self.image = pygame.Surface([8,8])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.player = player
        self.pos = array(pos, dtype='float64')
        self.vec = array(vec, dtype='float64') 
        self.kind = kind
        
        self.hp = hp # hp is how many enemies can the bullet hit
        self.atk = atk

    def update(self, dt):
        if dist(self.pos, self.player.pos) > 300 :
            self.kill()
            return
        if self.hp == 0 : 
            self.kill()
            return
        self.pos += self.vec*dt
        self.rect.center = self.pos

# 鹿角(麋鹿的起始武器)
# 防禦型武器，怪物碰到鹿角那一面會扣血，其餘部分扣玩家血
# 升級後鹿角會變大、攻擊力變強
class DeerAntler(pygame.sprite.Sprite):
    def __init__(self, player, enemies, color, level):
        super().__init__()
        self.level = level
        h = 52.5  # h 為鹿的圖片高 * 1.5
        self.image = pygame.Surface([20, h * (3/4 + level/4)]) # 升級
        self.image.fill(color) # 要以陰影或虛線標示攻擊範圍
        self.rect = self.image.get_rect()
        self.player = player
        if self.player.drct == 'left':
            self.pos = self.player.rect.left
        if self.player.drct == 'right':
            self.pos = self.player.rect.right
        basic_atk = 10
        self.atk = int(basic_atk * (1/2 + level/2)) #  升級
        self.hp = inf # hp is how many enemies can the bullet hit
        self.enemies = enemies

    def update(self, dt):
        if self.player.direction == 'left':
            self.pos = self.player.rect.left
        if self.player.direction == 'right':
            self.pos = self.player.rect.right
        self.rect.center = self.pos

    def shoot(self):
        bullets = pygame.sprite.Group()
        bullets.add(DeerAntler(self.player, self.enemies, color='#0000ff', level = 1))

# 雪橇(聖誕老人的起始武器)
# 從玩家的下方，由左而右水平開過去，到螢幕邊界會重新從左邊開進去
# 升級後雪橇速度變快、變大台、攻擊力變強
# 升級後可以開兩台的有空再補，有一點點麻煩
class Sled(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level):
        super().__init__()
        self.level = level
        self.h = 40  # h 為雪橇圖片高
        self.image = pygame.Surface([40, self.h * (3/4 + level/4)]) # 升級
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.topright = (0, self.player.pos[1]-self.h/2)
        basic_vec = 20
        self.vec = basic_vec * (1/2 + level/2) # 升級
        basic_atk = 10
        self.atk = basic_atk * (1/2 + level/2) # 升級
        self.hp = inf  # hp is how many enemies can the bullet hit
        self.enemies = enemies

    def update(self, dt):
        self.x += self.vec * dt
        if self.left >= width:
            self.rect.topright = (0, self.player.pos[1]-self.h/2)

    def shoot(self):
        bullets = pygame.sprite.Group()
        bullets.add(Sled(self.player, self.enemies, color='0000ff', level = 1))

# 鏟子(花園小精靈的起始武器)
# 會瞄準離玩家最近的敵人
# 傷害力較高，但只有鏟子頭有攻擊功能
# 升級後鏟子頭變大、攻擊力增加
class Shovel(pygame.sprite.Sprite):
    def __init__(self, player, color, level, enemies):
        super().__init__()
        self.level = level
        self.h = 10
        self.angle = atan((self.player.pos[1] - self.nearest_enemy.pos[1])/(self.player.pos[0] - self.nearest_enemy.pos[0]))
        self.image = pygame.Surface([self.h * (3/4 + level/4), self.h * (3/4 + level/4)]) # 升級
        # self.image是放鏟子頭，也就是真的可以攻擊的區域
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.nearest_enemy = Enemy.nearest_enemy(self.player.pos, enemies)
        self.rect.pos = (self.player.pos[0] - 25 * cos(self.angle), self.player.pos[1] - 25 * sin(self.angle))
        # 鏟子長 = 30，扣掉頭剩20的柄，因為是中心所以+5

        self.image_show_ori = pygame.Surface([10, 30]) # self.image是放鏟子圖片的地方
        self.image_show_ori.fill(color)
        self.image_show_ori.rect = self.image_show_ori.get_rect()
        self.image_show_ori.rect.bottom = self.player.pos
        self.image_show = self.image_show_ori.copy()
        self.image_show = pygame.transform.rotate(self.image_show_ori, self.angle)

        self.player = player
        self.hp = inf  # hp is how many enemies can the bullet hit
        basic_atk = 30
        self.atk = basic_atk * level # 升級

    def update(self, dt):
        self.rect.pos = (self.player.pos[0] - 25 * cos(self.angle), self.player.pos[1] - 25 * sin(self.angle))
        self.rect.center = self.rect.pos

        self.image_show = pygame.transform.rotate(self.image_show_ori, self.angle)       

    def shoot(self):
        bullets = pygame.sprite.Group()
        bullets.add(Shovel(self.player, self.enemies, color='0000ff', level = 1))

# 雪橇犬
# 會去找離自己最近的敵人攻擊
# 離玩家太遠(DOG_MAX_DIST = 200)會跑回玩家身邊，再出發去尋找敵人
# 升級後跑比較快、攻擊力增加
DOG_MAX_DIST = 200
class SledDog(pygame.sprite.Sprite):
    def __init__(self, player, color, level, enemies):
        super().__init__()
        self.level = level
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = self.rect.center
        self.nearest_enemy = Enemy.nearest_enemy(self.pos, enemies)
        self.angle = atan((self.pos[1] - self.nearest_enemy.pos[1])/(self.pos[0] - self.nearest_enemy.pos[0]))

        self.player = player
        self.hp = inf  # hp is how many enemies can the bullet hit
        basic_atk = 10
        self.atk = basic_atk * (1/2 + level/2) # 升級

        self.basic_speed = 10
        self.vec = (self.basic_speed * (3/4 + level/4) * cos(self.angle), self.basic_speed * (3/4 + level/4) * sin(self.angle))
        # 升級

    def update(self, dt):
        should_return = False
        if dist(self.player.pos, self.pos) >= DOG_MAX_DIST or should_return:
            angle = atan((self.pos[1] - self.player.pos[1])/(self.pos[0] - self.player.pos[0]))
            vec = (self.basic_speed * (3/4 + self.level/4) * cos(angle), self.basic_speed * (3/4 + self.level/4) * sin(angle))
            self.pos += vec * dt

            if dist(self.player.pos, self.pos) > 2:# 還沒回到玩家身邊
                should_return = True
            else:
                should_return = False
        else:
            self.pos += self.vec * dt
        self.rect.center = self.pos

    def shoot(self):
        bullets = pygame.sprite.Group()
        bullets.add(SledDog(self.player, self.enemies, color='0000ff', level = 1))

# 聖誕老人的鬍子
# 鬍子定軌跡的在玩家上下方移動
# 一定時間會繞720度(玩家沒有移動的話軌跡呈兩個在玩家位置相切的圓形，或8字形)，迴力鏢
# 升級後飛比較快、攻擊力增加
BREAD_DIST = 50 # 鬍子軌跡圓的半徑
class SantaBread(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level):
        super().__init__()
        self.level = level
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = self.player.pos
        self.player = player
        basic_angular_vec = 6
        # 360/angular_vec * dt 是轉一圈需要的時間
        self.angular_vec = basic_angular_vec * (1/2 + level/2) # 升級
        basic_atk = 5
        self.atk = basic_atk * (1/2 + level/2) # 升級
        self.hp = inf  # hp is how many enemies can the bullet hit
        self.enemies = enemies
        self.total_degree = 0 # 紀錄目前鬍子轉到哪 

    def update(self, dt):
        self.total_degree += self.angular_vec * dt
        self.total_degree %= 720
        self.pos = (self.player[0] - BREAD_DIST * cos(self.total_degree/2) * sin(self.total_degree/2), self.player[1] - BREAD_DIST * sin(self.total_degree/2)**2)

    def shoot(self):
        bullets = pygame.sprite.Group()
        bullets.add(SantaBread(self.player, self.enemies, color='0000ff', level = 1))

# 禮物
# 從玩家的面對方發射，發射到定點會爆炸(手榴彈)，且方向僅左右
# 爆炸會產生一圈rect，對接觸到的怪物造成傷害
# 升級後飛比較快(也就是更快擁有新的禮物)、攻擊力增加、攻擊範圍增加
# 匯入圖片的時候玩家的禮物固定一兩個顏色就好
GIFT_SOOT_DIST = 100
class Gift(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level):
        super().__init__()
        self.level = level
        self.image_show = pygame.Surface([15, 15])# image_show是禮物的圖片
        self.image_show.fill(color)
        self.image_show.rect = self.image_show.get_rect()
        self.player = player
        if self.player.drct == 'left':
            self.pos = self.player.rect.left
        if self.player.drct == 'right':
            self.pos = self.player.rect.right

        basic_vec = 40
        self.vec = basic_vec * (1/2 + level/2) # 升級
        basic_atk = 10
        self.atk = basic_atk * (1/2 + level/2) # 升級
        self.hp = inf  # hp is how many enemies can the bullet hit
        self.enemies = enemies
        self.total_dist = 0 # 紀錄目前禮物飛到哪裡
        self.should_explode = False
        self.hold_time = 0 # 爆炸造成傷害的時間
        basic_radius = 50
        self.radius = basic_radius * (3/4 + level/4)
        if self.should_explode:
            self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        else:
            self.image = pygame.Surface([0 , 0])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def update(self, dt):
        if self.player.drct == 'left':
            self.pos[0] -= self.vec * dt
        if self.player.drct == 'right':
            self.pos[0] += self.vec * dt
        self.total_dist += self.vec * dt
        if self.total_dist >= GIFT_SOOT_DIST:
            self.should_explode = True
            self.vec = 0
        if self.should_explode:
            self.hold_time += dt
        if self.hold_time >= 10 * dt:
            self.kill()

    def shoot(self):
        bullets = pygame.sprite.Group()
        bullets.add(Gift(self.player, self.enemies, color='0000ff', level = 1))

# LED燈條
