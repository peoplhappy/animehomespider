from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from animehomespider import Item
from scrapy_splash import SplashRequest
import bs4
import re
from selenium import webdriver
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
        pagesrc=soup.select_one("#list_content_div > div > span.font14black")
        pagepattern = r"共(\d+)页"
        if pagesrc:
            page = re.match(pagepattern, pagesrc.text).group(1)
        else:
            soup=bs4.BeautifulSoup(self.getpagesource(response.url),"lxml")
            pagesrc = soup.select_one("#list_content_div > div > span.font14black")
            page = re.match(pagepattern, pagesrc.text).group(1)
        print("start to collect anime info")
        for i in range(int(page)):

        pass


    def pagepaser(self,response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        items = soup.select("#list_content_div > ul > li:nth-of-type(1) > div.anim_border")
        for item in items:
            url = self.main_url + item.select_one("a")["href"]
            yield SplashRequest(url=url, callback=self.itemparser,args={'wait': '10',"timeout":"3600","render_all":"1"},dont_filter=True)
    def itemparser(self,response):
        soup = bs4.BeautifulSoup(response.text, "lxml")
        item=Item.AnimehomespiderItem()
        item["animename"]=soup.select_one("body > div.page_bg > div.wrap > div.middleright > div > div.odd_anim_title > div.odd_anim_title_tnew > div > a > span > h1").text
        item["animeurl"]=response.url
        item["animeplaytimes"]=soup.select_one("body > div.page_bg > div.wrap > div.middleright > div > div.anim_online > div.h2_title2 > span:nth-of-type(4) > span").text
        item["animemaker"]=soup.select_one("body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-of-type(2) > ul > li:nth-of-type(9)").text
        item["animeshowtime"]=soup.select_one("body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-of-type(2) > ul > li:nth-of-type(4)").text
        item["animetype"]=soup.select_one("body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-of-type(2) > ul > li:nth-of-type(6)").text
        item["animerated"]=soup.select_one("#anim_score_info > span.points_text").text
        item["animetotalvideotime"]=soup.select_one("body > div.page_bg > div.wrap > div.middleright > div > div.anim_online > div.h2_title2 > span:nth-of-type(3) > span > a").text
        item["animeplaytype"]=soup.select_one("body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-of-type(2) > ul > li:nth-of-type(1)").text
        item["animeoriginmaker"]=soup.select_one("body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-of-type(2) > ul > li:nth-of-type(7)").text
        item["animedirector"]=soup.select_one("body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-of-type(2) > ul > li:nth-of-type(8)").text
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

