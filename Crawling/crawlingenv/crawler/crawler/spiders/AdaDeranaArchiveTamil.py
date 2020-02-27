import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest

class AdaDeranaArchiveTamil(scrapy.Spider):
    name = "AdaDeranaArchiveTamil"

    data = {}
    data['news'] = []
    searchUrl = 'http://sinhala.adaderana.lk/news_archive.php?srcRslt=1'

    start_urls = [
        'http://tamil.adaderana.lk/news_archive.php'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("./data/ada_derana/tamil").mkdir(parents=True, exist_ok=True)
        with open("./data/ada_derana/tamil/" + str(time) + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for i in range(2020, 2006, -1):
            for j in range(1, 13):
                for k in range(1, 32):
                    time.sleep(3)
                    formdata = {'srcCategory': '999', 'srcYear':str(i), 'srcMonth':str(j), 'srcDay':str(k), 'Submit':'Search'}
                    yield FormRequest(self.searchUrl, callback=self.parsePage, formdata=formdata)

    def parsePage(self, response):
        for link in response.css('div.story-text h4 a ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                time.sleep(3)

    def parseNews(self, response):
        header = response.css("h2.completeNewsTitle ::text").get()
        content = response.css("div.newsContent ::text").getall()
        time = response.css('p.newsDateStamp ::text').get()
        url = response.url
        self.writeToJson(header, time, content, url)
