import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class LankapuwathEnglishCrawler(scrapy.Spider):
    name = "LankapuwathEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'http://english.lankapuvath.lk/category/local/',
        'http://english.lankapuvath.lk/category/world/',
        'http://english.lankapuvath.lk/category/sport/',
        'http://english.lankapuvath.lk/category/business/',
        'http://english.lankapuvath.lk/category/viewpoint/'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/lankapuwath/english").mkdir(parents=True, exist_ok=True)
        with open("./data/lankapuwath/english/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('h2.entry-title ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.urljoin(response.css("div.nav-links a.next ::attr(href)").get()), callback=self.parse)

    def parseNews(self, response):
        header = response.css("h1.entry-title ::text").get()
        content = response.css("div.article-container div.entry-content p ::text").getall()
        time = response.css("span.entry-meta-left-section time.entry-date ::text").get()
        self.writeToJson(header, time, content)
