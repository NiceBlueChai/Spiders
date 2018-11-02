import csv

from bs4 import BeautifulSoup as bs

from jingdong import HtmlDownload
import time


class Des:
    def __init__(self):
        self.n = 0
        self.a = 0
        # header = ['sku', 'url','title','comment', 'attrs']
        header = ['sku', 'url', 'attrs']
        self.rf = open('egg.csv', newline='')
        self.wf = open('des.csv', 'a+', newline='', encoding='utf-8')
        self.reader = csv.DictReader(self.rf)
        self.writer = csv.DictWriter(self.wf, header)
        try:
            with open('lin', 'r+')as f:
                self.a = f.read()
        except:
            self.writer.writeheader()
            print("lin")
        self._down = HtmlDownload()

    def __del__(self):
        self.rf.close()
        self.wf.close()

    def read_(self):

        for i, row in enumerate(self.reader):
            if self.a:
                if int(self.a) > i:
                    continue
            url = row["url"]
            sku = row["sku"]
            self._get_des(sku, url)
            print("正在爬取第%s个详情" % str(i))
            with open('lin', 'w', newline='')as f:
                f.write(str(i))

    def _get_des(self, sku, url):
        try:
            des = []
            res = self._down.download(url)
            if not res:
                self._get_des(sku, url)
            li = bs(res, 'html.parser').select(
                "[class='p-parameter'] ul li")  # parameter2 p-parameter-list
            if not li:
                self.writer.writerow(
                    {'sku': sku, 'url': url, 'attrs': str(des)})
                return
            for j in range(len(li)):
                des.append(li[j].getText().strip())
            self.writer.writerow({'sku': sku, 'url': url, 'attrs': str(des)})
        except Exception as e:
            print('get error', e)
            self._get_des(sku,url)


if __name__ == "__main__":
    d = Des()
    d.read_()
