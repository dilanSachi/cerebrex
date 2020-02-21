import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class NewsLkSinhalaCrawler(scrapy.Spider):
    name = "NewsLkSinhalaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://sinhala.news.lk/news'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/newslk/sinhala").mkdir(parents=True, exist_ok=True)
        with open("./data/newslk/sinhala/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('h3.catItemTitle a ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.urljoin("https://sinhala.news.lk" + response.css("ul.pagination li ::attr(href)").getall()[-2]), callback=self.parse)

    def parseNews(self, response):
        header = response.css("h2.itemTitle ::text").getall()
        content = response.css("div.itemIntroText ::text").getall() + response.css("div.itemFullText ::text").getall()
        time = response.css("span.itemDateCreated ::text").getall()
        self.writeToJson(header, time, content)
