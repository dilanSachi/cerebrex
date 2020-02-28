import scrapy
import json
from pathlib import Path
from random import randrange
from urllib import parse
from urllib.parse import parse_qs
from urllib.parse import urlparse

class GossipLankaEnglishCrawler(scrapy.Spider):
    name = "GossipLankaEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://english.gossiplankanews.com/'
    ]

    def writeToJson(self, header, time, content, name, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }
        Path("./data/gossiplanka/parallel/english").mkdir(parents=True, exist_ok=True)

        with open("./data/gossiplanka/parallel/english/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def writeToJsonSin(self, header, time, content, name, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }
        Path("./data/gossiplanka/parallel/sinhala").mkdir(parents=True, exist_ok=True)

        with open("./data/gossiplanka/parallel/sinhala/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css("div.title h1 a ::attr(href)").getall():
            if link is not None and "blogger.com" not in link:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        yield scrapy.Request(response.css("span.next-entries a ::attr(href)").get(), self.parse)

    def parseNews(self, response):
        header = response.css("div.title h1 a ::text").get()
        content = response.css("div.entry div ::text").getall()
        time = response.url.split("/")[3] + "_" + response.url.split("/")[4]
        sinhalaLink = response.css("div.entry a ::attr(href)").get()
        name = str(time) + str(randrange(1000000))
        url = response.url
        self.writeToJson(header, time, content, name, url)
        yield scrapy.Request(response.urljoin(sinhalaLink + "?" + parse.urlencode({"name": name})), self.parseSinhala)

    def parseSinhala(self, response):
        header = response.css("div.title h1 a ::text").get()
        content = response.css("div.entry ::text").getall()
        time = response.url.split("/")[3] + "/" + response.url.split("/")[4]
        parsed = urlparse(response.url)
        name = parse_qs(parsed.query)["name"][0]
        url = response.url
        self.writeToJsonSin(header, time, content, name, url)