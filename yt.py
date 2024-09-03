oledM = True
playback_speed = 3
 
from youtubesearchpython import VideosSearch
import os
from pytubefix import YouTube
 
import sys
from pathlib import Path
import av
import PIL
 
if oledM:
    from luma.core.interface.serial import i2c, spi, pcf8574
    from luma.core.interface.parallel import bitbang_6800
    from luma.core.render import canvas
    from luma.oled.device import ssd1306
    serial = i2c(port=0, address=0x3C)
    device = ssd1306(serial)
 
def playVideo():
    frameN = 1
    video_path = "videoYT.mp4"
    print(f'Loading ...')
    clip = av.open(video_path)
    for frame in clip.decode(video=0):
        frameN += 1
        if frameN % (playback_speed) == 0:
            img = frame.to_image()
            if img.width != device.width or img.height != device.height:
                # resize video to fit device
                size = device.width, device.height
                img = img.resize(size, PIL.Image.LANCZOS)
 
        device.display(img.convert(device.mode))
 
def donwload(link):
    yt = YouTube(link)
    print(f" Скачевается: {yt.title}")
    ys = yt.streams.get_highest_resolution()
    ys.download(filename="videoYT.mp4")
 
def screath(find,lim=10):
    ret = VideosSearch(find, limit = lim)
    return ret.result()
 
def prints(list): 
    print("------------------------------------------------------------------------")
    num = -1
    for res in list['result']:
        num += 1
        print(f"Номер: {num}")
        print(f"Название: {res['title']}     Длительность:{res['duration']}")
        print(f"Просмотры {res['viewCount']['short']}  Загрузка: {res['publishedTime']}")
        print(f"Канал: Название: {res['channel']['name']}")
        print(f"Ссылка: {res['link']}")
        print("------------------------------------------------------------------------")
 
if __name__ == "__main__":
    name = input("Название: ")
    if name == "__play__":
        playVideo()
        sys.exit()
    else:
        list =screath(name)
    prints(list)
    n = input("Номер: ")
    if n == "q":
        sys.exit()
    else:
        n = int(n)
        donwload(list['result'][n]['link'])
    if oledM:
        playVideo()
