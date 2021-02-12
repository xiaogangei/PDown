# -*- coding: utf-8 -*
import threading
import requests
import os
import time


class DownThread:
    def __init__(self, url, path, threadList):
        self.id = url
        self.url = url
        self.path = path
        self.fileName = os.path.basename(path)
        self.fileSize = self.getFileSize()
        self.progress = 0
        self.networkSpeed = 0
        self.remainingTime = 0
        self.isStart = False
        self.thread = threading.Thread(target=self.__downThread__)
        self.threadList = threadList

    def __downFile__(self):
        # 这重要了，先看看本地文件下载了多少
        if os.path.exists(self.path):
            temp_size = os.path.getsize(self.path)  # 本地已经下载的文件大小
        else:
            temp_size = 0
        # 显示一下下载了多少
        # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
        headers = {'Range': 'bytes=%d-' % temp_size}
        # 重新请求网址，加入新的请求头的
        r = requests.get(self.url, stream=True, verify=False, headers=headers)
        # 下面写入文件也要注意，看到"ab"了吗？
        # "ab"表示追加形式写入文件
        with open(self.path, "ab") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    ###这是下载实现进度显示####
                    self.progress = int(100 * temp_size / self.fileSize)
    # 获取文件大小

    def getFileSize(self):
        # 第一次请求是为了得到文件总大小
        r1 = requests.get(self.url, stream=True, verify=False)
        return int(r1.headers['Content-Length'])

    def getUrl(self):
        return self.url

    def getFileName(self):
        return self.fileName

    def getProgress(self):
        return self.progress

    def start(self):
        self.thread.start()

    def __downThread__(self):
        self.isStart = True
        # for x in range(100):
        #     time.sleep(1)
        #     self.progress += 1
        # print("下载文件中.....")
        self.__downFile__()
        self.threadList.remove(self)
        self.isStart = False
