from math import atan2, cos, dist, inf, pi, sin, degrees

import pygame
from numpy import array
from numpy.linalg import norm
from pygame.locals import *  # CONSTS

from .config import *
from .enemy import Enemy

from configparser import ConfigParser, ExtendedInterpolation

from json import loads

weapon_config = ConfigParser(interpolation=ExtendedInterpolation())
weapon_config.read('./data/config/weapon.ini')

def out_of_screen(pos):
    return pos[0] > width + 100 or pos[0] < -100 or pos[1] > height + 100 or pos[1] < -100


#remember, damage calculate at contact
class Weapon:
    def __init__(self, weapon_name, player):
        self.name = weapon_name
        config = weapon_config[self.name]
        self.max_level = int(config['max_level'])
        self.image = pygame.image.load(config['img_dir']).convert_alpha()
        self.level = 0
        self.player = player


    def can_upgrade(self):
        return self.level < self.max_level

class Snowball_bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos, vec, atk, hp=1):
        super().__init__()
        self.hp = hp
        self.vec = vec
        self.pos = pos
        self.atk = atk
        self.image = image
        self.rect = self.image.get_rect()

    def update(self, dt):
        #out of screen and disappear
        if out_of_screen(self.pos) or self.hp == 0 :
            return self.kill()
        self.pos += self.vec * dt
        self.rect.center = self.pos

# 基礎雪球
# 往多個方向發射，對敵人造成一次傷害後會消失
# 升級後攻擊力變強、數量變多
class Snowball(Weapon):
    def __init__(self, player): # no 表示第幾個此類武器，其餘武器default no恆等於1
        super().__init__('Snowball', player)
        config = weapon_config[self.name]
        self.image = pygame.transform.scale(self.image,(15,15))
        self.speed = loads(config['speed'])
        self.atk = loads(config['atk'])
        self.bullet_amount = loads(config['bullet_amount'])
        self.shoot_period = loads(config['shoot_period'])
        self.shoot_timer = self.calc_shoot_period()

    def calc_shoot_period(self):
        return self.shoot_period[self.level]

    def update(self, dt):
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        self.shoot_timer += self.calc_shoot_period()

        return self.shoot()

    def shoot(self):
        bullets = pygame.sprite.Group()
        for i in range(self.bullet_amount[self.level]):
            angle = 2*i*pi/self.bullet_amount[self.level]
            vec = array((self.speed[self.level]*cos(angle),self.speed[self.level]*sin(angle)))
            bullets.add(Snowball_bullet(self.image, self.player.pos.copy(), vec, self.atk[self.level]))
        return bullets
    

# 瞄準型雪球
# 往最近的敵人發射，預設可用兩次(hp = 2)
# 升級後攻擊力變強、可以用更多次
class Aim_snowball(Weapon):
    def __init__(self, player): # no 表示第幾個此類武器，其餘武器default no恆等於1
        super().__init__('Aim_snowball', player)
        config = weapon_config[self.name]
        self.image = pygame.transform.scale(self.image,(25,25))
        self.speed = loads(config['speed'])
        self.atk = loads(config['atk'])
        self.bullet_hp = loads(config['bullet_hp'])
        self.shoot_period = loads(config['shoot_period'])
        self.shoot_timer = self.calc_shoot_period()

    def calc_shoot_period(self):
        return self.shoot_period[self.level]

    def update(self, dt):
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        self.shoot_timer += self.calc_shoot_period()

        return self.shoot()

    def shoot(self):
        nearest_enemy = self.player.nearest_enemy()
        if not nearest_enemy : return []
        vec = nearest_enemy.pos-self.player.pos
        vec *= self.speed[self.level]/norm(vec)
        return Snowball_bullet(self.image, self.player.pos.copy(), 
            vec, self.atk[self.level],self.bullet_hp[self.level])  

# 鹿角(麋鹿的起始武器)
# 防禦型武器，怪物碰到鹿角那一面會扣血，其餘部分扣玩家血
# 升級後鹿角會變大、攻擊力變強
DeerAntler_height = 52.5 # 鹿的圖片高 * 1.5
DeerAntler_basic_atk = 10

