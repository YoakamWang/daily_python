import xmind

w = xmind.load("test.xmind")
s1 = w.getPrimarySheet()  # 获取此工作表
s1.setTitle("first sheet")  # 设置标题
a = {"h1": 'Python 技术学习', 'h2': ['Python基础', 'Python 爬虫'],
     'h3': [['Python环境安装', 'Python基础语法', 'Python数据结构'], ['Python爬虫基础知识详解', 'Python爬虫相关模块详解']]}
r1 = s1.getRootTopic()  # 获取此工作表的根主题
r1.setTitle(a['h1'])  # 设置标题
c = a['h2']
c2 = a['h3']
for i, val in enumerate(c):
    print(i, val)
    a = 'b' + str(i)
    a = r1.addSubTopic()
    a.setTitle(val)  # 设置标题
    for i2, val2 in enumerate(c2):
        if i == i2:
            a2 = 'b2' + str(i)
            a2 = a.addSubTopic()
            #        if isinstance(val, list):
            for i3, val3 in enumerate(val2):
                a3 = 'b3' + str(i3)
                a3 = a2.addSubTopic()
                a3.setTitle(val3)

xmind.save(w, "Python_detail.xmind")
