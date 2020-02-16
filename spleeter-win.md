# Spleeter 在win10下的实现

## 1. 安装Anaconda

## 2. Spleeter
1. 配置虚拟环境
``` bash
conda create -n spleeter
activate spleeter
#deactivate spleeter
```
2. 通过conda-forge安装ffmpeg
``` bash
conda config --add channels conda-forge
conda install ffmpeg
```
官方源慢的要死于是使用清华源:
``` bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```
3. Spleeter
``` bash
pip install spleeter
```
> 'pip' 不是内部或外部命令，也不是可运行的程序或批处理文件。

什么鬼...新环境里没有python于是就装一个:
``` bash
conda install pip
```
然后加个速:
``` bash
pip install spleeter -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
等了20多分钟应该装好了 试一下

......直接用会卡死,预下载一下模型(建议代理)

> https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems-finetune.tar.gz

解压然后放入 工作目录/pretrained_models/2stems

``` bash
spleeter separate -i C:/spleeter/"刘德华 - 中国人.flac" -p spleeter:5stems -o C:/spleeter/output
```
nice 能用了


## 3. 直接python实现
直接从源码上手.
1. 源码中第一步是建一个parser使得spleeter可以在命令行中使用和传递参数,我们直接跳过这一步,先实现separate参数的源码:

``` python
"""
    Entrypoint provider for performing source separation.

    USAGE: python -m spleeter separate \
        -p /path/to/params \
        -i inputfile1 inputfile2 ... inputfilen
        -o /path/to/output/dir \
        -i /path/to/audio1.wav /path/to/audio2.mp3
"""

from multiprocessing import Pool
from os.path import isabs, join, split, splitext
from tempfile import gettempdir

# pylint: disable=import-error
import tensorflow as tf
import numpy as np
# pylint: enable=import-error
```

会报错找不到tensorflow, 是因为jupyter notebook使用的是主环境的库, 于是在虚拟环境中再装一个jupyter notebook.

``` bash
pip install jupyter notebook -i https://pypi.tuna.tsinghua.edu.cn/simple/
```








