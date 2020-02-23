import scrapy
import json
from pathlib import Path
from random import randrange

class NewsFirstEnglishCrawler(scrapy.Spider):
    name = "NewsFirstEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.newsfirst.lk/latest-news/'
    ]

    def writeToJson(self, header, time, content):
        obj = {  
            'Header': header,
            'Time': time,
            'Content': content
        }
        # self.data['news'].append({  
        #     'Header': header,
        #     'Time': time,
        #     'Content': content
        # })

        Path("./data/news_first/english").mkdir(parents=True, exist_ok=True)

        with open("./data/news_first/english/" + str(randrange(10000000)) + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        newslist = response.css('div.sub-1-news-block ::attr(href)').getall()
        for i in range(0, len(newslist), 2):
            if newslist[i] is not None:
                yield scrapy.Request(response.urljoin(newslist[i]), callback = self.parseNews)
        newslist2 = response.css('div.main-news-heading ::attr(href)').getall()
        for i in range(0, len(newslist2)):
            if newslist2[i] is not None:
                yield scrapy.Request(response.urljoin(newslist2[i]), callback = self.parseNews)
        yield scrapy.Request(response.css("a.next ::attr(href)").get(), self.parse)

    def parseNews(self, response):
        header = response.css("h1.text-left ::text").getall()
        content = response.css("div.w-300 p ::text").getall()
        time = response.css('p.artical-new-byline ::text').getall()[1:]
        self.writeToJson(header, time, content)
