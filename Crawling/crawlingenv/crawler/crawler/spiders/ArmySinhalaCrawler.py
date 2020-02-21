import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class ArmySinhalaCrawler(scrapy.Spider):
    name = "ArmySinhalaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.army.lk/si/si-photo-story',
        'https://www.army.lk/si/si-news-highlight',
        'https://www.army.lk/si/si-news-features'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/army/sinhala").mkdir(parents=True, exist_ok=True)
        with open("./data/army/sinhala/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('ul.cVerticleList li h4 a ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin("https://www.army.lk/si/" + link), callback = self.parseNews)
        yield scrapy.Request(response.urljoin(response.css("li.next ::attr(href)").get()), callback=self.parse)

    def parseNews(self, response):
        header = response.css("div.container h1 ::text").get()
        content = response.css("div.container p.textalign ::text").getall()
        time = response.css("div.container p.cDate ::text").get()
        self.writeToJson(header, time, content)
