import scrapy
from pathlib import Path
from random import randrange
import json
import datetime

class HiruSinhalaBot(scrapy.Spider):
    name = "HiruSinhalaBot"

    start_urls = [
        'http://www.hirunews.lk/sinhala/local-news.php',
        'http://www.hirunews.lk/sinhala/international-news.php'
    ]
    oldLocalLink = ""
    oldInternationalLink = ""

    def writeToJson(self, header, time, content, docId, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../../data/hirunews/bot/sinhala").mkdir(parents=True, exist_ok=True)
        with open("../../../data/hirunews/bot/sinhala/" + docId + ".json", 'a', encoding="utf8") as ofile:
            json.dump(obj, ofile, ensure_ascii=False)

    def parse(self, response):
        crawled = ""
        with open("CrawlerLinks.json") as crawledlinks:
            crawled=json.load(crawledlinks)

        allnew = True
        newsLinks = response.css('div.all-section-tittle ::attr(href)').getall()
        if (len(newsLinks) > 0):
            firstlink = newsLinks[0]

            url = response.url
            if("local-news" in url):
                self.oldLocalLink = crawled["hirusinhalalocal"]
                crawled["hirusinhalalocal"] = firstlink
            elif("international-news" in url):
                self.oldInternationalLink = crawled["hirusinhalainternational"]
                crawled["hirusinhalainternational"] = firstlink
            else:
                print("no relatable link found")

            for link in newsLinks:
                if link is not None:
                    if (self.oldLocalLink != link and self.oldInternationalLink != link):
                        yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                    else:
                        allnew = False
                        break
            if (allnew):
                titlelist = response.css('div.pagi ::attr(title)').getall()
                linklist = response.css('div.pagi ::attr(href)').getall()
                for i in range(0, len(titlelist)):
                    if (titlelist[i] == 'next page'):
                        yield scrapy.Request(linklist[i], self.parseRestPages)
            with open("CrawlerLinks.json", 'w+', encoding="utf8") as outfile:
                json.dump(crawled, outfile, ensure_ascii=False)
        else:
            titlelist = response.css('div.pagi ::attr(title)').getall()
            linklist = response.css('div.pagi ::attr(href)').getall()
            for i in range(0, len(titlelist)):
                if (titlelist[i] == 'next page'):
                    yield scrapy.Request(linklist[i], self.parse)
    
    def parseRestPages(self, response):
        allnew = True
        for link in response.css('div.all-section-tittle ::attr(href)').getall():
            if link is not None:
                if (self.oldLocalLink != link and self.oldInternationalLink != link):
                    yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
                else:
                    allnew = False
                    break
        if (allnew):
            titlelist = response.css('div.pagi ::attr(title)').getall()
            linklist = response.css('div.pagi ::attr(href)').getall()
            for i in range(0, len(titlelist)):
                if (titlelist[i] == 'next page'):
                    yield scrapy.Request(linklist[i], self.parseRestPages)

    def parseNews(self, response):
        header = response.css("div.container center h1 ::text").get()
        time = response.css("div.container center p ::text").get()
        content = response.css("#article-phara ::text").getall()
        docId = response.url.split("/")[4]
        url = response.url
        self.writeToJson(header, time, content, docId, url)
