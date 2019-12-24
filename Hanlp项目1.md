# Hanlp 项目1 - java

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




## 3.python: 体育数据下的文本聚类

## 4.Hanlp书本知识结构

## 5.python: 关键词提取

## 6.python: 单词语义相似度

