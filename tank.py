"""
Tank
    enemytank
    herotank
wall
    brickwall
    stealwall
    grasswall
    waterwall
Bullet:敌我共用
Eagle
Game
"""
import random
import time

import pygame

# pygame初始化
pygame.init()

WINDOW_W = 1200
WINDOW_H = 720
WINDOW = pygame.display.set_mode((WINDOW_W, WINDOW_H))

"""
坦克
    属性：图片，坐标，血量，速度,方向
    方法：移动，发射
"""


class Tank:
    def __init__(self, x, y):
        self.speed = 1
        self.hp = 2
        self.direction = "U"
        self.image = pygame.image.load(f'images/enemy1{self.direction}.gif')

        # 获取图片rect属性
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 新增属性
        self.bullet_list = []

        # 新增旧坐标
        self.oldx = self.rect.x
        self.oldy = self.rect.y

        # 增加坦克状态
        self.is_alive = True

    def move(self):
        self.oldx = self.rect.x
        self.oldy = self.rect.y

        if self.direction == "U":
            if self.rect.y > 0:
                self.rect.y -= self.speed
        if self.direction == "D":
            self.rect.y += self.speed if self.rect.y <= WINDOW_H - self.rect.height else 0
        if self.direction == 'L':
            self.rect.x -= self.speed if self.rect.x > 0 else 0
        if self.direction == 'R':
            self.rect.x += self.speed if self.rect.x < WINDOW_W - self.rect.width else 0

    def fire(self):
        """发射子弹"""
        bullet = Bullet(self)
        self.bullet_list.append(bullet)

    def back(self):
        self.rect.x = self.oldx
        self.rect.y = self.oldy


class HeroTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 10
        # 更改图片
        self.image = pygame.image.load(f'images/p1tank{self.direction}.gif')

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.direction = 'L'  # 更改方向
            self.image = pygame.image.load(f'images/p1tank{self.direction}.gif')  # 重新加载图片
            super().move()  # 父类方法去移动

        elif pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.direction = 'R'
            self.image = pygame.image.load(f'images/p1tank{self.direction}.gif')
            super().move()
        elif pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self.direction = 'U'
            self.image = pygame.image.load(f'images/p1tank{self.direction}.gif')
            super().move()
        elif pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.direction = 'D'
            self.image = pygame.image.load(f'images/p1tank{self.direction}.gif')
            super().move()


class EnemyTank(Tank):
    def __init__(self):
        super().__init__(random.randint(0, WINDOW_W - 60), 0)
        self.image = pygame.image.load(f'images/enemy1{self.direction}.gif')

        self.speed = 1

    def random_direction(self):
        """随机方向"""
        return random.choice(['U', 'D', 'R', 'L'])

    def move(self):
        super().move()
        # 控制速率
        x = random.randint(1, 200)
        if x == 10:
            self.direction = self.random_direction()  # 控制方向
            self.image = pygame.image.load(f'images/enemy{random.randint(1, 3)}{self.direction}.gif')  # 更改图片


class Wall:
    """
    属性：血量，类型，坐标，图片
    方法：阻挡其他元素
    """

    def __init__(self, type_, x, y):
        self.hp = 1000  # 无敌
        self.image = pygame.image.load(f'images/{type_}.gif')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 新增墙状态
        self.is_alive = True

    def block_item(self, item):
        """区别坦克和子弹"""
        if isinstance(item, Tank):  # 坦克
            if pygame.Rect.colliderect(self.rect, item.rect):
                print("碰撞了--------------")
                item.back()  # 恢复上一次位置
        if isinstance(item, Bullet):  # 子弹
            if pygame.Rect.colliderect(self.rect, item.rect):
                print("子弹碰撞了")
                item.is_alive = False  # 修改子弹状态
                self.hp -= 1
                if self.hp <= 0:
                    self.is_alive = False


class BrickWall(Wall):
    def __init__(self, type_, x, y):
        super().__init__(type_, x, y)
        self.hp = 3


class Water(Wall):
    def block_item(self, item):
        if isinstance(item, Tank):  # 坦克
            if pygame.Rect.colliderect(self.rect, item.rect):
                print("碰撞了--------------")
                item.back()  # 恢复上一次位置


class Steel(Wall):
    pass


class Bullet:
    """
    属性：速度，damage,图片，坐标,方向
    方法：移动
    """

    def __init__(self, tank):
        self.direction = tank.direction  # 子弹方向和坦克一致
        self.image = pygame.image.load('images/enemymissile.gif')
        self.speed = 200
        self.rect = self.image.get_rect()

        # 自己计算坐标
        self.rect.x = tank.rect.x + tank.rect.width // 2 - self.rect.width // 2  # 子弹的中心点横坐标
        self.rect.y = tank.rect.y + tank.rect.height // 2 - self.rect.height // 2  # 子弹的中心点纵坐标

        # 子弹状态
        self.is_alive = True

    def move(self):
        if self.direction == "U":
            if self.rect.y > -self.rect.height:
                self.rect.y -= self.speed
            else:
                self.is_alive = False
        if self.direction == "D":
            if self.rect.y < WINDOW_H + self.rect.height:
                self.rect.y += self.speed
            else:
                self.is_alive = False
        if self.direction == 'L':
            if self.rect.x > - self.rect.width:
                self.rect.x -= self.speed
            else:
                self.is_alive = False
        if self.direction == 'R':
            if self.rect.x < WINDOW_W + self.rect.width:
                self.rect.x += self.speed
            else:
                self.is_alive = False

    def hit_enemy(self, item):
        if pygame.Rect.colliderect(self.rect, item.rect):
            print("碰撞了--------------")
            self.is_alive = False
            item.hp -= 1
            if item.hp <= 0:
                item.is_alive = False


