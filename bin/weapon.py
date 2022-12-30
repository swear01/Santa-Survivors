import pygame
from pygame.locals import * # CONSTS
from math import cos, sin, pi, dist, inf, atan
from numpy import array
from numpy.linalg import norm
from .enemy import Enemy
from main import width, height

# class Weapon:
#     def __init__(self, name, player, 
#         atk=10, reload=1, b_speed=70, b_hp=1,b_amt=1):
#         self.name = name
#         self.player = player
#         self.cooldown = reload
#         self.reload = reload
#         self.atk = atk
#         self.b_speed = b_speed
#         self.b_hp = b_hp
#         self.b_amt = b_amt

#     def shoot(self, pos, enemies):
#         if self.name == 'test':
#             bullets = pygame.sprite.Group()
#             for i in range(self.b_amt):
#                 angle = 2*i*pi/self.b_amt
#                 vec = (self.b_speed*cos(angle),self.b_speed*sin(angle))
#                 bullets.add(Bullet(pos, vec, self.player, color='#0000ff', hp=self.b_hp, atk=self.atk, kind='normal'))
#             return bullets

#         if self.name == 'autoaim':
#             if not enemies : return []
#             nearest_enemy = Enemy.nearest_enemy(pos, enemies)
#             vec = nearest_enemy.pos-self.player.pos
#             vec *= self.b_speed/norm(vec)
#             return Bullet(pos, vec, self.player, color='#ff00ff', hp=self.b_hp, atk=self.atk, kind='autoaim')         

# 基礎雪球
# 往七個方向發射，對敵人造成一次傷害後會消失
# 升級後攻擊力變強、數量變多
SnowBall_basic_atk = 10
SnowBall_basic_amt = 7
class SnowBall(pygame.sprite.Sprite):
    def __init__(self, player, enemies, color, level, no): # no 表示第幾個此類武器，其餘武器default no恆等於1
        super().__init__()
        self.image = pygame.Surface([8,8])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.player = player
        self.pos = player.pos
        self.rect.center = player.pos
        self.vec = 70
        self.hp = 1 # hp is how many enemies can the bullet hit
        self.atk = SnowBall_basic_atk * (1/2 + level/2) # 升級
        self.amt = SnowBall_basic_amt + level//3 # 升級
        self.no = no

    def update(self, dt):
        #out of screen and disappear
        if self.pos[0] > width + 100 or self.pos[0] < -100 or self.pos[1] > height + 100 or self.pos[1] < -100 :
            self.kill()
            return
        if self.hp == 0 : 
            self.kill()
            return
        angle = 2 * (self.no-1) * pi / self.amt
        vec = (self.vec * cos(angle), self.vec * sin(angle))
        self.pos += vec * dt
        self.rect.center = self.pos
    def shoot(self, level):
        bullets = pygame.sprite.Group()
        for i in range(self.amt):
            bullets.add(SnowBall(self.player, self.enemies, color='#0000ff', level = level, no = i + 1))
    

# 瞄準型雪球
# 往最近的敵人發射，預設可用兩次(hp = 2)
# 升級後攻擊力變強、可以用更多次
AimSnowBall_basic_atk = 10
AimSnowBall_basic_hp = 2
class AimSnowBall(pygame.sprite.Sprite):
    def __init__(self, player, enemies, color, level, no):
        super().__init__()
        self.image = pygame.Surface([8,8])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.player = player
        self.pos = player.pos
        self.rect.center = player.pos
        self.vec = 70
        self.hp = AimSnowBall_basic_hp + level//3 # 升級
        self.atk = AimSnowBall_basic_atk * (1/2 + level/2) # 升級
    def update(self, dt):
        #out of screen and disappear
        if self.pos[0] > width + 100 or self.pos[0] < -100 or self.pos[1] > height + 100 or self.pos[1] < -100 :
            self.kill()
            return
        if self.hp == 0 : 
            self.kill()
            return
        nearest_enemy = Enemy.nearest_enemy(self.player.pos, self.enemies)
        angle = atan((self.player.pos[1] - nearest_enemy.pos[1])/(self.player.pos[0] - nearest_enemy.pos[0]))
        vec = (self.vec * cos(angle), self.vec * sin(angle))
        self.pos += vec * dt
        self.rect.center = self.pos
    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(AimSnowBall(self.player, self.enemies, color='#0000ff', level = level, no = 1))


# 鹿角(麋鹿的起始武器)
# 防禦型武器，怪物碰到鹿角那一面會扣血，其餘部分扣玩家血
# 升級後鹿角會變大、攻擊力變強
DeerAntler_height = 52.5 # 鹿的圖片高 * 1.5
DeerAntler_basic_atk = 10
class DeerAntler(pygame.sprite.Sprite):
    def __init__(self, player, enemies, color, level, no):
        super().__init__()
        self.level = level
        self.image = pygame.Surface([20, DeerAntler_height * (3/4 + level/4)]) # 升級
        self.image.fill(color) # 要以陰影或虛線標示攻擊範圍
        self.rect = self.image.get_rect()
        self.player = player
        if self.player.drct == 'left':
            self.pos = self.player.rect.left
        if self.player.drct == 'right':
            self.pos = self.player.rect.right
        self.atk = int(DeerAntler_basic_atk * (1/2 + level/2)) #  升級
        self.hp = inf # hp is how many enemies can the bullet hit
        self.enemies = enemies

    def update(self, dt):
        if self.player.direction == 'left':
            self.pos = self.player.rect.left
        if self.player.direction == 'right':
            self.pos = self.player.rect.right
        self.rect.center = self.pos

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(DeerAntler(self.player, self.enemies, color='#0000ff', level = level, no = 1))

