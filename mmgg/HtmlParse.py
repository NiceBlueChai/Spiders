# coding: utf-8
import urllib.parse as parse
import json
import re

class HtmlParse(object):
    '''
    parse the response
    '''
    def parse(self, page_url, response):
        if not page_url or not response:
            return None
        soup = json.loads(response[9:-1],encoding='utf-8')
        new_url = self._get_new_url(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_url,new_data

    def _get_new_url(self, page_url, soup):
        '''
        抽取新的URL集合
        page_url: 下载页面的URL
        soup:soup
        :return: 返回新的URL集合
        '''
        baseUrl = "http://www.maomaogougou.cn/jsonp.asp?callback=callback&cid=0&id="
        id = soup["result"][-1]["id"]
        new_url = baseUrl+str(id)
        return new_url

    def _get_new_data(self, page_url, soup):
        '''
        抽取需要的数据
        page_url: 下载页面的URL
        :soup:
        :return: 返回有效数据list
        '''
        return soup["result"]
