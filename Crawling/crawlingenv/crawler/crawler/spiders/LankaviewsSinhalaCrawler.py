import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class LankaviewsSinhalaCrawler(scrapy.Spider):
    name = "LankaviewsSinhalaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.lankaviews.com/category/local-news/',
        'https://www.lankaviews.com/category/foriegn-news/'
        'https://www.lankaviews.com/category/sports-news/',
        'https://www.lankaviews.com/category/views/'
    ]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                    errback=self.parse,
                                    dont_filter=True)

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/lankaviews/sinhala").mkdir(parents=True, exist_ok=True)
        with open("./data/lankaviews/sinhala/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, failure):
        response = failure.value.response
        for link in response.css("a.news_heading_a ::attr(href)").getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews, errback = self.parseNews)
        yield scrapy.Request(response.urljoin(response.css("div.row a ::attr(href)").getall()[-1]), callback=self.parse, errback=self.parse)

    def parseNews(self, response):
        header = response.css("section.post_p h2 ::text").get()
        content = response.css("p.custom_lvwp_p ::text").getall()
        time = response.css("p.post_info ::text").get().split(" ")[2]
        self.writeToJson(header, time, content)
