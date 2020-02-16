# MongoDB, ElasticSearch, Nginx 学习笔记

## 1. MongoDB

客户端给服务器发出请求,服务器再向数据库查询数据,数据库返回查询结果,服务器返回操作.MongoDB就是一个**非关系型文档数据库**.

* SQL = 结构化查询语言(Structured Query Language)
* 关系型数据库中全是**表**,使用SQL来操作
* 非关系型数据库中全是键值

### 1.1简介

* MongoDB是为快速开发互联网Web应用而设计的数据库系统.
* MongoDB的设计目标是极简,灵活,作为Web应用栈的一部分.
* MongoDB的数据模型是面向文档的. 所谓文档是一种类似于JSON的结构.(BSON)

三个概念:
1. 数据库(database)
    * 数据库是仓库,仓库中可以存放集合
2. 集合(collection)
    * 集合类似于数组,集合中可以存放文档
3. 文档(document)
    * 文档是数据库中的最小单位,我们存储和操作的内容都是文档.

下载MongoDB:
*https://www.mongodb.com/download-center/community*
选择Community版本
(学习的话先用这个吧)

配置环境变量:
环境变量path中加入: *C:\Program Files\MongoDB\Server\4.2\bin*

创建数据库默认文件夹: *C:\data\db*

在cmd中输入**mongod**启动服务器服务

新开一个cmd输入**mongo**即可连接数据库, 出现>

mongod启动可带参数:
* --dbpath C:\mongo-data\db #指定db路径
* --port 1234 #指定端口

数据库(database):
* 数据库的服务器:
    * 用来保存数据
    * mongod来启动服务
* 数据库的客户端:
    * 用来操作服务器,对数据进行**增删查改**的操作
    * mongo来启动客户端

因为每次这样都要启动一遍太麻烦了
将MongoDB设置为系统服务,可以自动在后台启动,不用每次都手动启动

官网上说是安装过程中自动把它安装成了服务,但是我再service目录里没有看到MongoDB这个服务...
先不管了

### 1.2 进阶

