# coding: utf-8
import requests
import functools


class HtmlDownload:
    def __init__(self):
        self._M_headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
        self._headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
            }
        self.get = functools.partial(requests.get, headers=self._headers)
    def download(self, url):
        '''
        return response
        '''
        try:
            res = self.get(url)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
        except Exception:
            print("Download Error")
            return None
        return res.text