# 第一节 Python基础内容回顾

## 一、课前准备

慢慢培养自己解决问题的能力。

要学会见招拆招。

关于憋代码这个事，要憋，一定要憋，让你憋主要有两个原因：

1. 简单的语法使用错误，不憋记不住。
2. 复杂的程序逻辑，不憋培养不出来独立的思考能力。
3. 一定要有独立解决问题的能力。

## 二、必须掌握的Python基础

### 1、基础语法相关

1. if条件判断

```python
if 条件:
	# 事情1
else:
	# 事情2
```

做条件判断用。程序里需要条件判断，就用它。

情况一，数据里有一些我们不需要的内容

```python
# 伪代码，理解含义（思路）
if data里有你不需要的数据:
	再见
else
 	保留 
```

情况二，页面结构不统一，会有两种页面结构

```python
# 伪代码，理解含义（思路）
提取器1 = xxxx  # 用来提取页面中内容的
提取器2 = xxxx

# 页面有可能是不规则的
结果1 = 提取器1.提取（页面）
if 结果1:
  有结果.存起来
else:
  没有结果
  结果2 = 提取器2.提取（页面）
```

2. while循环

```python
while 条件:
	循环体
```

如果条件为真，就执行循环体，然后再次判断条件，知道条件为假，循环结束。

循环体是反复执行的一段代码。

3. 关于True和False
   True是真的意思。

   False是假的意思。

下面需要记住：

```python
# 几乎所有能表示空的东西，都可以认为是False
print(bool(0))
print(bool(''))
print(bool([]))
print(bool({}))
print(bool(set()))
print(bool(tuple()))
print(bool(None))
# 上面全是False，相反的都是真。利用这个特性，我们可以有以下的一些写法：
# 伪代码
结果 = 提取器.提取（页面）
if 结果:
  有结果.我要保存结果
else:
  没结果...
```

### 2、字符串（必须会的，而且要熟练掌握）

字符串本身不可变，所以的操作都是返回一个新的字符串。

字符串在**爬虫**里必须知道的几个操作：

1. 索引和切片

   索引，就是第几个字符，它从0开始

   切片，从字符串中提取n个字符

```python
s = '我爱黎明，黎明爱我'
print(s[1])
print(s[0])

print(s[2: 4])  # 从第2个，到第4个（第4个取不到）
```

2. strip()

   可以去掉字符串**左右两端**的空白（空白，换行\n，回车\r，制表符\t）

```python
s = '   \t\t\t我的天啊\r\r   \n\n  '  # 带各种空格和换行的字符串
s1 = s.strip()
print(s1)
```

3. split()

   做切割的。

```python
s = '10,男人本色,100000万'  # 在网页上提取到这样的一段数据，现在我需要电影名称
tmps = s.split(',')
name = tmps[1]
print(name)  # 男人本色

id, name, money = s.split(',')  # 切割后，把三个结果直接给三个变量
print(id)
print(name)
print(money)
```

4. replace()

   字符串替换

```python
s = '我    \t\t\n\n爱  黎  明  '  # 这是从网页上拿到的东西
s1 = s.replace(' ', '').replace('\t', '').replace('\n', '')  # 干掉空格，\t \n
print(s1)  # 我爱黎明
```

5. join()

   将列表拼接为字符串

```python
lst = ['我', '喜欢', '黎明']
s1 = ''.join(lst)  # 用空字符串把lst中的每一项拼接起来
print(s1)  # 我喜欢黎明

lst2 = ['\n\r', '\n\r', '周杰伦\n\r', '\n不认识我\r']
s2 = ''.join(lst2).replace('\n', '').replace('\r', '')
print(s2)  # 周杰伦不认识我
```

6. f-string

   格式化字符串的一种方案

```python
s = '周杰伦'
s1 = f'我喜欢{s}'  # 它会把一个变量塞入一个字符串
print(s1)  # 我喜欢周杰伦

k = 10085
s2 = f'我的电话是{k+1}'  # 它会把计算结果塞入一个字符串
print(s2)  # 我的电话号是10086
# 综上，f-string的大括号里，其实是一段表达式，能计算出结果
```

