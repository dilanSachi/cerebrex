import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class ArmyTamilCrawler(scrapy.Spider):
    name = "ArmyTamilCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.army.lk/ta/ta-photo-story',
        'https://www.army.lk/ta/ta-news-highlight',
        'https://www.army.lk/ta/ta-news-features'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/army/tamil").mkdir(parents=True, exist_ok=True)
        with open("./data/army/tamil/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('ul.cVerticleList li h4 a ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin("https://www.army.lk/ta/" + link), callback = self.parseNews)
        yield scrapy.Request(response.urljoin(response.css("li.next ::attr(href)").get()), callback=self.parse)

    def parseNews(self, response):
        header = response.css("div.container h1 ::text").get()
        content = response.css("div.container p ::text").getall()
        time = response.css("div.container p.cDate ::text").get()
        url = response.url
        self.writeToJson(header, time, content, url)