class Deer_antler_bullet(pygame.sprite.Sprite):
    def __init__(self, image, player, atk, level) -> None:
        super().__init__()
        self.images = [image, pygame.transform.flip(image, True, False)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.player = player
        self.atk = atk
        self.level = level
        self.hp = float('inf')

    def update(self, dt):
        print('update')
        self.pos = self.player.pos.copy()
        if self.player.drct == 'left':
            self.pos += (-15, -30)
            self.image = self.images[1]
        if self.player.drct == 'right':
            self.pos += (15,-30)
            self.image = self.images[0]
        self.rect.center = self.pos


class Deer_antler(Weapon):
    def __init__(self, player):
        super().__init__('Deer_antler', player)
        config = weapon_config[self.name]
        self.atk = loads(config['atk'])
        self.bullet = Deer_antler_bullet(self.image, self.player, self.atk[self.level], 1) #let it reset in update

    def update(self, dt):
        if self.level == self.bullet.level : return []
        self.bullet.kill()
        self.bullet = Deer_antler_bullet(self.image, self.player, self.atk[self.level], self.level)
        return self.bullet

# 雪橇(聖誕老人的起始武器)
# 從玩家的下方，由左而右水平開過去，到螢幕邊界會重新從左邊開進去
# 升級後雪橇速度變快、變大台、攻擊力變強
# 升級後可以開兩台的有空再補
class Sled_bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos, vec, atk) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.vec = vec
        self.hp = float('inf')
        self.atk = atk

    def update(self, dt):
        if out_of_screen(self.pos):
            return self.kill()
        self.pos += self.vec * dt
        self.rect.center = self.pos

class Sled(Weapon):
    def __init__(self, player):
        super().__init__('Sled', player)
        config = weapon_config[self.name]
        self.image = pygame.transform.scale2x(self.image)
        self.atk = loads(config['atk'])
        self.speed = loads(config['speed'])
        self.bullet_amount = loads(config['bullet_amount'])
        self.shoot_period = float(config['shoot_period'])
        self.shoot_timer = self.shoot_period
        self.bullets = pygame.sprite.Group()

    def update(self, dt):
        self.shoot_timer -= dt
        if len(self.bullets) == self.bullet_amount[self.level]: return []
        if self.shoot_timer >= 0 : return []
        self.shoot_timer = self.shoot_period
        sled_pos = array((-80, self.player.pos[1]))
        sled_vec = array((self.speed[self.level], 0))
        sled_bullet = Sled_bullet(self.image, sled_pos, sled_vec, self.atk[self.level])
        self.bullets.add(sled_bullet)
        return [sled_bullet]

        

# 鏟子(花園小精靈的起始武器)
# 會瞄準離玩家最近的敵人
# 傷害力較高，但只有鏟子頭有攻擊功能
# 升級後鏟子頭變大、攻擊力增加
Shovel_side_length = 10 # 鏟子頭的邊長
Shovel_basic_atk = 20
class Shovel_head(pygame.sprite.Sprite):
    def __init__(self, image, player, hp, atk_real, shoot_wait, nearest_enemy) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.player = player
        self.atk_real = atk_real
        self.shoot_wait = shoot_wait
        self.enemy = nearest_enemy
        self.atk = 0

        self.hp_real = hp
        self.hp = float('inf')

    def update(self, dt):
        self.shoot_wait -= dt
        self.pos = self.enemy.pos.copy()
        self.rect.center = self.pos
        if self.shoot_wait > 0 : return
        #after attack disappear
        if self.atk != 0 : return self.kill()
        self.atk = self.atk_real
        self.hp = self.hp_real
        
        


class Shovel(Weapon):
    def __init__(self, player):
        super().__init__('Shovel', player)
        config = weapon_config[self.name]
        self.atk = loads(config['atk'])
        self.hp = int(config['hp'])
        self.max_track_distance = int(config['max_track_distance'])
        self.shoot_period = loads(config['shoot_period'])
        self.shoot_timer = 0

    def update(self, dt):
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        
        nearest_enemy = self.player.nearest_enemy()
        if not nearest_enemy : return []
        vec = nearest_enemy.pos - self.player.pos 
        if norm(vec) > self.max_track_distance : return []

        #success shoot
        self.shoot_timer = self.shoot_period[self.level]
        angle = degrees(atan2(*vec))
        image = pygame.transform.rotate(self.image, angle)

        return Shovel_head(image, self.player, self.hp, self.atk[self.level], 
            self.shoot_period[self.level]/2, nearest_enemy)  