### 3、列表

列表，仅次于字符串的一种数据类型，它主要是能承载大量的数据。理论上内存不炸，它就能一直存在。

1. 索引，切片
   列表的索引和切片逻辑与字符串完全一致

```python
lst = ['赵本山', '王大陆', '大嘴猴', '马后炮']
item1 = lst[2]  # 大嘴猴
item2 = lst[1]  # 王大陆

lst2 = lst[2:]
print(lst2)  # ['大嘴猴', '马后炮']

# 注意，如果列表中没有数据，取0会报错
lst = []
print(lst[0])  # 报错，Index out of bounds

# 注意，如果给出的索引下标超过了列表的最大索引，依然会报错。
lst = ['123', '456']
print(lst[3])  # 报错，Index out of bounds
```

2. 增加
   给列表添加数据

```python
lst = [11, 22]
lst.append(33)
lst.append(44)
print(lst)  # [11, 22, 33, 44]
```

3. 删除
   删除数据（不常用）

```python
lst.remove('周润发')  # 把周润发删除
```

4. 修改

```python
lst = ['赵本山', '王大陆', '大嘴猴', '马后炮']
lst[1] = '周杰伦'
print(lst)  # ['赵本山', '周杰伦', '大嘴猴', '马后炮']
```

5. range

   用for循环数数的一个东西

```python
for i in range(10):
  print(i)  # 从0数到9
  
for i in range(5, 10):
  print(i)  # 从5数到9
```

6. 查询（必会）

```python
lst = ['赵本山', '周杰伦', '大嘴猴', '马后炮']
print(lst[0])
print(lst[1])
print(lst[2])
print(lst[3])

# 循环列表的索引
for i in range(len(lst)):
  print(lst[i])

# 循环列表的内容
for item in lst:
  print(item)
  
# enumerate
lst = [11, 22, 33, 44, 55]
# 得到的一个是元组 (index, item)
for i, item in enumerate(lst):
  print(i, item)
```

### 4、字典

字典可以成对保存数据。

想要从字典中拿到value，必须有key。

1. 增加

```python
dic = {}
dic['name'] = '周杰伦'
dic['age'] = 18
print(dic)  # {'name': '周杰伦', "age": 18}
```

2. 修改

```python
dic = {'name': '周杰伦', "age": 18}
dic['age'] = 19
print(dic)  # {'name': '周杰伦', "age": 19}
```

3. 删除（不常用）

```python
dic = {'name': '周杰伦', "age": 18}
dic.pop('age')
print(dic)  # {'name': '周杰伦'}
```

4. 查询（重点）

```python
dic = {'name': '周杰伦', "age": 18}

a = dic['name']  # 查询'name'的值
print(a)

b = dic['age']  # 拿到dic中age对应的值
print(b)

c = dic['add']  # 没有'add'，报错
d = dic.get('add')  # 没有'add'，不报错，返回None。9
 
```

5. while循环和for循环

   while循环一般不计数使用，for循环技术更容易。

   continue：停止本次循环。

   break：终止循环。

```python
dic = {'name': '周杰伦', 'age': 18}
for k in dic:  # 循环出所有的key
  print(k)
  print(dic[k])  # 获取到所有的value并打印
```

6. 嵌套

```python
dic = {
  'name': '汪峰',
  'age': 18,
  'wife': {
    'name': '章子怡',
    'age': 19,
  },
  'children': [
    {'name': '汪一峰', 'age': 18},
    {'name': '汪二峰', 'age': 19},
    {'name': '汪三峰', 'age': 20}
  ]
  
}

# 汪峰的第二个孩子的名字
print(dic['childern'][1]['name'])

# 汪峰所有孩子的名称和姓名
for item in dic['children']:
  print(item['name'])
  print(item['age'])
```

### 5、字符集和bytes

字符集，记住两个字符集就够了，一个是utf-8，一个是gbk。都是支持中文的。但是utf-8的编码数量远大于gbk，我们平时使用最多的事utf-8。

