# 视频切片程序

一个多线程的，批量将MP4格式的视频使用FFmpeg进行切片，转为M3U8格式的视频。

## 已经实现的功能

- [x] 转码之后文件名加密
- [x] 对转换的M3U8进行加密
- [x] 根据配置选择对源文件夹中文件大小符合配置范围的视频进行切片
- [x] 保存切片日志，将切片结果保存入MySQL数据库中

## TODO

- [ ] 修改配置逻辑，能更灵活的配置程序

## 注意

**程序依赖于FFmpeg，必须安装FFmpeg才可以执行**

安装Python依赖
```bash
pip3 install -r requirements.txt
```