MongoDB结构:
![mongodb1.png](https://i.loli.net/2020/02/13/junkpOUNbsqQ5GV.png)

基本指令:

* **show dbs / show databases** 
    * 列出现有的数据库
* **use test** 
    * 进入test数据库
    * 在MongoDB中不用初始化(创建)数据库/集合即可操作(自动创建)
    * 第一次插入文档的时候才生成
* **db**
    * 当前所处的数据库
* **show collections**
    * 查看现有的集合

CRUD操作:(增删改查)

具体操作查询[文档(墙外)](https://docs.mongodb.com/manual/crud/index.html)

* **db.\<collection_name\>.insert(doc)**
    * 向集合collection中插入一个文档
    * eg. 给test集合插入学生对象
    * db.student.insert({name:"sunwukong",age:18,gender:"male"})

* **db.\<collection_name\>.find()**
    * 查询当前集合中所有文档


### 1.3 图形化管理工具

下载一个[mongodbmanager](https://www.mongodbmanager.com/download)

安装之后默认连接,并打开它的小cmd按钮

F6 执行光标所在行代码
F9 执行选中的代码

或者使用[studio3T](https://studio3t.com/download/)

这个要好看一点

### 1.4 CRUD增删改查

#### 增加

以集合study为例:

* db.study.insert({name:"猪八戒",age:28,gender:"男"})
    * 插入单个对象

* db.study.insert([
    {name:"沙和尚",age:38,gender:"男"},
    {name:"白骨精",age:18,gender:"女"}
])

    * 插入多个对象

当我们向集合中插入文档时,如果没有给文档指定_id属性,则MongoDB会自动为文档添加_id属性来作为文档的唯一标识.

* **ObjectId()**
    * 命令可以生成标识

#### 查找

* db.study.find({age:38,gender:"男"})
    * 返回所有满足条件的文档(一个数组)

* db.study.findOne({age:28})
    * 返回的是第一个文档对象

* db.study.find().count()
    * 有多少个结果

#### 修改

* db.study.update(查询条件,新对象)
    * db.study.update({name:"猪八戒"},{age:100})
    * ↑ 这一条, 里面的内容会被age:100替换掉
    * 如果想要修改而不是替换,需要用**修改操作符**
    * **$set**可以用来替换
    * ↓
    ```sql
    db.study.update({name:"猪八戒"},
    {$set:{
        age:100,
        gender:"妖怪"
    }})
    ```
    * **$unset**用来删除指定属性
    * **匹配多个内容时update默认只改第一个,多个用updateMany()**

* db.study.replaceOne(查询条件,替换内容)

#### 删除

规则同上

* db.study.remove(匹配条件)
    * 默认会删掉多个
    * 必须要传参,如果是{}空参数,就会清空集合.
* db.study.deleteOne()
* db.study.deleteMany()
* db.study.drop()
    * 删除集合
* db.dropDatabase()
    * 删除数据库

**一般数据库中的数据都不会删除,所以删除的方法很少调用**

**一般会在数据中添加一个字段,来表示数据是否被删除:**

>isDel: 0 #没删除
>isDel: 1 #表示删除了


### 1.5 高级

**查询内嵌**
```sql
db.study.find({"hobby.movies":"hero"})
```

**[数组更新操作](https://docs.mongodb.com/manual/reference/operator/update-array/)**
```sql
$push //这个随意添加
$addToSet //重复则不添加
```

**循环**
```sql
for (var i=1 ; i<2000 ; i++){
    db.study.insert({num:i});
}
```
2000次insert操作很慢
```sql
var arr = [];
for (var i=1 ; i<2000 ; i++){
    arr.push({num:i});
}
db.study.insert(arr)
```

**值比较**
```sql
db.study.find({num:{$gt:500}}); // greater than
db.study.find({num:{$gt:40, $lt:50}}) // 传多个条件
```

* $eq =
* $gt >
* $lt <
* $gte >=
* $lte <=
* $ne !=


**分页**
```sql
db.study.find({num:{$gt:40}}).limit(10); // 最多显示10条
db.study.find({num:{$gt:40}}).skip(10).limit(20);
// 跳过前10条,显示11-20条
db.study.find({num:{$gt:40}}).limit(20).skip(10);
// limint,skip的位置MongoDB会帮你自动替换
```

### 1.6 文档之间的关系


* 一对一
    * 一般比较少, eg. 丈夫 - 妻子
    * 实现: 内嵌文档
* 一对多
    * eg. 父母 - 孩子, 用户 - 订单, 文章 - 评论
    * 父母可以有多个孩子,孩子只属于一对父母
    * 实现: 以id为索引
* 多对多
    * eg. 分类 - 商品
    * 一个分类可以有多个商品,一个商品可以有多个分类
    * 实现: 以数组为索引

### 1.7 暂时还没学的部分

* [sort和投影](https://www.bilibili.com/video/av49923533?p=14)
* mongoose
* schema和model
* document的方法
* mongoose的模块化

## 2 ElasticSearch

没有找到很新的教学视频,于是从官网上找了[中文的(墙外)](https://www.elastic.co/cn/webinars/getting-started-elasticsearch)Elasticsearch7教程来看看.

### 2.1 Elastic Stack 介绍

Elastic的应用范围非常广泛.
ElasticSearch有三大特点:
* 具备很好的横向拓展能力
* 毫秒级的性能,基于倒排索引
* 不需要知道数据库结构就可以查询,返回所有的相关结果

所以非常适合**在线实时搜索和分析**

Elastic技术栈:
![Elastic技术栈.png](https://i.loli.net/2020/02/14/OXz3luZGmFIy4xe.png)

* Kibana - 数据可视化
* Elasticsearch - 全文搜索
* Beats - 轻量级数据采集
* Logstash - 对数据先进行加工和处理



### 2.2 安装 Elasticsearch 和 Kibana

### 2.3 JSON 文档

### 2.4 CRUD操作

### 2.5 Mapping 和 Analyzers


## 3 Nginx

Nginx是一个高性能的HTTP和反向代理web服务器.

特点: 占用内存少,并发能力强,性能性能性能,支持热部署

有报告表明最高能承受5w并发连接.

### 3.1 基本概念

* **正向代理:**
    * 通过代理服务器访问外部网站, eg.代理ip, ssr

* **反向代理:**
    * 用户将请求发送到反向代理服务器,由反向代理服务器获取数据后再返回给客户端,此时暴露的是代理服务器的地址,隐藏了真实服务器IP地址

* **负载均衡:**
    * 单个服务器处理不了太多请求的情况下,负载均衡可以将请求分发到多个服务器上

* **动静分离**
    * 为了加快网站的解析速度,可以把动态页面和静态页面由不同的服务器来解析,加快解析速度,降低原来单个服务器的压力

### 3.2 安装以及常用命令


以centos为例:
```bash
sudo yum install yum-utils
# 依赖
sudo yum install nginx
```

```bash
nginx
# 启动nginx
nginx -v
# 查看nginx版本
nginx -h
# 查看nginx帮助
nginx -s reload
# 重新加载nginx
```

### 3.3 配置文件

nginx默认配置文件目录:
> /etc/nginx/nginx.conf

nginx配置文件由三部分组成:

**全局块:**

events块往上的部分

* 用户(组)
* worker process数
* 进程PID存放路径
* 日志存放路径和类型
* 配置文件的引入

**events块:**

events块涉及nginx服务器与用户的网络连接

eg.
* 是否开启对多work process下的网络连接进行序列化
* 是否允许同时接收多个网络连接
* 选取哪种事件驱动模型来处理连接请求
* 每个work process可以同时支持的最大连接数
* 等等

这部分的配置对nginx性能影响较大

**http块:**

配置nginx最频繁的部分,代理,缓存和日志定义等绝大多数功能和第三方模块的配置都在这里.

里边含有**http全局块**和**server块**

**http全局块**

包括了:
* 文件引入
* MIMIE-TYPE定义
* 日志自定义
* 连接超时时间
* 单链接请求数上限

**server块**

这部分和虚拟主机有关系.虚拟主机从用户的角度看,和一台独立的硬件主机是完全一样的,该技术的产生是为了节省互联网服务器的硬件成本.

每个http块可以包括多个server块,每个server块相当于一个虚拟主机

每个server块也分为全局server块,以及可以同时包含多个location块

**全局server块**

暂略

**location块**

[正则(视频结尾)]https://www.bilibili.com/video/av68136734?p=10

### 3.4 配置反向代理

第一个实例:
在server块中
1. 改server_name为本机ip
2. 在location块里面加入:
> proxy_pass 127.0.0.1:5000/upload
3. reload
> nginx -s reload

配置两个反向代理:
[略](https://www.bilibili.com/video/av68136734?p=10)

### 3.5 配置负载均衡

1. 在http块中加入upstream块:
```js
http {
    upstream myserver{
        server 127.0.0.1:3334   ;
        server 127.0.0.1:3335;
    }
}
```

2. server块中
```js
server_name 自己的ip;
```

3. location块中新加:
```js
proxy_pass http://myserver;
```


### 3.6 配置动静分离

暂略,用不到

[传送门](https://www.bilibili.com/video/av68136734?p=12)

自己查一下location里的expire



### 3.7 配置高可用集群

当nginx宕机之后怎么办?

![nginx高可用1.png](https://i.loli.net/2020/02/15/zm3y8IgWRiOHFTD.png)

### 3.8 nginx原理

[传送门](https://www.bilibili.com/video/av68136734?p=17)

1. master 和 worker
    * maseter进程接到任务,分发给不同的worker进程
2. worker如何进行工作
    * worker**争抢**(不是轮询)新的client任务
3. 一个master和多个worker的好处
    * reload热部署时,不影响正在进行的任务
    * 对于每个worker来说进程是独立的,不需要加锁,也保证了服务不会中断
4. 设置多少个worker
    * nginx采用了I/O多路复用机制,通过异步非阻塞方式来处理请求.每个worker的线程可以把一个cpu的性能发挥到极致,**所以worker数和服务器的cpu数相等是最为合适的**.设置少了会浪费cpu,多了会造成cpu频繁切换上下文带来的损耗.
5. **worker_connection连接数**
    * 问题1: 发送一个请求,占用了worker的几个连接数?
    * 答案: 2或者4个.
    * 普通的静态请求:2个连接
    * HTTP反代:4个连接
    * 
    * 问题2: nginx有一个master,有四个worker,每个worker支持最大的连接数是1024,那么支持的最大并发数是多少?
    * 答案: 普通静态访问:1*4*1024 / 2
    * 答案: HTTP反向代理: 1*4*1024 / 4, 每个反代占4个连接数.