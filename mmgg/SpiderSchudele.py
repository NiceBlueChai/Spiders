from DataOutput import DataOutput,create_db
from HtmlDownload import HtmlDownload
from HtmlParse import HtmlParse
from UrlManage import UrlManager

class Schedul(object):
    def __init__(self):
        self._manager = UrlManager()
        self._download = HtmlDownload()
        self._parse = HtmlParse()
        self._output = DataOutput()
    def crawl(self, root_url):
        # 入口url
        self._manager.add_new_url(root_url)
        # 判断是否还有新的url
        while(self._manager.has_new_url()):
            try:
                # 从URL管理器中获取URL
                new_url = self._manager.get_new_url()
                # 下载网页
                response = self._download.download(new_url)
                # 解析抽取网页数据
                new_url, data = self._parse.parse(new_url, response)
                # 将抽取到的新的urls添加到URL管理器中
                self._manager.add_new_url(new_url)
                # 数据存储器存储数据
                self._output.store_data(data)
                print('已经抓取了 %s 个链接' %self._manager.old_url_size())
                print(new_url)
            except Exception as e:
                print('crawl Error',e)
        #数据存储器将文件输出成指定格式
            try:
                self._output.output_db()
            except:
                print('output Error')

if __name__ =="__main__":
    create_db()
    spider_man = Schedul()
    # spider_man.crawl('http://www.maomaogougou.cn/jsonp.asp?callback=callback&cid=7&id=28568')
    spider_man.crawl('http://www.maomaogougou.cn/jsonp.asp?callback=callback&cid=7&id=568')