import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class NewsLkEnglishCrawler(scrapy.Spider):
    name = "NewsLkEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://news.lk/news'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/newslk/english").mkdir(parents=True, exist_ok=True)
        with open("./data/newslk/english/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('h3.catItemTitle a ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.urljoin("https://news.lk" + response.css("ul.pagination li ::attr(href)").getall()[-2]), callback=self.parse)

    def parseNews(self, response):
        header = response.css("h2.itemTitle ::text").getall()
        content = response.css("div.itemIntroText p ::text").getall() + response.css("div.itemFullText p ::text").getall()
        time = response.css("span.itemDateCreated ::text").getall()
        url = response.url
        self.writeToJson(header, time, content, url)
