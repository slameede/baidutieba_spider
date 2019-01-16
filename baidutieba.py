import requests
from lxml import etree

class BaiduImageSpider:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0"}
        self.baseurl = "http://tieba.baidu.com"
        self.page = "http://tieba.baidu.com/f?"
    # 获取每个帖子的url html的源码
    def getPageTieurl(self,params):
        res = requests.get(self.page,params=params,headers=self.headers)
        res.encoding = "utf-8"
        html = res.text

    #     从html中获取每个帖子的url
        parsehtml = etree.HTML(html)
        print(parsehtml)
        r_list = parsehtml.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        print(r_list)
        for t_houzhui in r_list:
            t_url = self.baseurl + t_houzhui
            self.getTieurlImage(t_url)


    #获取每个帖子中图片的url
    def getTieurlImage(self,t_url):
        # 获取帖子的html源码
        res = requests.get(t_url,headers=self.headers)
        res.encoding="utf-8"
    #     获取到每个帖子的url
        html = res.text
        # 获取图片的url
        parseHtml = etree.HTML(html)
        i_list = parseHtml.xpath('//img[@class="BDE_Image"]/@src')
        for i in i_list:
            self.writeImage(i)
            print(i)


    # 把图片保存到本地
    def writeImage(self,i):
        # 获取图片的源码bytes类型
        res = requests.get(i,headers=self.headers)
        res.encoding = "utf-8"
        html = res.content
    #     保存到本地
        filename = i[-10:]
        with open(filename,"wb") as f:
            print("%s正在下载"%filename)
            f.write(html)
            print("%s下载成功"%filename)


    def workOn(self):
        name = input("请输入要爬取的贴吧名：")
        begin = int(input("起始页："))
        end = int(input("终止页："))
        for page in range(begin,end+1):
            pn = (page-1)*50
            params = {"kw":name,
                      "pn":str(pn)
                      }
            self.getPageTieurl(params)


if __name__== "__main__":
    spider = BaiduImageSpider()
    spider.workOn()
