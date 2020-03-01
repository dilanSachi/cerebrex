import scrapy
from pathlib import Path
from random import randrange
import json
import datetime

class DinaminaBot(scrapy.Spider):
    name = "DinaminaBot"

    start_urls = [
        'http://www.dinamina.lk/date/'
    ]
    oldLink = ""

    def start_requests(self):
        tomorrowDate = str(datetime.date.today()+datetime.timedelta(days=1))
        yield scrapy.Request(self.start_urls[0] + tomorrowDate, callback=self.parse)

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../../data/dailynews/bot/sinhala").mkdir(parents=True, exist_ok=True)
        with open("../../../data/dailynews/bot/sinhala/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as ofile:  
            json.dump(obj, ofile, ensure_ascii=False)

    def parse(self, response):
        crawled = ""
        with open("CrawlerLinks.json") as crawledlinks:
            crawled=json.load(crawledlinks)

        allnew = True
        newsLinks = response.css('#main span.field-content a ::attr(href)').getall()
        if (len(newsLinks) > 0):
            firstlink = newsLinks[0]
            url = response.url
            print(crawled)
            self.oldLink = crawled["dinamina"]
            crawled["dinamina"] = firstlink

            for link in newsLinks:
                if link is not None:
                    if (self.oldLink != link):
                        yield scrapy.Request(response.urljoin("http://www.dinamina.lk" + link), callback = self.parseNews)
                    else:
                        allnew = False
                        break
            if (allnew):
                yield scrapy.Request(response.css("li.date-prev a ::attr(href)").getall()[0], callback=self.parseRestPages)
            with open("CrawlerLinks.json", 'w+', encoding="utf8") as outfile:
                json.dump(crawled, outfile, ensure_ascii=False)
        else:
            yield scrapy.Request(response.css("li.date-prev a ::attr(href)").getall()[0], callback=self.parse)

    def parseRestPages(self, response):
        allnew = True
        for link in response.css('span.field-content ::attr(href)').getall():
            if link is not None:
                if (self.oldLink != link):
                    yield scrapy.Request(response.urljoin("http://www.dinamina.lk" + link), callback = self.parseNews)
                else:
                    allnew = False
                    break
        if (allnew):
            yield scrapy.Request(response.css("li.date-prev a ::attr(href)").getall()[0], callback=self.parseRestPages)

    def parseNews(self, response):
        header = response.css("div.clearfix h1 ::text").get()
        content = response.css("div.field-items div.even div ::text").getall()
        time = response.css("span.date-display-single ::text").get()
        url = response.url
        self.writeToJson(header, time, content, url)
