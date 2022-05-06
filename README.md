# python 多线程tx课堂下载器

## 介绍

​	一款下载tx课堂视频的程序，支持多种登录方式，可下载付费或免费视频（前提已购买订阅）

本项目的初衷是想将视频下载在本地，便于观看。欢迎大家学习交流。

一切以学习为目的，勿非法传播，如有侵权，联系删除。

## 文件内容：

tx课堂下载器：

​	存放视频文件夹（默认存放在此，也可根据源码更改）

​	download.py

​    ffmpeg.exe

​	requirements.txt

## 使用方法

若电脑有相应第三方库，可直接运行download.py程序

若无，可先在本文件夹创建虚拟空间

```
cd 文件夹
python -m venv 虚拟环境名称
虚拟环境名称\scripts\activate
pip install -Ur requirements.txt
python qcourse.py
```

运行后，按照相应的提示，填入相应的值，便可下载课程完整视频到本地
## 注意
直接使用exe程序，请先安装好edge浏览器，因为本程序调用的是edge浏览器
如果有能力自己调用python运行的，自己修改代码选择浏览器就好。
## 功能

- 模拟登录，获取cookies（支持wx登录和qq登录）
- 下载整个课程
- 视频下载后自动转换为`mp4`格式

## 感谢

​	本项目得到了很多大佬的帮助，在视频下载方面，使用了hecoter大佬的 m3u8download-hecoter的第三方库，文档编辑参考了qcourse_scripts项目，感谢各位大佬的帮助和支持