# 雪橇(聖誕老人的起始武器)
# 從玩家的下方，由左而右水平開過去，到螢幕邊界會重新從左邊開進去
# 升級後雪橇速度變快、變大台、攻擊力變強
# 升級後可以開兩台的有空再補
Sled_height = 40 # 雪橇圖片高
Sled_basic_vec = 40
Sled_basic_atk = 10
class Sled(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level, no):
        super().__init__()
        self.level = level 
        self.image = pygame.Surface([40, Sled_height * (3/4 + level/4)]) # 升級
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.topright = (0, self.player.pos[1]-Sled_height/2)
        self.vec = Sled_basic_vec * (1/2 + level/2) # 升級
        self.atk = Sled_basic_atk * (1/2 + level/2) # 升級
        self.hp = inf  # hp is how many enemies can the bullet hit
        self.enemies = enemies

    def update(self, dt):
        self.x += self.vec * dt
        if self.left >= width:
            self.rect.topright = (0, self.player.pos[1]-Sled_height/2)

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(Sled(self.player, self.enemies, color='0000ff', level = level, no = 1))

# 鏟子(花園小精靈的起始武器)
# 會瞄準離玩家最近的敵人
# 傷害力較高，但只有鏟子頭有攻擊功能
# 升級後鏟子頭變大、攻擊力增加
Shovel_side_length = 10 # 鏟子頭的邊長
Shovel_basic_atk = 20
class Shovel(pygame.sprite.Sprite):
    def __init__(self, player,enemies, color, level, no):
        super().__init__()
        self.level = level
        self.angle = atan((self.player.pos[1] - self.nearest_enemy.pos[1])/(self.player.pos[0] - self.nearest_enemy.pos[0]))
        self.image = pygame.Surface([Shovel_side_length * (3/4 + level/4), Shovel_side_length * (3/4 + level/4)]) # 升級
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
        self.atk = Shovel_basic_atk * level # 升級

    def update(self, dt):
        self.rect.pos = (self.player.pos[0] - 25 * cos(self.angle), self.player.pos[1] - 25 * sin(self.angle))
        self.rect.center = self.rect.pos

        self.image_show = pygame.transform.rotate(self.image_show_ori, self.angle)       

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(Shovel(self.player, self.enemies, color='0000ff', level = level, no = 1))

# 雪橇犬
# 會去找離自己最近的敵人攻擊
# 離玩家太遠(SledDog_max_dist = 200)會跑回玩家身邊，再出發去尋找敵人
# 升級後跑比較快、攻擊力增加
SledDog_max_dist = 200
SledDog_basic_atk = 15
SledDog_basic_vec = 50
class SledDog(pygame.sprite.Sprite):
    def __init__(self, player,enemies, color, level, no):
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
        self.atk = SledDog_basic_atk * (1/2 + level/2) # 升級
        self.vec = (SledDog_basic_vec * (3/4 + level/4) * cos(self.angle), self.basic_speed * (3/4 + level/4) * sin(self.angle))
        # 升級
        self.should_return = False
    def update(self, dt):
        if dist(self.player.pos, self.pos) >= SledDog_max_dist or self.should_return:
            angle = atan((self.pos[1] - self.player.pos[1])/(self.pos[0] - self.player.pos[0]))
            vec = (SledDog_basic_vec * (3/4 + self.level/4) * cos(angle), SledDog_basic_vec * (3/4 + self.level/4) * sin(angle))
            self.pos += vec * dt

            if dist(self.player.pos, self.pos) > 2:# 還沒回到玩家身邊
                self.should_return = True
            else:
                self.should_return = False
        else:
            self.pos += self.vec * dt
        self.rect.center = self.pos

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(SledDog(self.player, self.enemies, color='0000ff', level = level, no = 1))

# 聖誕老人的鬍子
# 鬍子定軌跡的在玩家上下方移動
# 一定時間會繞720度(玩家沒有移動的話軌跡呈兩個在玩家位置相切的圓形，或8字形)，迴力鏢
# 升級後飛比較快、攻擊力增加
SantaBread_dist = 50 # 鬍子軌跡圓的半徑
SantaBread_basic_angularvec = 6 # 360/SantaBread_basic_angularvec * dt 是轉一圈需要的時間
SantaBread_basic_atk = 5
class SantaBread(pygame.sprite.Sprite):
    def __int__(self, player, enemies, color, level, no):
        super().__init__()
        self.level = level
        self.image = pygame.Surface([15, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = self.player.pos
        self.player = player

        self.angular_vec = SantaBread_basic_angularvec * (1/2 + level/2) # 升級
        self.atk = SantaBread_basic_atk * (1/2 + level/2) # 升級
        self.hp = inf  # hp is how many enemies can the bullet hit
        self.enemies = enemies
        self.total_angle = 0 # 紀錄目前鬍子轉到哪 

    def update(self, dt):
        self.total_angle += self.angular_vec * dt
        self.total_angle %= 720
        self.pos = (self.player[0] - SantaBread_dist * cos(self.total_angle/2) * sin(self.total_angle/2), self.player[1] - SantaBread_dist * sin(self.total_angle/2)**2)

    def shoot(self, level):
        bullets = pygame.sprite.Group()
        bullets.add(SantaBread(self.player, self.enemies, color='0000ff', level = level, no = 1))

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
            bullets.add(Seal(self.player, self.enemies, color='0000ff', level = level, no = i+1))
