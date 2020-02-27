import scrapy
import json
from random import randrange
from pathlib import Path
from urllib import parse
from urllib.parse import parse_qs
from urllib.parse import urlparse

class WikipediaSinhalaCrawler(scrapy.Spider):
    name = "WikipediaSinhalaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://si.wikipedia.org/wiki/%E0%B7%80%E0%B7%92%E0%B7%81%E0%B7%9A%E0%B7%82:%E0%B7%83%E0%B7%92%E0%B6%BA%E0%B7%85%E0%B7%94_%E0%B6%B4%E0%B7%92%E0%B6%A7%E0%B7%94'
    ]

    def writeToJson(self, header, content, name, url):
        obj = {  
            'Header': header,
            'Url': url,
            'Content': content
        }
        # self.data['news'].append({  
        #     'Header': header,
        #     'Time': time,
        #     'Content': content
        # })

        Path("./data/wikipedia/aligned_news").mkdir(parents=True, exist_ok=True)

        with open("./data/wikipedia/aligned_news/" + name + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        print(response.url)
        for link in response.css('ul.mw-allpages-chunk li ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin("https://si.wikipedia.org" + link), callback = self.parseNews)

        yield scrapy.Request("https://si.wikipedia.org" + response.css('div.mw-allpages-nav ::attr(href)').getall()[-1], self.parse)

    def parseNews(self, response):
        header = response.css("h1.firstHeading ::text").getall()
        content = response.css("div.mw-content-ltr ::text").getall()
        en = response.css("div.body li.interwiki-en ::attr(href)").get()
        ta = response.css("div.body li.interwiki-ta ::attr(href)").get()
        name = str(randrange(1000000))
        if (en):
            yield scrapy.Request(en + "?" + parse.urlencode({"name": name}), callback = self.parseEngTamNews)
        if (ta):
             yield scrapy.Request(ta + "?" + parse.urlencode({"name": name}), callback = self.parseEngTamNews)
        self.writeToJson(header, content, name)

    def parseEngTamNews(self, response):
        header = response.css("h1.firstHeading ::text").getall()
        content = response.css("div.mw-content-ltr ::text").getall()
        parsed = urlparse(response.url)
        name = parse_qs(parsed.query)["name"][0]
        url = response.url
        self.writeToJson(header, content, name, url)