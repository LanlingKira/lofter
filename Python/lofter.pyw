#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from tkinter import *
import requests
import re
import os
import threading

root = Tk()
root.title('Lofter一键下载')
root.resizable(False, False)


def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)


center_window(root, 580, 75)

print('Lofter一键下载')
#下载目录
download = 'download'
state = True

htmlHeaders = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}


#获取内容
def getHtml(url):
    html = requests.get(url, headers=htmlHeaders, timeout=60)
    html.encoding = 'utf-8'
    return html.text


#获取图片
def getImg(html):
    reg = r'bigimgsrc=\"(.*?)\.(jpg|png|jpeg|gif)'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    return imglist


#获取目录
def getTitle(url):
    reg = r'post\/(.*)'
    titlere = re.compile(reg)
    title = re.findall(titlere, url)
    return title


#创建目录
def mkdir(path):
    path = path.strip()
    path = path.rstrip('\\')
    isExists = os.path.exists(download + '\\' + path)
    if not isExists:
        os.makedirs(download + '\\' + path)
        print('目录创建成功 -> [' + path + ']')
        s.set('目录创建成功 -> [' + path + ']')
        return True
    else:
        print('目录已存在 -> [' + path + ']')
        s.set('目录已存在 -> [' + path + ']')
        return False


def MyThread(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()


s = StringVar()
l = StringVar()
l.set('请输入图片下载地址: ')
Label(root, textvariable=l, font=('SimHei', 12)).place(x=5, y=8, anchor='nw')
ee = StringVar()
Entry(root, textvariable=ee, width=50).place(x=170, y=8)


def isUrl():
    global state
    log = ''
    imgLink = ee.get()
    log = imgLink + '\n'
    imgHeaders = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': imgLink,
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    reg = r'http(.*?)\.lofter\.com\/post\/(.*)'
    urlre = re.compile(reg)
    link = re.findall(urlre, imgLink)
    if state and len(link) > 0:
        state = False
        print('获取内容中...')
        s.set('获取内容中...')
        l.set('请输入图片下载地址: ')
        b.set('等待')
        htmlContent = getHtml(imgLink)
        print('解析内容中...')
        s.set('解析内容中...')
        imgList = getImg(htmlContent)
        if len(imgList) == 0:
            l.set('请重新输入下载地址: ')
            print('未解析到图片')
            s.set('未解析到图片')
            b.set('下载')
            state = True
            return False
        else:
            print('解析到' + str(len(imgList)) + '张图片')
            s.set('解析到' + str(len(imgList)) + '张图片')
        print('创建目录')
        s.set('创建目录')
        imgTitle = getTitle(imgLink)
        mkdir(imgTitle[0])
        print('下载中...')
        s.set('下载中...')
        imgNum = 1
        success = 0
        error = 0
        progress = 0
        for imgPath in imgList:
            imgUrl = imgPath[0] + '.' + imgPath[1]
            try:
                img = requests.get(imgUrl, headers=imgHeaders, timeout=60).content
                f = open(download + '\\' + imgTitle[0] + '\\' + str(imgNum) + '.' + imgPath[1], 'wb')
                f.write(img)
                f.close()
                print('下载进度: ' + str(round(imgNum * 100 / len(imgList))) + '% -> [success]')
                s.set('下载进度: ' + str(round(imgNum * 100 / len(imgList))) + '% -> [success]')
                success += 1
                log += str(imgNum) + '. ' + imgUrl + '\n'
            except Exception as e:
                print('下载进度: ' + str(round(imgNum * 100 / len(imgList))) + '% -> [error]')
                s.set('下载进度: ' + str(round(imgNum * 100 / len(imgList))) + '% -> [error]')
                error += 1
            imgNum += 1
        print('下载完成，' + str(success) + ' 成功，' + str(error) + ' 失败')
        s.set('下载完成，' + str(success) + ' 成功，' + str(error) + ' 失败')

        #写入日志
        f = open(download + '\\' + imgTitle[0] + '\\log.txt', 'w', encoding='utf-8')
        f.write(log)
        f.close()
        b.set('下载')
        state = True
        return True
    else:
        if state:
            l.set('地址错误请重新输入: ')
            print('获取内容失败')
            s.set('获取内容失败')
        return False


b = StringVar()
b.set('下载')
Button(root, textvariable=b, font=('SimHei', 12), command=lambda: MyThread(isUrl)).place(x=530, y=3)
Label(root, textvariable=s, font=('SimHei', 12)).place(x=5, y=40)
Label(root, text='By兰陵', font=('SimHei', 10)).place(x=530, y=55)
root.mainloop()
