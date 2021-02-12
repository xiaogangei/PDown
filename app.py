#!/usr/bin/env python3
# -*- coding: utf-8 -*
# app.py
# @author Will Holmes
# @description
# @created 2021-02-11 13:05:06
# @last-modified 2021-02-12 14:52:05
# ---------------------------------------------------------


from flask import Flask, render_template, request
import sys
import requests
import os
import threading
import time
import json
from DownThread import DownThread
from tools import formatFileSize

app = Flask(__name__)
downPath = "/Users/xiaogang/Downloads/"
downProgress = 0
downList = []
threadList = []
# 是否完成
isComplete = False
# 下载文件
requests.packages.urllib3.disable_warnings()

# 判断下载目录是否存在，如果不存在创建
if not os.path.isdir(downPath):
    os.makedirs(downPath)


@app.route('/download')
def download():
    global downUlr, downList
    url = request.args.get('url')
    path = request.args.get('path')
    # 判断是否传入URL
    if url == None:
        res = {"code": 401, "msg": "Missing the url parameter!! "}
        return json.dumps(res)
    # 获取文件名
    if path == None:
        fileName = os.path.basename(url)
    else:
        fileName = path
    # 获取文件大小
    # 文件路径
    filePath = downPath+fileName
    currThread = None
    # 判断下载线程是否存在
    for thread in threadList:
        if thread.getUrl() == url:
            currThread = thread
    # 如果线程不存在就创建
    if currThread == None:
        currThread = DownThread(url, filePath,threadList)
        currThread.start()
        threadList.append(currThread)

    res = {"code": 200, "file_name": currThread.getFileName(),
           "file_size": currThread.getFileSize(), "progress": currThread.getProgress()}
    return json.dumps(res)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/downloading')
def downloading():
    return render_template("downloading.html")


@app.route('/downComplete')
def downComplete():
    return render_template("downComplete.html")


@app.route('/getCompleteList')
def getCompleteList():
    fileList = os.listdir(downPath)
    res = {"code": 200, "file_list": fileList}
    return json.dumps(res)


@app.route('/getDownList')
def getDownList():
    dowList = []
    for thread in threadList:
        downFile = {
            "url": thread.getUrl(),
            "file_name": thread.getFileName(),
            "file_size": formatFileSize(thread.getFileSize()),
            "progress": thread.getProgress()
        }
        dowList.append(downFile)

    res = {"code": 200, "down_list": dowList}
    return json.dumps(res)


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True)
