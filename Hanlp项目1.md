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
