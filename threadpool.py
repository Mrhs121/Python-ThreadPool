import requests
from bs4 import BeautifulSoup
import re
import os
import threading
from functools import partial
import queue


# 线程池
class ThreadPool(object):
    def __init__(self, max_workers):
        self.queue = queue.Queue()
        self.workers = [threading.Thread(target=self._worker) for _ in range(max_workers)]

    def start(self):
        for worker in self.workers:
            worker.start()

    def stop(self):
        for _ in range(self.workers):
            self.queue.put(None)
        for worker in self.workers:
            worker.join()

    def submit(self, job):
        self.queue.put(job)

    def _worker(self):
        while True:
            job = self.queue.get()
            if job is None:
                break
            job()


def download(url, dirname):
    r = requests.get(url)
    if r.status_code == 200:
        folder = os.path.exists("./download/" + dirname)
        if not folder:
            os.makedirs("./download/" + dirname)
        print("下载 " + url)
        with open("./download/" + dirname + '/' + url.split("/")[-1], "wb") as code:
            code.write(r.content)
        return 0
    else:
        return -1


pool = ThreadPool(max_workers=8)
pool.start()
urls = [...........] # 例如可以是需要爬的所有页面的url、或者所有需要下载文件的链接等等
for url in urls:
  pool.submit(partial(download, url, dirname))
pool.stop()