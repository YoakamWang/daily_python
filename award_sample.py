import random

where = ['重庆小面', '山东煎饼', '成都小馆', '东北烧饼']
target = random.choice(where)
print(f'今天中午吃：{target}')



where = ['赵老大', '钱老二', '孙老三', '李老四', '周老五', '吴老六', '郑老七', '王老八', '冯老九', '陈老十']
target = random.sample(where, 3)
print(f'三名中奖者分别是：{target}')