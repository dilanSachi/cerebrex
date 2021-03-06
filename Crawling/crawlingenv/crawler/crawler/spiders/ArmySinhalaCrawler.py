import scrapy
import json
from pathlib import Path
from random import randrange

class ArmySinhalaCrawler(scrapy.Spider):
    name = "ArmySinhalaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.army.lk/si/si-news-highlight',
        'https://www.army.lk/si/si-photo-story',
        'https://www.army.lk/si/si-news-features'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
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
        content = response.css("div.container p ::text").getall()
        time = response.css("div.container p.cDate ::text").get()
        url = response.url
        self.writeToJson(header, time, content, url)
