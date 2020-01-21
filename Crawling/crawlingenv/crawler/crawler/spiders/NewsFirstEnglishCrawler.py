import scrapy
import json

class NewsFirstEnglishCrawler(scrapy.Spider):
    name = "NewsFirstEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://www.newsfirst.lk/sinhala/latest-news/',
    ]

    def writeToJson(self, header, time, content, docId):
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

        with open("./data/hiru_news/" + docId + ".json", 'a') as outfile:  
            json.dump(obj, outfile)

    def parse(self, response):
        newslist = response.css('div.sub-1-news-block ::attr(href)').getall()
        for i in range(0, len(newslist), 2):
            if newslist[i] is not None:
                yield scrapy.Request(response.urljoin(newslist[i]), callback = self.parseNews)
        newslist2 = response.css('div.main-news-heading ::attr(href)').getall()
        for i in range(0, len(newslist2)):
            if newslist2[i] is not None:
                yield scrapy.Request(response.urljoin(newslist2[i]), callback = self.parseNews)
        yield scrapy.Request(response.css('ul.pagination ::attr(title)').getall()[-1], self.parse)

    def parseNews(self, response):
        header = response.css("div.lts-cntp2 ::text").getall()
        content = response.css("div.lts-txt2 ::text").getall()
        time = response.css('div.time ::text').get()
        docId = response.url.split("/")[3]
        self.writeToJson(header, time, content, docId)