# 雪橇犬
# 會去找離自己最近的敵人攻擊
# 離玩家太遠(SledDog_max_dist = 200)會跑回玩家身邊，再出發去尋找敵人
# 升級後跑比較快、攻擊力增加
class Sled_dog_bullet(pygame.sprite.Sprite):
    def __init__(self, image, player, speed, atk, atk_period, max_distance) -> None:
        super().__init__()
        self.images = [image, pygame.transform.flip(image, True, False)]
        self.image = self.images[0]
        self.max_distance = max_distance
        self.rect = self.image.get_rect()
        self.player = player
        self.pos = self.player.pos.copy()
        self.speed = speed
        self.hp = 0
        self.atk = atk
        self.atk_period = atk_period
        self.atk_timer = 0
        self.target_enemy = pygame.sprite.Group()

    def update(self, dt):
        if norm(self.pos - self.player.pos) > self.max_distance:
            return self.kill()
        if not self.target_enemy.has():
            nearest_enemy = self.nearest_enemy(self.player.enemies)
            if not nearest_enemy : return
            self.target_enemy.add(nearest_enemy)
        if norm(self.pos - self.target_enemy.sprites()[0].pos) > 10 : 
            vec = self.target_enemy.sprites()[0].pos - self.pos
            vec *= self.speed/norm(vec)
            self.pos += vec*dt

            #animations
            if vec[0] > 0 :
                self.image = self.images[1]
            if vec[0] < 0 :
                self.image = self.images[0]

        if self.hp <= 0 :
            self.atk_timer -= dt
            if self.atk_timer <= 0 :
                self.atk_timer = self.atk_period
                self.hp += 1
        self.rect.center = self.pos
        

    def nearest_enemy(self, enemies):
        if not enemies : return None
        return min(enemies, key=lambda enemy: norm(enemy.pos-self.pos))        

