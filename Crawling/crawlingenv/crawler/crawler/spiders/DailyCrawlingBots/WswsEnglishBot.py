import scrapy
from pathlib import Path
from random import randrange
import json
import datetime

class WswsEnglishBot(scrapy.Spider):
    name = "WswsEnglishBot"

    start_urls = [
        'https://www.wsws.org/en/articles/'
    ]

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../../data/wsws/bot/english").mkdir(parents=True, exist_ok=True)
        with open("../../../data/wsws/bot/english/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as ofile:
            json.dump(obj, ofile, ensure_ascii=False)

    def parse(self, response):
        newsMonths = response.css('div.category p ::attr(href)').getall()
        today = datetime.date.today()
        first = today.replace(day=1)
        prevMonth = (first - datetime.timedelta(days=1)).strftime("%Y/%m")

        for monthLink in newsMonths:
            if monthLink is not None and prevMonth in monthLink:
                yield scrapy.Request(response.urljoin(monthLink), callback = self.parseMonth)
                break

    def parseMonth(self, response):
        for link in response.css('div.category ul li ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)

    def parseNews(self, response):
        header = response.css("div.clearfix div h2 ::text").getall()[1]
        content = response.css("div.clearfix p ::text").getall()
        time = response.css('div.clearfix h5 ::text').getall()[-1]
        url = response.url
        self.writeToJson(header, time, content, url)
