## 本地工具

- 需要配置项：
    - ssh_config.py：根据实例添加远程服务器的配置，ip，port，username，password等。
    - settings.py：其他设置
    
- 安装依赖：
```bash
pip3 install paramiko cryptography==2.4.2
```

- 获取需要运行切片程序的服务器：
    ```bash
    python3 get_videos.py
    ```
    执行结束之后，会生成和ip地址对应的txt文件，会保存该服务器下需要切片的视频，以及会在`need_slice_server.txt`文件中保存该服务器地址。
- 远程启动切片程序
    ```bash
    python3 slice_video.py
    ```
    会读取`need_slice_server.txt`文件中的ip并发起切片指令。
    由于等待返回的话，执行切片程序时间较久，所以发出指令之后就会结束。
    然后会将`need_slice_server.txt`文件清空。
- 删除违规程序
    ```bash
    python3 delete_video.py
    ```
    将需要删除的视频名称添加到`violation.txt`中，一行一个视频。
    程序会读取该文件，然后同步到远程服务器，远程服务器启动删除程序。
    删除其中的视频，删除完毕之后服务器端会删除用来同步违规视频的文件。
    本地`violation.txt`中的视频列表目前是需要自己清空。


在我自己的服务器进行了简单的测试：

服务器文件情况：
```bash
[root@zhi video]# ls
input  keys  output  video_operate
[root@zhi video]# pwd
/root/video
[root@zhi video]# ls input/
1.mp4                                                                                   【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好5.mp4
【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好1.mp4  【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好6.mp4
【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好2.mp4  【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好7.mp4
【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好3.mp4  【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好8.mp4
【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好4.mp4  【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好.mp4
[root@zhi video]# ls keys/
[root@zhi video]# ls output/
[root@zhi video]# ls video_operate/
delete_videos.py  README.md  requirements.txt  sliceconfig.ini  slice.py  slice_video.py  src  video_count.py
```

本地文件情况：
```bash
[zhi@zhi-pc slice_tools]$ ls -la
-rw-r--r--  1 zhi zhi 1326  5月 25 19:29 delete_video.py
-rw-r--r--  1 zhi zhi 1719  5月 25 18:45 get_videos.py
-rw-r--r--  1 zhi zhi    0  5月 25 20:29 need_slice_server.txt
-rw-r--r--  1 zhi zhi 2722  5月 25 20:50 README.md
-rw-r--r--  1 zhi zhi 1045  5月 25 20:11 run_rclone.py
-rw-r--r--  1 zhi zhi  251  5月 25 20:06 settings.py
-rw-r--r--  1 zhi zhi 1150  5月 25 20:35 slice_video.py
-rw-r--r--  1 zhi zhi  621  5月 25 18:59 ssh_client.py
-rw-r--r--  1 zhi zhi  258  5月 25 20:28 ssh_config.py
-rw-r--r--  1 zhi zhi  971  5月 25 14:41 video_data.py
-rw-r--r--  1 zhi zhi  411  5月 25 19:33 violation.txt  #文件中有测试的违规视频
```

下面进行测试