class Sled_dog(Weapon):
    def __init__(self, player):
        super().__init__('Sled_dog', player)
        config = weapon_config[self.name]
        self.image = pygame.transform.scale(self.image, array(self.image.get_size())//2)
        self.atk = loads(config['atk'])
        self.speed = loads(config['speed'])
        self.atk_period = float(config['atk_period'])
        self.max_distance = int(config['max_distance'])
        self.bullets = pygame.sprite.Group()

    def update(self, dt):
        if len(self.bullets) >= 1:
            if self.bullets.sprites()[0].atk == self.atk[self.level]:
                return []
            self.bullets.sprites[0].kill()
        sled_dog_bullet = Sled_dog_bullet(self.image, self.player, 
            self.speed[self.level], self.atk[self.level], self.atk_period, self.max_distance)
        self.bullets.add(sled_dog_bullet)
        return [sled_dog_bullet]

# 聖誕老人的鬍子
# 鬍子定軌跡的在玩家上下方移動
# 上下繞8-curve
SantaBread_dist = 50 # 鬍子軌跡圓的半徑
SantaBread_basic_angularvec = 6 # 360/SantaBread_basic_angularvec * dt 是轉一圈需要的時間
SantaBread_basic_atk = 5
class Mustache_Bullet(pygame.sprite.Sprite):
    def __init__(self, image, player, speed, angular_speed, hp, atk):
        super().__init__()
        self.angle = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.player = player
        self.hp = hp
        self.atk = atk
        self.pos = self.player.pos.copy()
        self.speed = speed #actually size
        self.angular_speed = angular_speed

    def update(self, dt):
        if self.angle >= 2*pi : return self.kill()
        self.angle += self.angular_speed*dt
        relat_pos = array((0.5*sin(2*self.angle),cos(self.angle)))*self.speed
        self.pos = self.player.pos + relat_pos
        self.rect.center = self.pos

class Mustache(Weapon):
    def __init__(self, player):
        super().__init__('Mustache', player)
        config = weapon_config[self.name]
        self.shoot_period = float(config['shoot_period']) #無縫接軌
        self.shoot_timer = 0
        self.speed = loads(config['speed'])
        self.atk = loads(config['atk'])
        self.hp = int(config['hp'])

    def update(self, dt):
        self.shoot_timer -= dt
        if self.shoot_timer > 0 : return []
        self.shoot_timer += self.shoot_period
        angular_speed = 2*pi/self.shoot_period
        return Mustache_Bullet(self.image,self.player,self.speed[self.level],
            angular_speed, self.hp, self.atk[self.level])

# 禮物
# 從玩家的面對方發射，發射到定點會爆炸(手榴彈)，且方向僅左右
# 爆炸會產生一圈rect，對接觸到的怪物造成傷害
# 升級後飛比較快(也就是更快擁有新的禮物)、攻擊力增加、攻擊範圍增加
# 匯入圖片的時候玩家的禮物固定一兩個顏色就好
Gift_shoot_dist = 100
Gift_basic_vec = 40
Gift_basic_atk = 10
class Gift(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level, no):
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
        self.vec = Gift_basic_vec * (1/2 + level/2) # 升級
        self.atk = Gift_basic_atk * (1/2 + level/2) # 升級
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
        if self.total_dist >= Gift_shoot_dist:
            self.should_explode = True
            self.vec = 0
        if self.should_explode:
            self.hold_time += dt
        if self.hold_time >= 10 * dt:
            self.kill()

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(Gift(self.player, self.enemies, color='0000ff', level = level, no = 1))

# LED燈條
# 會以玩家為中心甩，造成的傷害低
# 升級後攻擊力增加、甩得比較快
# 要用到mask，在主函式或許需要多拉出來寫是否enemy overlap mask
LED_basic_angularvec = 6 # 360/angular_vec * dt 是轉一圈需要的時間
LED_basic_atk = 5
class LED(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level, no):
        super().__init__()
        self.level = level
        self.image_ori = pygame.Surface([8, 60]) # 圖片有半條是透明的，圖片中心會是玩家，燈條實際長度只有30
        self.image_ori.fill(color)
        self.image_ori_rect = self.image_ori.get_rect()
        self.image_ori_rect.center = self.player.pos
        self.image = self.image_ori.copy()
        self.player = player
        
        self.angular_vec = LED_basic_angularvec * (1/2 + level/2) # 升級
        self.atk = LED_basic_atk * (3/4 + level/4) # 升級
        self.hp = inf 
        self.enemies = enemies
        self.total_angle = 0 # 紀錄目前LED轉到哪
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.total_angle += self.angular_vec * dt
        self.total_angle %= 360
        self.pos = self.player.pos
        self.rect.center = self.pos
        self.image = pygame.transform.rotate(self.image_ori, self.total_angle)
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(LED(self.player, self.enemies, color='0000ff', level = level, no = 1))

# 拐杖糖
# 會以玩家為圓心，面對的方向為中心線，上下各甩出60度的範圍
# 造成的傷害比LED燈條略高，但還是希望他偏低
# 升級後攻擊力增加，甩得比較快
# 要用到mask，在主函式或許需要多拉出來寫是否enemy overlap mask
CandyCane_basic_angularvec = 4   # 240/angular_vec * dt 是轉一個週期需要的時間
CandyCane_basic_atk = 8
class CandyCane(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level, no):
        super().__init__()
        self.level = level
        self.image_ori = pygame.Surface([50, 20]) # 圖片有半條是透明的，圖片中心會是玩家，拐杖糖實際長度只有25
        # default圖片檔是橫的，透明部份在右邊
        self.image_ori.fill(color)
        self.image_ori_rect = self.image_ori.get_rect()
        self.image_ori_rect.center = self.player.pos

        if self.player.drct == 'left':
            self.image = self.image_ori.copy()
        if self.player.drct == 'right':
            self.image = pygame.transform.flip(self.image_ori,False,True)
        self.player = player
        self.angular_vec = CandyCane_basic_angularvec * (1/2 + level/2) # 升級
        self.atk = CandyCane_basic_atk * (3/4 + level/4) # 升級
        self.hp = inf 
        self.enemies = enemies
        self.total_angle = 0 # 紀錄目前拐杖糖轉到哪
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos = self.player.pos
        self.rect.center = self.pos
        if abs(self.total_angle) >= 60: # 和平衡位置差60度時轉回去
            self.angular_vec *= -1
        self.total_angle += self.angular_vec * dt
        if self.player.drct == 'left':
            self.image = pygame.transform.rotate(self.image_ori, self.total_angle)
        if self.player.drct == 'right':
            self.image1 = pygame.transform.flip(self.image_ori,False,True)
            self.image = pygame.transform.rotate(self.image1, self.total_angle)
        
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(CandyCane(self.player, self.enemies, color='0000ff', level = level, no = 1))


# 雪花/或雪地
# 玩家以自己目前位置為中心設立雪地，進入雪地的怪物會持續扣血且速度變慢，玩家速度不變
# 造成的傷害比LED還低，不然就是讓這武器不好被解鎖
# 升級後攻擊力增加、雪地範圍變大
SnowFlake_basic_sidelength = 50
SnowFlake_basic_atk = 3
class SnowFlake(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level, no):
        super().__init__()
        self.level = level
        self.side_length = SnowFlake_basic_sidelength * (3/4 + level/4) # 升級
        self.image = pygame.Surface([self.side_length, self.side_length])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.center = player.pos
        self.atk = SnowFlake_basic_atk * (1/2 + level/2) # 升級
        self.hp = inf  # hp is how many enemies can the bullet hit
        self.enemies = enemies
        self.hold_time = 0 # 單片雪花存活時間

    def update(self, dt):
        self.hold_time += dt
        if self.hold_time >= 100000 * dt:
            self.pos = self.player.pos
            self.hold_time = 0
    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(SnowFlake(self.player, self.enemies, color='0000ff', level = level, no = 1))


# 海豹
# 直線型迴力鏢，從玩家的左上、右上、右下、左下斜45度角出發，走過一定距離後，返回玩家身邊。
# 升級後移動速度變快，攻擊力變強
Seal_basic_vec = 30
Seal_basic_atk = 15
Seal_amt = 4
Seal_move_time = 100 # 單位是dt
class Seal(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level, no):
        super().__init__()
        self.level = level
        self.no = no
        self.image_ori = pygame.Surface([20, 20])
        self.image_ori.fill(color)
        if no == 1 or no == 4:
            self.image = self.image_ori.copy()
        if no == 2 or no == 3:
            self.image = pygame.transform.flip(self.image_ori, True, False)
        self.rect = self.image.get_rect()
        self.pos = self.player.pos
        self.player = player
        self.angle = 45 * no # 出發的角度
        self.vec = Seal_basic_vec * (3/4 + level/4) # 升級
        self.atk = Seal_basic_atk * (1/2 + level/2) # 升級
        self.hp = inf  # hp is how many enemies can the bullet hit
        self.enemies = enemies
        self.should_return = False
        self.move_time = 0

    def update(self, dt):
        if self.move_time >= Seal_move_time and not self.should_return:
            self.should_return = True
            self.move_time = 0
        if not self.should_return:
            self.pos -= (self.vec * cos(self.angle) * dt, self.vec * sin(self.angle) * dt)
            self.rect.center = self.pos
            self.move_time += 1
        if self.should_return and self.move_time < Seal_move_time:
            self.pos += ((self.player.pos[0] - self.pos[0])/Seal_move_time, (self.player.pos[1] - self.pos[1])/Seal_move_time)
            self.move_time += 1
        if self.should_return and self.move_time >= Seal_move_time:
            self.pos = self.player.pos
            self.move_time = 0
        self.rect.center = self.pos

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        for i in range(Seal_amt):
            bullet

weapon_list = {'Snowball':Snowball, 'Aim_snowball':Aim_snowball,
    'Deer_antler':Deer_antler, 'Sled':Sled, 'Shovel':Shovel,
    'Sled_dog':Sled_dog, 'Mustache':Mustache}