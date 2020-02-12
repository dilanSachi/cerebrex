import scrapy
import json
import io
from pathlib import Path
from random import randrange

class ITNTamilCrawler(scrapy.Spider):
    name = "ITNTamilCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.itnnews.lk/ta/international/',
        'https://www.itnnews.lk/ta/local/',
        'https://www.itnnews.lk/ta/entertainment/',
        'https://www.itnnews.lk/ta/business/',
        'https://www.itnnews.lk/ta/sports/'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/itn/tamil").mkdir(parents=True, exist_ok=True)
        with open("./data/itn/tamil/" + time + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('div.block-content a.more ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.css('a.next ::attr(href)').get(), self.parse)

    def parseNews(self, response):
        header = response.css("div.article-title h1 ::text").get()
        content = response.css("div.column9 ::text").getall()
        time = response.css('div.a-content span.meta ::text').get()
        self.writeToJson(header, time, content)
