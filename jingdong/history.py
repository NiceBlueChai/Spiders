
import csv
import functools
import json
from urllib import parse

import requests
from bs4 import BeautifulSoup as bs
from jd2 import Cre_Token_Js

from jingdong import HtmlDownload


def get_ip(x=5):
    '''
    代理ip
    '''
    ip_list = requests.get(
        "http://127.0.0.1:8000/?count=10")
    return json.loads(ip_list.text)

    # ip_list = requests.get(
    #     "http://www.httpdaili.com/api.asp?sl=5&noinfo=true&ddbh=253729634896557666").text.split('\r\n')
    # return ip_list


class ManMan:
    '''
    获取manmanbuy上的商品价格
    '''

    def __init__(self):
        self.ip_list = []
        self.proxies = {}
        self._try_num = 0
        self._get = functools.partial(requests.get, headers={
                                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36', 'Referer': 'http://www.manmanbuy.com'}, timeout=5)
        self._parse = functools.partial(parse.urlencode, encoding='GBK')
        # 等待再次爬取
        self.fail = set()
        self.a = 0
        # header = ['sku', 'url','title','comment', 'attrs']
        header = ['sku', 'manmanbuy']
        self.rf = open('egg.csv', newline='')
        self.wf = open('history.csv', 'a+', newline='', encoding='utf-8')
        self.reader = csv.DictReader(self.rf)
        self.writer = csv.DictWriter(self.wf, header)

        try:
            with open('history', 'r+')as f:
                self.a = f.read()
        except:
            self.writer.writeheader()

        self._down = HtmlDownload()
        # 初始化代理
        self.ip_ports = get_ip()
        self.ex_proxies()

    def __del__(self):
        self.rf.close()
        self.wf.close()

    def ex_proxies(self):
        '''
        切换代理ip
        '''
        if not self.ip_ports:
            self.ip_ports = get_ip()
        ip_port = self.ip_ports.pop()
        ip = ip_port[0]
        port = ip_port[1]
        self.proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }
        self._del_ip(ip)

        # if not self.ip_list:
        #     self.ip_list = get_ip()
        # ip_port = self.ip_list.pop()
        # self.proxies = {
        #     'http': 'http://%s' % ip_port,
        #     'https': 'http://%s' % ip_port
        # }

        print(self.proxies)

    def _del_ip(self, ip):
        '''
        删除ip
        '''
        r = requests.get('http://127.0.0.1:8000/delete?ip=%s' % ip)
        print(r.text)

    def read_(self):

        for i, row in enumerate(self.reader):
            if self.a:
                if int(self.a) > i:
                    continue
            sku = row["sku"]
            print("正在对比第%s个商品" % str(i))
            self._try_num = 0
            self._get_cost(sku)
            with open('history', 'w', newline='')as f:
                f.write(str(i))

    def _get_cost(self, sku):
        try:
            Goods_ID = sku
            Token = Cre_Token_Js(Goods_ID)  # 用JavaScript将含有商品ID的链接，加密生成token
            URL = 'http://tool.manmanbuy.com/history.aspx?DA=1&action=gethistory&url=http%253A%2F%2Fitem.jd.com%2F' + \
                Goods_ID+'.html&bjid=&spbh=&cxid=&zkid=&w=951&token='+Token
            print(Goods_ID)
            print(URL)
            res = self._get(url=URL, proxies=self.proxies)
            data = json.loads(res.text)
            v = data["datePrice"]
            if len(str(v)) < 20:
                raise Exception('验证码')
            print('其他平台的价格', str(v))
            self.writer.writerow({'sku': sku, 'manmanbuy': str(v)})

        except Exception as e:
            print("manman error", e)
            # 换代理重新爬取
            if self._try_num > 20:
                return
            print('try again')
            self.ex_proxies()
            self._try_num += 1
            self._get_cost(sku)
            return


if __name__ == "__main__":
    m = ManMan()
    m.read_()
