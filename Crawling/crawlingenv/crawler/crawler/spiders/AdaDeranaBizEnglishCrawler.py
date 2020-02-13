import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time

class AdaDeranaBizEnglishCrawler(scrapy.Spider):
    name = "AdaDeranaBizEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'http://bizenglish.adaderana.lk/category/top-news/',
        'http://bizenglish.adaderana.lk/category/news-2/',
        'http://bizenglish.adaderana.lk/category/analysis/',
        'http://bizenglish.adaderana.lk/category/features/'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/ada_derana/english").mkdir(parents=True, exist_ok=True)
        with open("./data/ada_derana/english/" + time + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('div.business-summary div.col-lg-12 ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        time.sleep(3)
        yield scrapy.Request(response.css('ul.pager ::attr(href)').getall()[-2], self.parse)

    def parseNews(self, response):
        header = response.css("div.news-header h3 ::text").get()
        content = response.css("div.news-text ::text").getall()
        time = response.css('div.news-header p ::text').get()
        self.writeToJson(header, time, content)
