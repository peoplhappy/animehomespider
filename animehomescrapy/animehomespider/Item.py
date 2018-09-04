# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimehomespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    animename = scrapy.Field() # 动画名称 body > div.page_bg > div.wrap > div.middleright > div > div.odd_anim_title > div.odd_anim_title_tnew > div > a > span > h1
    animeurl = scrapy.Field()  # 动画的播放url 提取后直接进入通过response获取
    animeplaytimes = scrapy.Field() #动画的播放次数 body > div.page_bg > div.wrap > div.middleright > div > div.anim_online > div.h2_title2 > span:nth-child(4) > span
    animemaker = scrapy.Field()  # 动画的制作商 制作公司 : Bones 可能多个，正则提取  body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-child(2) > ul > li:nth-child(9)
    animeshowtime = scrapy.Field() #动画的放映时间 首播时间 : 2018-04-07，需要正则提取 body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-child(2) > ul > li:nth-child(4)
    animetype = scrapy.Field()  #动画的类型 悬疑等 取下面所有a的innertext body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-child(2) > ul > li:nth-child(6)
    animerated = scrapy.Field() #动画的评分  #anim_score_info > span.points_text 评分
    animetotalvideotime = scrapy.Field() #动画的集数  body > div.page_bg > div.wrap > div.middleright > div > div.anim_online > div.h2_title2 > span:nth-child(3) > span > a
    animeplaytype = scrapy.Field() #放映种类  TV  OVA 剧场等信息为 动画种类:TV，正则提取 body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-child(2) > ul > li:nth-child(1)
    animeoriginmaker = scrapy.Field() #原作 原作 : 堀越耕平 正则提取（可能多个）body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-child(2) > ul > li:nth-child(7)
    animedirector = scrapy.Field() #监督 监督 : 长崎健司 正则提取（可能多个）   body > div.page_bg > div.wrap > div.left > div > div.anim_intro > div.week_mend_new > div > div.anim_attributenew > div:nth-child(2) > ul > li:nth-child(8)
    pass
     ##list_content_div > div > span.font14bold  第多少页，正则取出循环获取