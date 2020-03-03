import scrapy
from pathlib import Path
from random import randrange
import json
import datetime
from urllib import parse
from urllib.parse import parse_qs
from urllib.parse import urlparse

class WswsTamilBot(scrapy.Spider):
    name = "WswsTamilBot"

    start_urls = [
        'https://www.wsws.org/ta/articles/'
    ]

    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    def writeToJson(self, header, time, content, name, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../../data/wsws/bot/tamil_parallel/tamil").mkdir(parents=True, exist_ok=True)
        with open("../../../data/wsws/bot/tamil_parallel/tamil/" + name + ".json", 'a', encoding="utf8") as ofile:
            json.dump(obj, ofile, ensure_ascii=False)

    def writeEngToJson(self, header, time, content, name, url):
        obj = {
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../../data/wsws/bot/tamil_parallel/english").mkdir(parents=True, exist_ok=True)
        with open("../../../data/wsws/bot/tamil_parallel/english/" + name + ".json", 'a', encoding="utf8") as outfile:
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        newsMonths = response.css('div.category p ::attr(href)').getall()
        today = datetime.date.today()
        first = today.replace(day=1)
        prevMonth = (first - datetime.timedelta(days=1)).strftime("%Y/%m")

        for monthLink in newsMonths:
            if monthLink is not None and prevMonth in monthLink:
                yield scrapy.Request(response.urljoin("https://www.wsws.org" + monthLink), callback = self.parseMonth)
                break

    def parseMonth(self, response):
        for link in response.css('div.category ul li ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback=self.parseNews)

    def parseNews(self, response):
        header = response.css("#content h2 ::text").get()
        content = response.css("#content p ::text").extract()
        time = response.css("#content h5 ::text").extract()[-1]
        try:
            engLink = response.css("#content h4 ::attr(href)").getall()
            name = str(randrange(1000000))
            if len(engLink) > 0:
                yield scrapy.Request(response.urljoin(engLink[0] + "?" + parse.urlencode({"name": name})), callback=self.parseEngNews)
        except Exception:
            engLink = response.css("#content h5 ::attr(href)").getall()
            name = str(time) + str(randrange(1000000))
            if len(engLink) > 0:
                yield scrapy.Request(response.urljoin(engLink[0] + "?" + parse.urlencode({"name": name})), callback=self.parseEngNews)

        url = response.url
        self.writeToJson(header, time, content, name, url)

    def parseEngNews(self, response):
        header = response.css("div.clearfix div h2 ::text").getall()[1]
        content = response.css("div.clearfix p ::text").getall()
        time = response.css('div.clearfix h5 ::text').getall()[-1]
        parsed = urlparse(response.url)
        name = parse_qs(parsed.query)["name"][0]
        url = response.url
        self.writeEngToJson(header, time, content, name, url)
