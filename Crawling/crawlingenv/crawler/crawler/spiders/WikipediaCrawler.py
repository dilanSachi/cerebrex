import scrapy
import json
from random import randrange
from pathlib import Path

class WikipediaCrawler(scrapy.Spider):
    name = "WikipediaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://si.wikipedia.org/wiki/%E0%B7%80%E0%B7%92%E0%B7%81%E0%B7%9A%E0%B7%82:%E0%B7%83%E0%B7%92%E0%B6%BA%E0%B7%85%E0%B7%94_%E0%B6%B4%E0%B7%92%E0%B6%A7%E0%B7%94'
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

        Path("./data/wikipedia").mkdir(parents=True, exist_ok=True)

        with open("./data/wikipedia/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        print(response.url)
        for link in response.css('ul.mw-allpages-chunk li ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin("https://si.wikipedia.org" + link), callback = self.parseNews)

        yield scrapy.Request("https://si.wikipedia.org" + response.css('div.mw-allpages-nav ::attr(href)').getall()[-1], self.parse)

    def parseNews(self, response):
        header = response.css("div.mw-content-ltr ::text").getall()
        #content = response.css("div.lts-txt2 ::text").getall()
        #time = response.css('div.time ::text').get()
        self.writeToJson(header, "", "")
