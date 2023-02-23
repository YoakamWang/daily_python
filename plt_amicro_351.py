import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# epoch,acc,loss,val_acc,val_loss
data = pd.read_excel(r"D:\Indoor Mapping\A-Micro\Test Result\SC351 accuracy test.xlsx", sheet_name='Sheet2',
                     engine='openpyxl')
# print(data['Issue'])
x_axis_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y_axis_data1 = data['Error'][0:10]
y_axis_data2 = data['Error'][10:20]
y_axis_data4 = data['Error'][20:30]

y_axis_data3 = [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
# print(y_axis_data3)
# 画图
plt.plot(x_axis_data, y_axis_data1, 'b*--', alpha=0.9, linewidth=1, label='Machine 1')  # '
plt.plot(x_axis_data, y_axis_data2, 'rs--', alpha=0.9, linewidth=1, label='Machine 2')
plt.plot(x_axis_data, y_axis_data3, 'go-', alpha=0.5, linewidth=2, label='acc')
plt.plot(x_axis_data, y_axis_data4, 'yo--', alpha=0.9, linewidth=1, label='Machine 3')

## 设置数据标签位置及大小
for a, b in zip(x_axis_data, y_axis_data1):
    plt.text(a, b, str(b), ha='center', va='bottom', fontsize=6)  # ha='center', va='top'
for a, b1 in zip(x_axis_data, y_axis_data2):
    plt.text(a, b1, str(b1), ha='center', va='bottom', fontsize=6)
for a, b2 in zip(x_axis_data, y_axis_data3):
    plt.text(a, b2, str(b2), ha='center', va='bottom', fontsize=6)
for a, b3 in zip(x_axis_data, y_axis_data4):
    plt.text(a, b3, str(b3), ha='center', va='bottom', fontsize=6)
plt.legend()  # 显示上面的label

plt.xlabel('Times')
plt.ylabel('Error')  # accuracy

# plt.ylim(-1,1)#仅设置y轴坐标范围
plt.show()
