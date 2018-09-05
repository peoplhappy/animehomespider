# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv


class AnimehomespiderPipeline(object):
    csv_file=None

    def __init__(self):
        fieldnames = ['动画名称', '动画url', '动画总集数', '动画放映时间', '动画评分', '动画的放映类型', '动画的播放次数', '动画原作', '动画类型', '动画制作公司',
                      '动画监督']



    def process_item(self, item, spider):
        #写入csv中
        self.csv_file = csv.writer(
            open("D:/animehomespider/animehomescrapy/animehomespider/animeinfo.csv", 'a',encoding="utf-8",newline=''))
        self.csv_file.writerow((item["animename"], item["animeurl"], item["animetotalvideotime"], item["animeshowtime"], item["animerated"], item["animeplaytype"],item["animeplaytimes"],item["animeoriginmaker"],item["animetype"],item["animemaker"],item["animedirector"]))
        return item
