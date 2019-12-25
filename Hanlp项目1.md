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
    语料库.分词() # 可选Hanlp分词,二元语法分词,自定义分词
    语料库.卡方检测提取主要特征()
    调用一个NaiveBayse # 或SVM
    NB.train(语料库)
    保存model下次就能调用
如果有模型:
    直接调用NB.predict(text)
```
结果: text , class
```
模式:训练集
文本编码:UTF-8
根目录:E:\maven\HanLP\data\test\搜狗文本分类语料库迷你版
加载中...
[体育]...100.00% 1000 篇文档
[健康]...100.00% 1000 篇文档
[军事]...100.00% 1000 篇文档
[教育]...100.00% 1000 篇文档
[汽车]...100.00% 1000 篇文档
耗时 13467 ms 加载了 5 个类目,共 5000 篇文档
原始数据集大小:5000
使用卡方检测选择特征中...耗时 124 ms,选中特征数:21436 / 102311 = 20.95%
贝叶斯统计结束
《C罗获2018环球足球奖最佳球员 德尚荣膺最佳教练》 属于分类 【体育】
《英国造航母耗时8年仍未服役 被中国速度远远甩在身后》 属于分类 【军事】
《研究生考录模式亟待进一步专业化》 属于分类 【教育】
《如果真想用食物解压,建议可以食用燕麦》 属于分类 【健康】
《通用及其部分竞争对手目前正在考虑解决库存问题》 属于分类 【汽车】
```

## 3.python: 体育数据下的文本聚类

### 3.1 尝试跑通文本聚类
因为在java下不好调试(也可能是我不会),**人生苦短我用python:**
(训练和调试用python,生成模型后部署在java这样应该可以)
``` python
from pyhanlp import *
ClusterAnalyzer = JClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
PATH2 = "E:/anaconda/Lib/site-packages/pyhanlp/static/data/test/搜狗文本分类语料库迷你版"
```
``` python
for algorithm in "kmeans", "repeated bisection":
    %time print ("%s F1=%.2f\n" % (algorithm , ClusterAnalyzer.evaluate(f'{PATH2}',algorithm) * 100))
```
得到结果:
```
kmeans F1=73.99
Wall time: 35.5 s

repeated bisection F1=66.49
Wall time: 59.5 s
```
惊呆了,这跟书上写的完全不一样啊
多试几次之后最好的结果是:
```
kmeans F1=82.27
Wall time: 1min 30s

repeated bisection F1=78.06
Wall time: 1min 15s
```
这样的话也算是勉强接近了书中的(kmeans,83.74),(repeatedBisection,85.58)了
重复二分聚类是会比kmeans快一些,但是**成绩波动大**,需要多运行几次.但是这样的问题是在实际部署中你不知道F1的成绩.
运行中我发现python只是调用了Java的class,如果要做修改还是要修改java源码
所以最好的方法应该是找到java类似jupyter notebook这样方便调试的ide(想想都不可能啊)


### 3.2 将三种方法应用到<体育>

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
由于没有训练测试集,暂时无法得知第三种方法的F1有多少
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
咦我发现有几个文件是一摸一样的
所以聚类可以很容易的分出他们
那么将重复的都删掉,再运行的话可能会分出更准确的聚类
``` python
import os
for i in listresult[:-1]:
    print (f'{PATH}'+i+'.txt')
    os.remove(f'{PATH}'+i+'.txt')
```
``` python
rawresult:128   ->   rawresult:113
```
自动分出来113个聚类,我觉得可以用提取几个关键词的方法来确定聚类的类别,详见第五节
## 4.Hanlp书本知识结构
1. 概述,简介,语料库,Trie树结构
2. 分词:
    1. 词典分词
    2. 二元语法分词
    3. 隐马尔科夫模型
    4. 感知机
    5. 条件随机场
3. 进阶:
    1. 词性标注
    2. 命名实体识别
    3. 信息抽取
    4. 文本聚类
    5. 文本分类
    6. 句法分析
4. 漫谈深度学习

* Hanlp设计了一种非常迅速高效的数据结构
* 从分词开始一步一步介绍中文分词技术的发展,接着从序列标注的方法延伸到具体的进阶应用
* 我们可以发现,Hanlp关注的更多是传统机器学习的方法以及兼顾学界的精准与工业界的部署效率.
* 本书的最后提到,传统机器学习有其局限性(像XOR),所以想要获得更好的结果需要继续研究深度学习的实现方法.

## 5.python: 关键词提取
open文件的方法有点难写,就集成了一个func:
``` python
def getStrFromTxt(path1):
    tmp = ""
    with open(path1,'r', encoding='UTF-8') as f:        
        tmp = f.read()
    return tmp
