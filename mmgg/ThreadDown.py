import threading
from queue import Queue
from sqlite_select import select
import requests
n = 0


class ThreadDown(threading.Thread):

    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }

    def run(self):
        while True:
            global n
            n += 1
            try:
                a = self.queue.get(timeout=1)
                print(self.name, a)
                print("n=%r" % n)
                self._download(a[0])
                queue.task_done()
            except Exception:
                raise Exception

    def _download(self, url):
        filename = url.split('/')[-1]
        with open("img/"+filename, 'wb')as f:
            f.write(requests.get(url, headers=self._headers).content)


if __name__ == '__main__':
    queue = Queue()
    for item in select():
        queue.put(item)
    a = ["T0", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]
    b = []
    for name in a:
        thr = ThreadDown(name, queue)
        thr.start()
        b.append(thr)
    # queue.join()
    for i in b:
        i.join()
