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

class WswsTamilOldArchiveCrawler(scrapy.Spider):
    name = "WswsTamilOldArchiveCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.wsws.org/tamil/archive/archive.shtml'
    ]

    def writeToJson(self, header, time, content, name, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/wsws/tamil_parallel/tamil").mkdir(parents=True, exist_ok=True)
        with open("./data/wsws/tamil_parallel/tamil/" + name + ".json", 'a', encoding="utf8") as outfile:
            json.dump(obj, outfile, ensure_ascii=False)

    def writeToJsonEng(self, header, time, content, name, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/wsws/tamil_parallel/english").mkdir(parents=True, exist_ok=True)
        with open("./data/wsws/tamil_parallel/english/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css("table table td font a ::attr(href)").getall():
            if link is not None and "archive/archive" not in link:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNewsMonth)

    def parseNewsMonth(self, response):
        for link in response.css('span.Apple-style-span ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)

    def parseNews(self, response):
        header = response.css("td h2 span font ::text").get()
        content = response.css("table td p ::text").getall()
        time = ""
        name = str(randrange(1000000))
        totalLinks = response.css("a ::attr(href)").getall()
        for link in totalLinks:
            if "/en/articles" in link:
                yield scrapy.Request(response.urljoin(link + "?" + parse.urlencode({"name": name})), callback=self.parseEngNews)
                break
        url = response.url
        self.writeToJson(header, time, content, name, url)

    def parseEngNews(self, response):
        header = response.css("div.clearfix div h2 ::text").getall()[1]
        content = response.css("div.clearfix p ::text").getall()
        time = response.css('div.clearfix h5 ::text').getall()[-1]
        parsed = urlparse(response.url)
        name = parse_qs(parsed.query)["name"][0]
        url = response.url
        self.writeToJsonEng(header, time, content, name, url)