```python
bs = '我的天啊abcd'.encode('utf-8')
print(bs)
# 一个中文在utf-8中是三个字节，一个英文是一个字节，所以英文字母是正常显示的。

# 把字节还原回字符串
bs = b'\xe6\x88\x91\xe7\x9a\x84\xe5\xa4\xa9\xe5\x93\xaaabcdef'
s = bs.decode('utf-8')
print(s)
```

bytes不是给人看的，是给机器看的，我们遇到的所有文字、图片、音频、视频，所有东西到了计算机里都是字节。

### 6、文件操作

Python中，想要处理一个文件，必须使用open()先打开一个文件。

```python
f = open('文件名', mode='模式', encoding='文件编码')
f.read() | f.write()
f.close()
```

模式：主要有4种，分别是：r、w、a、b

1. r：只读模式。含义是：当前这一次open的目的是读取数据。只能读，不能写。
2. w：只写模式。含义是：当前这一次open的目的是写入数据。只能写，不能读。
3. a：追加模式。含义是：当前这一次open的目的是向后面追加。只能写，不能读。
4. b：字节模式。可以和上面三种模式进行混合搭配，目的是写入的内容或读取的内容是字节。

encoding：文件编码，处理的文件是文本的时候才能使用。

另一种写法：

```python
with open('文件名', mode='模式', encoding='文件编码') as f:
  pass
```

这种写法的好处是，不需要我们手动关闭`f`。

### 7、关于函数

代码量很少的时候，我们并不需要函数。但是一旦代码量大了，一次要写几百行代码，调试起来就变得很困难，此时，就更建议把程序改写成一个一个具有特定功能的函数。方便调试，也方便代码重用。

```python
def 函数名(参数):
  # 函数体
  return 返回值

#调用函数
函数名（参数）
```

### 8、关于模块

模块是已经有人帮我们写好的一些代码，这些代码被保存在一个py的文件里，我们可以拿来直接用。

在Python中有三种模块。

1. Python内置模块
   不用安装，直接导入就能用

2. 第三方模块
   需要安装，安装后导入使用

3. 自定义模块
   直接导入使用

导入模块的语法：

```python
import 模块
from 模块 import 功能
from 模块.子模块 import 功能
```

爬虫一般会用到的模块：

1. time模块

```python
import time
time.time()  # 这个是获取到时间戳
time.sleep(10)  # 让程序睡眠10秒
```

2. os模块

```python
import os
# 判断文件是否存在
os.path.exists()  # 判断文件或文件夹是否存在
os.path.join()  # 文件路径拼接
os.makedirs()  # 创建文件夹
```

3. json模块（重中之重）

   现在的网站习惯性用json传递数据。

   json是一种类似字典一样的东西。对Python而言，json是字符串。

```python
# json字符串 转成 Python字典
import json
s = "{'name': 'jay', 'age': 18}"
dic = json.loads(s)
print(type(dic))
```

```python
# Python字典 转成 json字符串
import json
dic = {'name': 'jay', 'age': 18}
s = json.dumps(dic)
print(type(s))
```

4. random模块

   生成随机数

```python
import random
i = random.randint(1, 10)  # 1-10随机数
print(i)
```

5. 异常处理（重中之重）

```python
try:  # 尝试
  print('假如发生了异常')
  print('1/0')
except Exception as e:  # 程序出现问题，会从这里走
  print(e)  # 打印出现的问题

  print('不论上面是否又问题，这里依然可以正常执行')
```

程序执行的时候，如果`try`中的代码出现错误，自动跳到`except`中，执行`except`中的代码，然后程序继续往下执行。如果`try`中的代码没有出现错误，会跳过`except`，继续往下执行。

```python
# 一般的代码逻辑
import time
for i in range(10):
  try:
    发送请求，获取网上数据
    print('获取成功')
    break  # 成功了，就跳出循环
  except Exception as e:
    print('失败了，走这里')
    time.sleep(i*10)  # 睡眠一下继续获取数据
```

