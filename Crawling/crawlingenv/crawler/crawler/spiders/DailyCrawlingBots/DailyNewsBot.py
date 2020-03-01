import scrapy
from pathlib import Path
from random import randrange
from scrapy.http import FormRequest
import json
import datetime

class DailyNewsBot(scrapy.Spider):
    name = "DailyNewsBot"

    start_urls = [
        'http://www.dailynews.lk/date/'
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

        Path("../../../data/dailynews/bot/english").mkdir(parents=True, exist_ok=True)
        with open("../../../data/dailynews/bot/english/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as ofile:  
            json.dump(obj, ofile, ensure_ascii=False)

    def parse(self, response):
        crawled = ""
        with open("CrawlerLinks.json") as crawledlinks:
            crawled=json.load(crawledlinks)

        allnew = True
        newsLinks = response.css('span.field-content ::attr(href)').getall()
        if (len(newsLinks) > 0):
            firstlink = newsLinks[0]
            print(crawled)
            self.oldLink = crawled["dailynews"]
            crawled["dailynews"] = firstlink

            for link in newsLinks:
                if link is not None:
                    if (self.oldLink != link):
                        yield scrapy.Request(response.urljoin("http://www.dailynews.lk" + link), callback = self.parseNews)
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
                    yield scrapy.Request(response.urljoin("http://www.dailynews.lk" + link), callback = self.parseNews)
                else:
                    allnew = False
                    break
        if (allnew):
            yield scrapy.Request(response.urljoin(response.css("li.date-prev a ::attr(href)").get()), callback=self.parseRestPages)

    def parseNews(self, response):
        header = response.css("div.clearfix h1 ::text").get()
        content = response.css("div.field-items p ::text").getall()
        time = response.url.split("/")[3] + "/" + response.url.split("/")[4] + "/" + response.url.split("/")[5]
        url = response.url
        self.writeToJson(header, time, content, url)
