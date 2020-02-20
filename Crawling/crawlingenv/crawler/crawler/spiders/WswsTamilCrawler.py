import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest
from urllib import parse
from urllib.parse import parse_qs
from urllib.parse import urlparse

class WswsTamilCrawler(scrapy.Spider):
    name = "WswsTamilCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.wsws.org/tamil/archive.shtml'
    ]

    def writeToJson(self, header, time, content, name):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/wsws/tamil").mkdir(parents=True, exist_ok=True)
        with open("./data/wsws/tamil/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css("#midColm h2 ::attr(href)").getall():
            if link is not None:
                yield scrapy.Request(response.urljoin("https://www.wsws.org" + link), callback = self.parseNews)

    def parseNews(self, response):
        header = response.css("#article h2 ::text").get()
        content = response.css("#article p ::text").extract()
        time = response.css("#article h5 ::text").extract()[-1]
        try:
            engLink = response.css("#article h4 ::attr(href)").getall()
            name = str(time) + str(randrange(1000000))
            if len(engLink) > 0:
                yield scrapy.Request(response.urljoin(engLink[0] + "?" + parse.urlencode({"name": name})), callback=self.parseEngNews)
        except Exception:
            engLink = response.css("#article h5 ::attr(href)").getall()
            name = str(time) + str(randrange(1000000))
            if len(engLink) > 0:
                yield scrapy.Request(response.urljoin(engLink[0] + "?" + parse.urlencode({"name": name})), callback=self.parseEngNews)
        self.writeToJson(header, time, content, name)

    def parseEngNews(self, response):
        header = response.css("div.clearfix div h2 ::text").getall()[1]
        content = response.css("div.clearfix p ::text").getall()
        time = response.css('div.clearfix h5 ::text').getall()[-1]
        parsed = urlparse(response.url)
        name = parse_qs(parsed.query)["name"][0]
        self.writeToJson(header, time, content, name)
