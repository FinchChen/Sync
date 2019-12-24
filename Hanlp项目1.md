# Hanlp 项目1 - ~~java~~ Python!!!!!

## 1. 环境搭建

### java jdk1.8

https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

在官网勾选,然后登陆oracle账号,再下载相应版本,这里使用的是Windows.
直接安装即可,不用配置环境变量.

### maven 3.6.3

https://maven.apache.org/download.cgi

* 下载maven zip包,解压到没用中文的目录.
* 环境变量先添加 MAVEN_HOME: C:\Program Files\maven\apache-maven-3.6.3
* path里添加 %MAVEN_HOME%\bin
(win7用 ; 分开)
* 在maven的conf里修改原本的local repo目录
``` json
<localRepository>E:\maven\repo</localRepository>
```

* 修改阿里云的mirror
``` json
<mirror>
　　　<id>alimaven</id>
　　　<mirrorOf>central</mirrorOf>
　　　<name>aliyun maven</name>
　　　<url>http://maven.aliyun.com/nexus/content/groups/public/</url>
</mirror>
```

### pyhanlp

* 先装anaconda (略)
* conda prompt里：
> pip install pyhanlp

如果出错了可以参考[手动安装](https://github.com/hankcs/pyhanlp/wiki/%E6%89%8B%E5%8A%A8%E9%85%8D%E7%BD%AE)

对了还有依赖文件:
> pip install absl-py
pip install jpype1>=0.7.0

### java hanlp

可以使用maven:
``` json
<dependency>
    <groupId>com.hankcs</groupId>
    <artifactId>hanlp</artifactId>
    <version>portable-1.7.5</version>
</dependency>
```
我使用的是git整个repo然后用idea打开:
> git clone https://github.com/hankcs/HanLP.git

hanlp.properties和data这个暂时先不管，碰到了问题再说
至此环境搭建完毕

## 2.python: 文本分类

### 2.1 尝试跑通文本分类的demo
咦这个好像是在idea里用java跑的,贴一下大概的伪代码:
```
如果没有模型:
    调用一个NaiveBayse
    NB.train(语料库)
    保存model下次就能调用
如果有模型:
    直接调用NB.predict(text)
```
结果: text , class
```
《C罗获2018环球足球奖最佳球员 德尚荣膺最佳教练》 属于分类 【体育】
《英国造航母耗时8年仍未服役 被中国速度远远甩在身后》 属于分类 【军事】
《研究生考录模式亟待进一步专业化》 属于分类 【教育】
《如果真想用食物解压,建议可以食用燕麦》 属于分类 【健康】
《通用及其部分竞争对手目前正在考虑解决库存问题》 属于分类 【汽车】
```

## 3.python: 体育数据下的文本聚类

### 3.1 尝试文本聚类
因为在java下不好调试(也可能是我不会),**人生苦短我用python:**
(训练和调试用python,生成模型后部署在java这样应该可以)
新建一个jupyter notebook
``` python
from pyhanlp import *

ClusterAnalyzer = JClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
PATH = "E:/maven/Hanlp/data/test/搜狗文本分类语料库迷你版/体育1/"
#本来是体育文件夹,我做了个副本体育1

analyzer = ClusterAnalyzer()
```
这里创建了一个analyzer对象
``` python
tmp = !ls {PATH} #0001.txt .......
for i in tmp:
    with open(f'{PATH}'+i,'r', encoding='UTF-8') as f:        
        tmp = f.read()
        analyzer.addDocument(i[:4],tmp) # 取前四位做id
```
数据集有了,接下来是调用object
``` python
# rawresult = analyzer.kmeans(5)
# rawresult = analyzer.repeatedBisection(5)
rawresult = analyzer.repeatedBisection(1.0) #必须是float
```
第一种是kmeans聚类,第二种是加强版的kmeans-重复二分类聚类
一,二里面的参数是指定要分多少类
第三种的参数是由β=1.0来自动判断聚类个数
具体参考Hanlp书中 10.4.2 节
``` python
len(rawresult) # 128
listresult = str(rawresult[0]).strip('][').replace(" ","").split(',')
```
返回优化后的listresult: [0001,0002,0003,0004.......]
然后可以看看聚类里的都分了些什么:
``` python
for i in listresult:
    print ("*************************************************     \n"+i)
    print (open(f'{PATH}'+i+'.txt','r', encoding='UTF-8').read())
```



## 4.Hanlp书本知识结构

## 5.python: 关键词提取

## 6.python: 单词语义相似度

