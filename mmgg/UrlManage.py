# URLMamager.py
# -*- coding: utf-8 -*-


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()  # 未爬取的URL集合
        self.old_urls = set()  # 已爬取的URL集合

    def has_new_url(self):
        '''
        判断是否有未爬取的URL
        :return: bool
        '''
        return self.new_url_size() != 0

    def add_new_url(self, url):
        '''
        将新的URL添加到未爬取的URL集合中
        url: str
        '''
        if url is None:
            return
        if url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls: list):
        '''
        将新的url列表添加到未爬取的URL集合中
        urls: list
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        '''
        获取一个未爬取的URL
        return a url
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def new_url_size(self):
        '''
        获取未爬取的URL集合的大小
        :return:
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''
        获取已经爬取过的URL集合的大小
        :return:
        '''
        return len(self.old_urls)
