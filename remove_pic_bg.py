# 安装库：pip install backgroundremover
# 执行命令 # backgroundremover -i "带背景照片" -o "去除背景照片"
# backgroundremover -i "cg.jpg" -o "cg_outopt.jpg"
# 初次执行要下载模型（大概170m）- u2net.pth 下载好的模型放在 c:/Windows/user/.u2net/u2net.pth
#Python方式调用：

# 导入库
import os
os.system('backgroundremover -i "cg.jpg" -o "cg_output.jpg"')