```
这里接之前写好的listresult.
``` python
TermFrequency = JClass('com.hankcs.hanlp.corpus.occurrence.TermFrequency')
TermFrequencyCounter = JClass('com.hankcs.hanlp.mining.word.TermFrequencyCounter')

counter = TermFrequencyCounter()
for i in listresult:
    counter.add(getStrFromTxt(f'{PATH}'+i+'.txt'))

print (counter.top(10))
```
> [林丹=283, 中国队=279, 比赛=156, 中=149, 鲍春来=119, 决赛=118, 局=108, 李永波=84, 对手=82, 比分=80]

单看这个我们可以把分出来的这类取名叫<林丹>
再看看每个文件的:
``` python
for i in listresult:
    print(TermFrequencyCounter.getKeywordList(getStrFromTxt(f'{PATH}'+i+'.txt'),10))
``` 
这里用的是词频统计,还可以使用TF-IDF或TextRank
```
[中国队, 中国, 羽坛, 方面, 实力, 杯赛, 显然, 大赛, 中国羽毛球, 高手]
[林丹, 汤杯, 中国队, 盖德, 击败, 决赛, 东京, 鲍春来, 丹麦队, 中国男队]
[中国队, 林丹, 昨天, 比赛, 盖德, 前, 优势, 中国, 鲍春来, 赢]
[说, 中国队, 李永波, 运动员, 相信, 无法, 希望, 场上, 国际羽联, 只能]
[鲍春来, 领先, 比分, 局, 休息, 中国队, 选手, 进入, 乔纳森, 丹麦]
[中国队, 林丹, 李永波, 决赛, 丹麦队, 汤杯, 冠军, 鲍春来, 说, 夺冠]
[领先, 比分, 局, 鲍春来, 蔡赟, 林丹, 付海峰, 对手, 休息, 丹麦]
[中国队, 比赛, 中, 夺冠, 中国女队, 表现, 蒋燕皎, 目前, 杯赛, 杜婧]
[林丹, 儿子, 记者, 脚伤, 出战, 表示, 盖德, 父母, 汤姆斯杯, 打响]
[林丹, 盖德, 比赛, 鲍春来, 调整, 表示, 胜利, 汤姆斯杯, 打得, 战胜]
[林丹, 鲍春来, 中国队, 陶菲克, 比赛, 决赛, 付海峰, 中, 防守, 蔡]
[林丹, 皮特, 比赛, 说, 中, 非常, 决赛, 表现, 节奏, 皮特·盖德]
[林丹, 李永波, 心里, 说, 踏实, 没有, 比赛, 开局, 连得, 赢]
[李永波, 林丹, 说, 中国队, 队员, 比赛, 更, 希望, 领先, 需要]
[林丹, 陶菲克, 比赛, 平, 中, 球, 决赛, 比分, 中午, 骥]
[林丹, 加油, 谢杏芳, 盖德, 观众, 胜利, 看台, 男友, 球迷, 比赛]
[组, 中国队, 预选赛, 获得, 球队, 法国队, 战胜, 中, B, A]
[林丹, 领先, 比分, 局, 得分, 对手, 进入, 丹麦, 中国队, 皮特·盖德]
[盖德, 林丹, 前, 中国队, 网, 对手, 汤杯, 擒, 控制, 局]
[中国队, 法国队, 组, 射门, 预选赛, 获得, 禁区, 球队, Ｂ, Ａ]
[说, 中国队, 李永波, 运动员, 相信, 无法, 希望, 场上, 国际羽联, 只能]
[丹麦, 老将, 汤杯, 机会, 最后, 明天, 已经, 中国, 中国队, 老队员]
[中, 比赛, 决赛, 实力, 中国队, 中国, 鲍春来, 男双, 汤杯, 林丹]
[林丹, 球, 比赛, 赛后, 说, 节奏, 之后, 中, 高手, 陶菲克]
[中国队, 林丹, 丹麦, 比赛, 中国, 鲍春来, 决赛, 领先, 蔡赟, 胜]
[林丹, 中国队, 盖德, 汤姆斯杯, 中国, 成功, 卫冕, 决赛, 冠军, 中]
[比分, 比赛, 局, 黄牌, 马来西亚队, 伦加德, 陈重名, 红牌, 没有, 最高]
[丹麦队, 决赛, 中国队, 表示, 表现, 水平, 昨天, 出, 鲍春来, 队员]
[林丹, 中国队, 李永波, 前, 盖德, 没有, 比赛, 说道, 胜利, 网]
[林丹, 中, 陶菲克, 印尼队, 中国队, 马来西亚队, 碰到, 团体赛, 半决赛, 决赛]
[中国队, 丹麦队, 双打, 单打, 中, 决赛, 鲍春来, 比赛, 半决赛, 林丹]
[中国队, 优势, 中国, 没有, 也许, 适应, 过程, 起来, 赶上, 赛制]
[比赛, 中, 陶菲克, 林丹, 印尼男队, 鲍春来, 中国男队, 赛后, 局, 今天]
[队员, 更多, 更, 能够, 李永波, 汤姆斯杯, 打出, 需要, 气势, 比赛]
[陈宏, 中, 称, 李永波, 未, 上场, 选手, 记者, 观众, 致意]
[中国队, 比赛, 中, 鲍春来, 林丹, 对手, 局, 最终, 成功, 出场]
[李永波, 没有, 鲍春来, 比赛, 中国队, 中, 已经, 决赛, 冠军, 队员]
[中国队, 决赛, 队员, 状态, 林丹, 李永波, 本报讯, 打出, 叶倩文, 印尼队]
[印尼, 林丹, 中国队, 陶菲克, 中, 决赛, 世锦赛, 选手, 避开, 逐鹿]
[晶报, 林丹, 中国队, 今天, 说, 集体, 评价, 胜利, 盖德, 没有]
[蔡赟, 付海峰, 比分, 局, 领先, 组合, 平, 休息, 丹麦, 进入]
```
可以看到虽然林丹的文本虽然占了一半,但还是有很多不是羽毛球的被分了进来
准确率大概只有70%
(然后又尝试了二元短语提取和关键句提取,效果并不理想)
之后再回到聚类上面去研究算法

## 6.python: 单词语义相似度
参考书13.3.4节
看书的过程中,我对word2vec做的单词语义相似度有点感兴趣,实现了一下
``` python
from pyhanlp import *
from tests.book.ch03.msr import msr_train
from tests.test_utility import test_data_path

