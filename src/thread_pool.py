#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-
"""
线程池
"""

import queue
import threading


class CustomThread(threading.Thread):
    """多线程"""

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        """执行"""
        while True:
            if self.q.empty():
                break
            func, args = self.q.get()
            func(*args)
            self.q.task_done()


class CustomThreadPool(object):
    """线程池"""

    def __init__(self, maxsize=100):
        self.q = queue.Queue()
        self.maxsize = maxsize
        self.thread_pool = []
        self.task = ()

    def add_task(self, tasks):
        """
        添加任务列表
        """
        for self.task in tasks:
            self.q.put(self.task)

    def add_thread(self):
        """初始化线程池"""
        for i in range(self.maxsize):
            thread = CustomThread(self.q)
            self.thread_pool.append(thread)

    def start_thread(self):
        """开始线程任务"""
        for i in range(len(self.thread_pool)):
            self.thread_pool[i].start()

    def close(self):
        """结束"""
        self.q.join()
