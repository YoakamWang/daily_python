import pygame


class Bg(pygame.sprite.Sprite):
    def __init__(self):
        super(Bg, self).__init__()
        bg_small = pygame.image.load('bg.png').convert_alpha()
        grass_land = bg_small.subsurface((0, 0, 128, 128))
        self.surf = pygame.transform.scale(grass_land, (800, 600))
        self.rect = self.surf.get_rect(left=0, top=0)  # 左上角定位


class Pig(pygame.sprite.Sprite):
    def __init__(self):
        super(Pig, self).__init__()
        self.surf = pygame.image.load('pig_in_car.png').convert_alpha()
        self.rect = self.surf.get_rect(center=(400, 300))  # 中心定位

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.move_ip((-5, 0))
        elif keys[pygame.K_RIGHT]:
            self.rect.move_ip((5, 0))
        elif keys[pygame.K_UP]:
            self.rect.move_ip((0, -5))
        elif keys[pygame.K_DOWN]:
            self.rect.move_ip((0, 5))

        # 防止小猪跑到屏幕外面
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600


class Goddess(pygame.sprite.Sprite):
    def __init__(self):
        super(Goddess, self).__init__()
        self.surf = pygame.image.load('building.png').convert_alpha()
        # self.surf = building.subsurface(((7 * 64 - 10, 0, 40, 75)))
        self.rect = self.surf.get_rect(center=(500, 430))  # 女神像的中心放到画布(500, 430)的位置


def main():
    pygame.init()
    pygame.display.set_caption('未闻Code：青南做的游戏')  # 游戏标题
    win = pygame.display.set_mode((800, 600))  # 窗口尺寸

    bg = Bg()
    goddess = Goddess()
    pig = Pig()
    all_sprites = [bg, goddess, pig]  # 注意添加顺序，后添加的对象图层在先添加的对象的图层上面

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击左上角或者右上角的x关闭窗口时，停止程序
                running = False

        keys = pygame.key.get_pressed()
        pig.update(keys)
        for sprite in all_sprites:
            win.blit(sprite.surf, sprite.rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()

# class Method1(object):
#
#     def __init__(self, name):
#         self.__name = name
#
#     def sayhello(self):
#         print("Method say hello!")
#
#     def __sayhi(self):
#         print("Method say hi!")
#
#
# # 初始化Method
# m = Method1("Python")
# # 调用sayhello方法
# m.sayhello()
# # 调用sayhi方法
# #m.__sayhi()
# m._Method1__sayhi()
# # 输出属性__name
# #print(m.__name)
# print(m._Method1__name)


# import glob
# result = glob.glob('**/*.py', recursive=True)
# print(result)
# name = '青南'
# salary = 99999
# msg = (f'我的名字是{name}'       f'我的月薪是{salary}')
# print(msg)

# import os

# py_files = []
# for root, folder, files in os.walk('.'):
#     for file in files:
#         if file.endswith('.py'):
#             py_files.append(os.path.join(root, file))
# print(py_files)

# import os
# all_file = os.listdir('.')
# target_file = [x for x in all_file if x.endswith('.py')]
# print(target_file)
# print(all_file)
# import contextlib
#
# def callback_1():
#     print('我是第一个回调函数')
#
# def callback_2(x):
#     print(f'我是第二个回调函数，传入参数：{x}')
# def callback_3():
#     print("hahaha")
#
# with contextlib.ExitStack() as stack:
#     stack.callback(callback_1)
#     stack.callback(callback_2, 100)
#     stack.callback(callback_3)
#     print(12345)
#     print('xxxx')
# print('退出缩进')


# import random
#
# where = ['重庆小面', '山东煎饼', '成都小馆', '东北烧饼']
# target = random.choice(where)
# print(f'今天中午吃：{target}')
#
#
#
# where = ['赵老大', '钱老二', '孙老三', '李老四', '周老五', '吴老六', '郑老七', '王老八', '冯老九', '陈老十']
# target = random.sample(where, 3)
# print(f'三名中奖者分别是：{target}')
