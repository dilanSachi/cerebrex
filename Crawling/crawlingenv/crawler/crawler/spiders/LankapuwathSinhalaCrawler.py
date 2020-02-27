import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class LankapuwathSinhalaCrawler(scrapy.Spider):
    name = "LankapuwathSinhalaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'http://sinhala.lankapuvath.lk/category/local/',
        'http://sinhala.lankapuvath.lk/category/world/',
        'http://sinhala.lankapuvath.lk/category/sport/',
        'http://sinhala.lankapuvath.lk/category/business/',
        'http://sinhala.lankapuvath.lk/category/viewpoint/',
        'http://sinhala.lankapuvath.lk/category/more-news/'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/lankapuwath/sinhala").mkdir(parents=True, exist_ok=True)
        with open("./data/lankapuwath/sinhala/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
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
        url = response.url
        self.writeToJson(header, time, content, url)