1. 获取需要切片的服务器，找到大于限制的程序。
```bash
(slice_video)  # 我的虚拟环境
[zhi@zhi-pc slice_tools]$ python3 get_videos.py
连接39.105.152.226服务器
(slice_video) 
[zhi@zhi-pc slice_tools]$ ls -la
-rw-r--r--  1 zhi zhi  932  5月 25 20:59 39_105_152_226.txt  # 新建的文件，保存了该服务器需要进行切片的视频
-rw-r--r--  1 zhi zhi 1326  5月 25 19:29 delete_video.py
-rw-r--r--  1 zhi zhi 1716  5月 25 20:59 get_videos.py
-rw-r--r--  1 zhi zhi   60  5月 25 20:59 need_slice_server.txt  # 写如了需要切片的服务器，可自行调整
-rw-r--r--  1 zhi zhi 3685  5月 25 21:00 README.md
-rw-r--r--  1 zhi zhi 1045  5月 25 20:11 run_rclone.py
-rw-r--r--  1 zhi zhi  251  5月 25 20:06 settings.py
-rw-r--r--  1 zhi zhi 1150  5月 25 20:35 slice_video.py
-rw-r--r--  1 zhi zhi  621  5月 25 18:59 ssh_client.py
-rw-r--r--  1 zhi zhi  258  5月 25 20:28 ssh_config.py
-rw-r--r--  1 zhi zhi  971  5月 25 14:41 video_data.py
-rw-r--r--  1 zhi zhi  411  5月 25 19:33 violation.txt
```
2. 启动切片程序
```bash
(slice_video) 
[zhi@zhi-pc slice_tools]$ python3 slice_video.py
服务器39.105.152.226:执行切片命令已经发送
```
服务器文件情况
```bash
[root@zhi video]# ls keys/
0bde992b896bc6de904051cbc3118319.key      41bb55e5a29713e93e9713b4c900238b.key      6d537cb68bba4cfa39b819f78f84136a.key      8ebc478c0e113d4f3630843033c4e6b8.key      ab8d6ae5b0d2b2a19e1924c5b93fab8e.key
0bde992b896bc6de904051cbc3118319.keyinfo  41bb55e5a29713e93e9713b4c900238b.keyinfo  6d537cb68bba4cfa39b819f78f84136a.keyinfo  8ebc478c0e113d4f3630843033c4e6b8.keyinfo  ab8d6ae5b0d2b2a19e1924c5b93fab8e.keyinfo
2263812f19365600c35832e45ed089d9.key      6258224851468967934ac1735c0aa409.key      71376a8b2d3640948c0b6d3e22314135.key      a7ab771d626b211c001129b6e633f06d.key      ee340d727d22a95c72b59705db5d88bb.key
2263812f19365600c35832e45ed089d9.keyinfo  6258224851468967934ac1735c0aa409.keyinfo  71376a8b2d3640948c0b6d3e22314135.keyinfo  a7ab771d626b211c001129b6e633f06d.keyinfo  ee340d727d22a95c72b59705db5d88bb.keyinfo
[root@zhi video]# ls output/
169016b8ee77b23453d77be590e3bdb8  1f9745702a09dfec5054dbf3aa98e2f0  260b50c93c51614c7da95d678a2a3930  6ef856d8ca33a5b4b66223ee186d661d  bf9e1b7f34c8574f632f4b521de9249c
19ddb7607e231c8f912e7ba3943862a9  24f87298cb96cff0e4140d6dbcf82bce  36a49e97660a4848cdb8a25ee4ec6567  ab333fba6522309463176945a7848d93  fde0e8fa6442852f480289a0e0cf86f2
[root@zhi video]# ll input/
total 0
-rw-r--r-- 1 root root 0 May 25 21:04 1.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好1.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好2.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好3.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好4.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好5.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好6.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好7.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好8.mp4
-rw-r--r-- 1 root root 0 May 25 21:04 【MV】Camila Cabello -Never Be the Same - 高清MV在线播放 - 音悦Tai - 让娱乐更美好.mp4
```
3. 删除违规视频
```bash
(slice_video) 
[zhi@zhi-pc slice_tools]$ python3 delete_video.py
服务器39.105.152.226:删除命令已经发送
```
服务器`output`文件夹情况，未对input以及.key，.keyinfo进行删除。
```bash
[root@zhi video]# ls output/
1f9745702a09dfec5054dbf3aa98e2f0  24f87298cb96cff0e4140d6dbcf82bce  260b50c93c51614c7da95d678a2a3930  36a49e97660a4848cdb8a25ee4ec6567  6ef856d8ca33a5b4b66223ee186d661d  fde0e8fa6442852f480289a0e0cf86f2
```