import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class ArmyEnglishArchiveCrawler(scrapy.Spider):
    name = "ArmyEnglishArchiveCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.army.lk/news-archive',
        'https://www.army.lk/news-archive-2002-2009'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/army/english/archive").mkdir(parents=True, exist_ok=True)
        with open("./data/army/english/archive/" + str(randrange(10000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('ul.cVerticleList li h2 a ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin("https://www.army.lk/" + link), callback = self.parseNews)
        yield scrapy.Request(response.urljoin(response.css("li.next ::attr(href)").get()), callback=self.parse)

    def parseNews(self, response):
        header = response.css("div.container h1 ::text").get()
        content = response.css("div.container p ::text").getall()
        time = response.css("div.container p.cDate ::text").get()
        self.writeToJson(header, time, content)
