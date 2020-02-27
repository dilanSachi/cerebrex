import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class WswsEnglishCrawler(scrapy.Spider):
    name = "WswsEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.wsws.org/en/articles/'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/wsws/english").mkdir(parents=True, exist_ok=True)
        with open("./data/wsws/english/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('div.category p ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNewsMonth)

    def parseNewsMonth(self, response):
        for link in response.css('div.category ul li ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)

    def parseNews(self, response):
        header = response.css("div.clearfix div h2 ::text").getall()[1]
        content = response.css("div.clearfix p ::text").getall()
        time = response.css('div.clearfix h5 ::text').getall()[-1]
        url = response.url
        self.writeToJson(header, time, content, url)
