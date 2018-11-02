import functools
import json
import re
from urllib import parse
from bs4 import BeautifulSoup as bs
import requests


class HtmlDownload:
    def __init__(self):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        self._get = functools.partial(requests.get, headers=self._headers)

    def download(self, url):
        '''
        下载页面
        :param url: 要下载页面的链接
        :type url: str
        '''

        try:
            res = self._get(url)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
        except Exception:
            print("Download Error")
            return None
        return res.text


class HtmlParse:
    _d = HtmlDownload()
    new_data = []

    def parse(self, page_url, response):
        if not page_url or not response:
            return
        soup = bs(response, 'html.parser')
        new_url = self._get_new_url(page_url, soup)
        new_data = self._get_data(page_url, soup)
        return new_url, new_data

    def _get_new_url(self, page_url, soup):
        next_page_url = soup.select('.pn-next')[0].attrs.get('href')
        if not next_page_url:
            return None
        next_page_url = parse.urljoin(page_url, next_page_url)
        return next_page_url

    def _get_data(self, page_url, soup):
        '''

        '''

        skulist = []
        goods_list = soup.select("[class='gl-i-wrap j-sku-item']")
        for i in range(len(goods_list)):
            goods = goods_list[i]
            # 商品名称
            title = goods.select("div[class=p-name] em")[0].getText().strip()
            sku = goods.attrs.get('data-sku', None)
            self.new_data.append({'sku': sku, 'title': title})
            skulist.append(sku)
        self._get_com_price(skulist)
        self._get_des(self.new_data)
        return self.new_data

    def _get_com_price(self, skulist):
        '''
        获取商品的价格和评论数
        '''
        c_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + \
            ",".join(skulist)
        # 评论数
        coment = json.loads(self._d.download(c_url))
        for i in range(len(skulist)):
            self.new_data[i]["comment"] = coment[
                "CommentsCount"][i]["CommentCount"]
        for i in range(len(self.new_data)):
            # 价格
            p_url = "https://p.3.cn/prices/mgets?skuIds=J_" + \
                self.new_data[i]['sku']
            self.new_data[i]["price"] = json.loads(
                self._d.download(p_url))[0]["p"]

    def _get_des(self, skulist):
        '''
        获取商品详情页面的属性
        '''
        for i in range(len(self.new_data)):
            url = "https://item.jd.com/"+self.new_data[i]['sku']+'.html'
            des = []
            li = bs(self._d.download(url), 'html.parser').select(
                "[class='parameter2 p-parameter-list'] li")
            if not li:
                self.new_data[i]["attrs"] = des
                return
            for i in range(len(li)):
                des.append(li[i].getText())
            self.new_data[i]["attrs"] = des


class UrlManage:
    def __init__(self):
        self.new_urls = set()
        self.old_ulrs = set()

    def has_new_url(self):
        '''
        是否有未爬取的链接
        :return: bool
        '''
        return self.new_url_size() != 0

    def new_url_size(self):
        '''
        未爬取的链接数
        :return: Integer
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''
        已爬取的链接数
        :return: Integer
        '''
        return len(self.old_ulrs)

    def get_new_url(self):
        '''
        获取一个未爬取的url
        :return: string
        '''
        new_url = self.new_urls.pop()
        self.old_ulrs.add(new_url)
        return new_url

    def add_new_url(self, url):
        '''
        新添加一个ulr到未爬取的集合中
        :param url: new url
        :type url: string
        '''
        self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        将新的url列表添加到未爬取的URL集合中
        :param urls: new url list
        :type urls: list
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)


class DataOutput:
    '''
    输出到文件
    '''

    def __init__(self):
        self._f = open('s.json', 'w', encoding='utf-8')
        self.data = {}

    def __del__(self):
        self._f.close()
        print("文件已保存")

    def store_data(self, data):
        if not data:
            return
        self.data['goods'] = data

    def output_(self):
        json.dump(self.data, self._f, ensure_ascii=False)


class Schedule:
    '''
    爬虫调度
    '''

    def __init__(self):
        self._download = HtmlDownload()
        self._parse = HtmlParse()
        self._manage = UrlManage()
        self._output = DataOutput()

    def craw(self, root_url):
        '''
        :param root_url: 入口url
        :type root_url: string
        '''
        self._manage.add_new_url(root_url)
        # 判断是否还有未爬取的url
        while(self._manage.has_new_url and self._manage.old_url_size() < 2):
            print("正在爬取第%r个页面" % str(self._manage.old_url_size()+1))
            try:
                # 取一个未爬取的url
                new_url = self._manage.get_new_url()
                response = self._download.download(new_url)
                new_url, data = self._parse.parse(new_url, response)
                self._manage.add_new_url(new_url)
                self._output.store_data(data)

            except Exception as e:
                print('crawl Error', e)
                break
        try:
            self._output.output_()
        except Exception as e:
            print("输出错误", e)


if __name__ == '__main__':
    import time
    c = time.time()
    spider_man = Schedule()
    spider_man.craw("https://list.jd.com/list.html?cat=670%2C671%2C672&go=0")
    print(time.time()-c)
