import scrapy
import json
from pathlib import Path
from random import randrange

class DailyNewsCrawler(scrapy.Spider):
    name = "DailyNewsCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'http://dailynews.lk/date/2020-02-22'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }
        # self.data['news'].append({  
        #     'Header': header,
        #     'Time': time,
        #     'Content': content
        # })

        Path("./data/dailynews/english").mkdir(parents=True, exist_ok=True)

        name = str(randrange(1000000))

        with open("./data/dailynews/english/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css("span.field-content ::attr(href)").getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.css("li.date-prev a ::attr(href)").getall()[0], self.parse)

    def parseNews(self, response):
        header = response.css("div.clearfix h1 ::text").get()
        content = response.css("div.field-items p ::text").getall()
        time = response.url.split("/")[3] + "/" + response.url.split("/")[4] + "/" + response.url.split("/")[5]
        self.writeToJson(header, time, content)
