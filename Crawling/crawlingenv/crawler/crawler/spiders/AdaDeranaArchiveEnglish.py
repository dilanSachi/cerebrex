import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class AdaDeranaArchiveEnglish(scrapy.Spider):
    name = "AdaDeranaArchiveEnglish"

    data = {}
    data['news'] = []
    searchUrl = 'http://adaderana.lk/news_archive.php?srcRslt=1'

    start_urls = [
        'http://adaderana.lk/news_archive.php'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }

        Path("./data/ada_derana/english").mkdir(parents=True, exist_ok=True)
        with open("./data/ada_derana/english/" + str(time) + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for i in range(2020, 2006, -1):
            for j in range(1, 13):
                for k in range(1, 32):
                    time.sleep(1)
                    formdata = {'srcCategory': '999', 'srcYear':str(i), 'srcMonth':str(j), 'srcDay':str(k), 'Submit':'Search'}
                    yield FormRequest(self.searchUrl, callback=self.parsePage, formdata=formdata)

    def parsePage(self, response):
        for link in response.css('h2.hidden-xs ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                time.sleep(1)

    def parseNews(self, response):
        header = response.css("article.news h1 ::text").get()
        content = response.css("div.news-content ::text").getall()
        time = response.css('p.news-datestamp ::text').get()
        self.writeToJson(header, time, content)
