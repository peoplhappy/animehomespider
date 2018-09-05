from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from animehomespider import Item
from scrapy_splash import SplashRequest
import bs4
import re
from selenium import webdriver
import json
import csv
class animespider(CrawlSpider):
    name="animespider"
    main_url="http://donghua.dmzj.com"
    start_urls = ["http://donghua.dmzj.com/acg_donghua/"]
    header={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",}



    def start_requests(self):
        for i in range(1999, 2019):
            url=self.start_urls[0]+"0-0-0-"+str(i)+"-all-0-0-0-"+"1.html"
            yield SplashRequest(url=url, callback=self.parser,args={'wait': '10',"timeout":"3600","render_all":"1"},dont_filter=True)

    def parser(self,response):
        #获取页数
        soup=bs4.BeautifulSoup(response.text,"lxml")
        pagesrc=soup.select_one("#list_content_div  div  span.font14black")
        pagepattern = r"共(\d+)页"
        if pagesrc:
            page = re.match(pagepattern, pagesrc.text).group(1)
        else:
            soup=bs4.BeautifulSoup(self.getpagesource(response.url),"lxml")
            pagesrc = soup.select_one("#list_content_div  div  span.font14black")
            page = re.match(pagepattern, pagesrc.text).group(1)
        print("start to collect anime info")
        pattern=r"\d+\.html"
        result=re.search(pattern,response.url);
        for i in range(1,int(page)+1):
            url = response.url.replace(result.group(0),"") + str(i)+".html"
            yield SplashRequest(url=url, callback=self.pagepaser,
                                args={'wait': '10', "timeout": "3600", "render_all": "1"}, dont_filter=True)


    def pagepaser(self,response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        items = soup.select("div.anim_border")
        for item in items:
            url = self.main_url + item.select_one("a")["href"]
            yield SplashRequest(url=url, callback=self.itemparser,args={'wait': '10',"timeout":"3600","render_all":"1"},dont_filter=True)
    def itemparser(self,response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        item=Item.AnimehomespiderItem()
        item["animename"]=soup.select_one("div.odd_anim_title_tnew  div  a  span  h1").text
        item["animeurl"]=response.url
        #提取播放次数
        playpattern=r"总播放次数为(\d+)次"
        result=re.search(playpattern,soup.select_one("div.anim_online  div.h2_title2  span:nth-of-type(4)").text)
        if result:
            item["animeplaytimes"]=result.group(1)
        else:
            item["animeplaytimes"] = 0
        makerpattern=r"制作公司\s+:\s+(.*)"
        result=re.search(makerpattern,soup.select_one("div.anim_attributenew  div:nth-of-type(2)  ul  li:nth-of-type(9)").text)
        if result:
            item["animemaker"] =result.group(1)
        else:
            item["animemaker"] = ""
        showpattern = r"首播时间\s+:\s+(.*)"
        result = re.search(showpattern,
                           soup.select_one("div.anim_attributenew  div:nth-of-type(2)  ul  li:nth-of-type(4)").text)
        if result:
            item["animeshowtime"] = result.group(1)
        else:
            item["animeshowtime"] = ""
        item["animetype"]=soup.select_one("div.anim_attributenew  div:nth-of-type(2)  ul  li:nth-of-type(6) a").text
        item["animerated"]=soup.select_one("#anim_score_info  span.points_text").text
        item["animetotalvideotime"]=soup.select_one("div.odd_anim_title > div.odd_anim_title_tnew > div > span.font12yellow").text
        playtypepattern=r"动画种类\s+:\s+(.*)"
        result = re.search(playtypepattern,
                           soup.select_one("div.anim_attributenew  div:nth-of-type(2)  ul  li:nth-of-type(1)").text)
        if result:
            item["animeplaytype"] = result.group(1)
        else:
            item["animeplaytype"] = ""
        originpattern = r"原作\s+:\s+(.*)"
        result = re.search(originpattern,
                           soup.select_one("div.anim_attributenew  div:nth-of-type(2)  ul  li:nth-of-type(7)").text)
        if result:
            item["animeoriginmaker"] = result.group(1)
        else:
            item["animeoriginmaker"] = ""
        directorpattern = r"监督\s+:\s+(.*)"
        result = re.search(directorpattern,
                           soup.select_one("div.anim_attributenew  div:nth-of-type(2)  ul  li:nth-of-type(8)").text)
        if result:
            item["animedirector"] = result.group(1)
        else:
            item["animedirector"] = ""
        print(json.dumps(dict(item),ensure_ascii=False))
        yield item
        pass
    def getpagesource(self,url):
        chrome_option = webdriver.ChromeOptions();
        chrome_option.add_argument("--headless")
        driverpath = "D:/Downloads/chromedriver_win32/chromedriver.exe"
        driver = webdriver.Chrome(driverpath, chrome_options=chrome_option)
        driver.get(url)
        driver.implicitly_wait(5)
        html = driver.page_source
        driver.close()
        return html
    def getvalue(self,pattern,srcdata,index):
        result=re.search(pattern,srcdata)
        if result:
            return result.group(index)
        else:
            return "-"
