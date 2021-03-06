import scrapy
import json
import io
from pathlib import Path
from random import randrange
import time
from scrapy.http import FormRequest
import json

class ArmyTamilBot(scrapy.Spider):
    name = "ArmyTamilBot"

    start_urls = [
        'https://www.army.lk/ta/ta-photo-story',
        'https://www.army.lk/ta/ta-news-highlight',
        'https://www.army.lk/ta/ta-news-features'
    ]
    oldPhotoStoryLink = ""
    oldHighlightLink = ""
    oldFeaturesLink = ""

    def writeToJson(self, header, time, content, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }

        Path("../../data/army/bot/tamil").mkdir(parents=True, exist_ok=True)
        with open("../../data/army/bot/tamil/" + str(randrange(1000000)) + ".json", 'a', encoding="utf8") as ofile:  
            json.dump(obj, ofile, ensure_ascii=False)

    def parse(self, response):
        crawled = ""
        with open("./DailyCrawlingBots/CrawlerLinks.json") as crawledlinks:
            crawled=json.load(crawledlinks)

        allnew = True
        firstlink = response.css('ul.cVerticleList li h4 a ::attr(href)').getall()[0]
        url = response.url
        if("photo-story" in url):
            self.oldPhotoStoryLink = crawled["armytamilphotostory"]
            crawled["armytamilphotostory"] = firstlink
        elif("news-highlight" in url):
            self.oldHighlightLink = crawled["armytamilnewshighlight"]
            crawled["armytamilnewshighlight"] = firstlink
        elif("news-features" in url):
            self.oldFeaturesLink = crawled["armytamilnewsfeatures"]
            crawled["armytamilnewsfeatures"] = firstlink
        else:
            print("no relatable link found")

        for link in response.css('ul.cVerticleList li h4 a ::attr(href)').getall():
            if link is not None:
                if (self.oldFeaturesLink != link and self.oldHighlightLink != link and self.oldPhotoStoryLink != link):
                    yield scrapy.Request(response.urljoin("https://www.army.lk/ta/" + link), callback = self.parseNews)
                else:
                    allnew = False
                    
                    break
        if (allnew):
            yield scrapy.Request(response.urljoin(response.css("li.next ::attr(href)").get()), callback=self.parseRestPages)
        with open("./DailyCrawlingBots/CrawlerLinks.json", 'w+', encoding="utf8") as outfile:
            json.dump(crawled, outfile, ensure_ascii=False)
    
    def parseRestPages(self, response):
        allnew = True

        for link in response.css('ul.cVerticleList li h4 a ::attr(href)').getall():
            if link is not None:
                if (self.oldFeaturesLink != link and self.oldHighlightLink != link and self.oldPhotoStoryLink != link):
                    yield scrapy.Request(response.urljoin("https://www.army.lk/ta/" + link), callback = self.parseNews)
                else:
                    allnew = False
                    break
        if (allnew):
            yield scrapy.Request(response.urljoin(response.css("li.next ::attr(href)").get()), callback=self.parseRestPages)

    def parseNews(self, response):
        header = response.css("div.container h1 ::text").get()
        content = response.css("div.container p ::text").getall()
        time = response.css("div.container p.cDate ::text").get()
        url = response.url
        self.writeToJson(header, time, content, url)
