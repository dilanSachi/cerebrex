import scrapy
from pathlib import Path
from random import randrange
import json
import datetime

class ITNSinhalaBot(scrapy.Spider):
    name = "ITNSinhalaBot"

    start_urls = [
        'https://www.itnnews.lk/local/',
        'https://www.itnnews.lk/international/',
        'https://www.itnnews.lk/business/',
        'https://www.itnnews.lk/sports/',
        'https://www.itnnews.lk/entertainment/'
    ]
    oldLocalLink = ""
    oldInternationalLink = ""
    oldBusinessLink = ""
    oldSportsLink = ""
    oldEntertainmentLink = ""

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../../data/itn/bot/sinhala").mkdir(parents=True, exist_ok=True)
        with open("../../../data/itn/bot/sinhala/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as ofile:
            json.dump(obj, ofile, ensure_ascii=False)

    def parse(self, response):
        crawled = ""
        with open("CrawlerLinks.json") as crawledlinks:
            crawled=json.load(crawledlinks)

        allnew = True
        newsLinks = response.css('div.block-content a.more ::attr(href)').getall()
        if (len(newsLinks) > 0):
            firstlink = newsLinks[0]

            url = response.url
            if("local" in url):
                self.oldLocalLink = crawled["itnsinhalalocal"]
                crawled["itnsinhalalocal"] = firstlink
            elif("entertainment" in url):
                self.oldEntertainmentLink = crawled["itnsinhalaentertainment"]
                crawled["itnsinhalaentertainment"] = firstlink
            elif("international" in url):
                self.oldInternationalLink = crawled["itnsinhalainternational"]
                crawled["itnsinhalainternational"] = firstlink
            elif("business" in url):
                self.oldBusinessLink = crawled["itnsinhalabusiness"]
                crawled["itnsinhalabusiness"] = firstlink
            elif("sports" in url):
                self.oldSportsLink = crawled["itnsinhalasports"]
                crawled["itnsinhalasports"] = firstlink
            else:
                print("no relatable link found")

            for link in newsLinks:
                if link is not None:
                    if (self.oldLocalLink != link and self.oldInternationalLink != link and
                            self.oldBusinessLink != link and self.oldEntertainmentLink != link and self.oldSportsLink != link):
                        yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                    else:
                        allnew = False
                        break
            if (allnew):
                yield scrapy.Request(response.css('a.next ::attr(href)').get(), self.parseRestPages)
            with open("CrawlerLinks.json", 'w+', encoding="utf8") as outfile:
                json.dump(crawled, outfile, ensure_ascii=False)
        else:
            yield scrapy.Request(response.css('a.next ::attr(href)').get(), self.parse)
    
    def parseRestPages(self, response):
        allnew = True
        for link in response.css('div.block-content a.more ::attr(href)').getall():
            if link is not None:
                if (self.oldLocalLink != link and self.oldInternationalLink != link and
                        self.oldBusinessLink != link and self.oldEntertainmentLink != link and self.oldSportsLink != link):
                    yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                else:
                    allnew = False
                    break
        if (allnew):
            yield scrapy.Request(response.css('a.next ::attr(href)').get(), self.parseRestPages)

    def parseNews(self, response):
        header = response.css("div.article-title h1 ::text").get()
        content = response.css("div.column9 ::text").getall()
        time = response.css('div.a-content span.meta ::text').get()
        url = response.url
        self.writeToJson(header, time, content, url)