IOUtil = JClass('com.hankcs.hanlp.corpus.io.IOUtil')
DocVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
Word2VecTrainer = JClass('com.hankcs.hanlp.mining.word2vec.Word2VecTrainer')
WordVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.WordVectorModel')

# 演示词向量的训练与应用
TRAIN_FILE_NAME = msr_train
MODEL_FILE_NAME = os.path.join(test_data_path(), "word2vec.txt")
```
没有模型的话会自动下载一个icwb2-data作为语料库,大概50MB
``` python
def train_or_load_model():
    if not IOUtil.isFileExisted(MODEL_FILE_NAME):
        if not IOUtil.isFileExisted(TRAIN_FILE_NAME):
            raise RuntimeError("语料不存在，请阅读文档了解语料获取与格式：https://github.com/hankcs/HanLP/wiki/word2vec")
        trainerBuilder = Word2VecTrainer()
        return trainerBuilder.train(TRAIN_FILE_NAME, MODEL_FILE_NAME)
    return load_model()

def print_nearest(word, model):
    print(
        "\n                                                Word     "
        "Cosine\n------------------------------------------------------------------------")
    for entry in model.nearest(word):
        print("%50s\t\t%f" % (entry.getKey(), entry.getValue()))
```
抄了两个function
``` python
wordVectorModel = train_or_load_model()
print_nearest("袜子", wordVectorModel)
```
得到和"袜子"最接近的词语:
```
                                                Word             Cosine
------------------------------------------------------------------------
                                                 摘		0.692532
                                                 掉		0.552828
                                                甩掉		0.510651
                                               王登龙		0.439798
                                                 砸		0.435302
                                                 烂		0.425343
                                                竟然		0.422790
                                                公社		0.416469
                                                吃喝		0.411804
                                               胡卫红		0.401735
```
这都是什么啊哈哈哈哈哈哈哈...感觉是因为测试用的语料库太少了
深度学习的word2vec的话肯定是数据越多准确率越高的
书中推荐爬取wikipedia做成语料库
留着以后实现吧