class Eagle:
    pass


class Game:
    def __init__(self):
        # 设置窗口标题
        pygame.display.set_caption("坦克大战")
        # 设置图标
        logo_img = pygame.image.load('images/enemy2L.gif')
        pygame.display.set_icon(logo_img)

        # 加载背景图
        self.bg_img = pygame.image.load("images/bg3.jpg")

        # 创建坦克
        self.tank = HeroTank(random.randint(0, 1140), WINDOW_H - 60)

        # 创建敌方坦克
        self.enemy_tank_list = [EnemyTank() for i in range(5)]

        # 记录所有墙
        self.wall_list = []
        for i in range(20):
            if i % 2 == 0:
                # 创建砖墙
                brick = BrickWall('walls', random.randrange(0, WINDOW_W - 60, 60),
                                  random.randrange(60, WINDOW_H - 120, 60))
                self.wall_list.append(brick)
            elif i % 3 == 0:
                steel = Steel('steels', random.randrange(0, WINDOW_W - 60, 60),
                              random.randrange(60, WINDOW_H - 120, 60))
                self.wall_list.append(steel)
            else:
                water = Water('water', random.randrange(0, WINDOW_W - 60, 60), random.randrange(60, WINDOW_H - 120, 60))
                self.wall_list.append(water)

        # 新增障碍物列表
        # self.add_wall_list = []

    def draw(self):
        """贴图"""
        # 贴背景图
        WINDOW.blit(self.bg_img, (0, 0))
        if self.tank.is_alive:
            # 贴坦克图
            WINDOW.blit(self.tank.image, (self.tank.rect.x, self.tank.rect.y))
        else:
            print("游戏结束")
            exit()

        # 贴敌方坦克图
        for enemy_tank in self.enemy_tank_list:
            if enemy_tank.is_alive:
                # 贴图
                WINDOW.blit(enemy_tank.image, (enemy_tank.rect.x, enemy_tank.rect.y))
            else:
                self.enemy_tank_list.remove(enemy_tank)

            # 贴敌方子弹图
            for bullet in enemy_tank.bullet_list:
                if bullet.is_alive:
                    WINDOW.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
                else:
                    # 删除飞出边界的子弹
                    enemy_tank.bullet_list.remove(bullet)
        # 贴我方子弹图
        for bullet in self.tank.bullet_list:
            if bullet.is_alive:
                WINDOW.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
            else:
                # 删除飞出边界的子弹
                self.tank.bullet_list.remove(bullet)

        # 贴墙图
        for wall in self.wall_list:
            if wall.is_alive:
                WINDOW.blit(wall.image, (wall.rect.x, wall.rect.y))
            else:
                self.wall_list.remove(wall)

        # for wall in self.add_wall_list:
        #     if wall.is_alive:
        #         WINDOW.blit(wall.image, (wall.rect.x, wall.rect.y))
        #     else:
        #         self.wall_list.remove(wall)

    def block_item(self):
        # 判定墙和其他元素
        for wall in self.wall_list:
            # 与我方坦克碰撞
            wall.block_item(self.tank)
            # 我方子弹
            for bullet in self.tank.bullet_list:
                wall.block_item(bullet)

            # 与敌方坦克
            for enemy_tank in self.enemy_tank_list:
                wall.block_item(enemy_tank)

                # 与敌方子弹检查
                for bullet in enemy_tank.bullet_list:
                    # 和墙碰撞
                    wall.block_item(bullet)
                    # 敌方子弹和我方坦克
                    bullet.hit_enemy(self.tank)

        # 我方子弹和敌方坦克
        for bullet in self.tank.bullet_list:
            for enemy_tank in self.enemy_tank_list:
                bullet.hit_enemy(enemy_tank)

        # 敌方子弹和我方坦克

    def move(self):
        """元素移动"""
        # 我方坦克移动
        self.tank.move()
        # 敌方坦克移动
        for enemy_tank in self.enemy_tank_list:
            enemy_tank.move()

            # 敌方子弹移动
            for bullet in enemy_tank.bullet_list:
                bullet.move()

        # 我方子弹移动
        for bullet in self.tank.bullet_list:
            bullet.move()

    def update(self):
        """刷新"""
        pygame.display.update()

    def event(self):
        for event in pygame.event.get():
            # 1. 鼠标点击关闭窗口事件
            if event.type == pygame.QUIT:
                print("点击关闭窗口按钮")
                exit()  # 关闭程序

            if event.type == pygame.KEYDOWN:
                # 判断用户按键
                if event.key == pygame.K_SPACE:
                    self.tank.fire()
                if event.key == pygame.K_0:
                    for enemy_tank in self.enemy_tank_list:
                        enemy_tank.fire()

                if event.key == pygame.K_ESCAPE:
                    self.wall_list.clear()
                    self.enemy_tank_list.clear()
                    # self.add_wall_list.clear()

                # if event.key == pygame.K_1:
                #     brick = BrickWall('walls',random.randrange(0, WINDOW_W - 60, 60),random.randrange(60, WINDOW_H - 120, 60))
                #     self.add_wall_list.append(brick)

    def run(self):
        while True:
            # 贴图
            self.draw()
            # 调用事件
            self.event()
            # 调用移动方法
            self.move()
            # 阻挡元素
            self.block_item()
            # 刷新
            self.update()
            pass


if __name__ == '__main__':
    game = Game()
    game.run()
