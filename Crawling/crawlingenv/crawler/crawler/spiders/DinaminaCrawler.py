import scrapy
import json
from pathlib import Path
from random import randrange

class DinaminaCrawler(scrapy.Spider):
    name = "DinaminaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'http://www.dinamina.lk/date/2020-02-22'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/dailynews/sinhala").mkdir(parents=True, exist_ok=True)

        name = str(randrange(1000000))

        with open("./data/dailynews/sinhala/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css("span.field-content ::attr(href)").getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.css("li.date-prev a ::attr(href)").getall()[0], self.parse)

    def parseNews(self, response):
        header = response.css("div.clearfix h1 ::text").get()
        content = response.css("div.field-items div.even div ::text").getall()
        time = response.css("span.date-display-single ::text").get()
        url = response.url
        self.writeToJson(header, time, content, url)
