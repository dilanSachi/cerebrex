import scrapy
import json

class HiruEnglishCrawler(scrapy.Spider):
    name = "HiruEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'http://www.hirunews.lk/',
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
        for link in response.css('div.lts-cntp ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        print(response.css('div.pagi ::attr(title)').getall()[-1])
        titlelist = response.css('div.pagi ::attr(title)').getall()
        linklist = response.css('div.pagi ::attr(href)').getall()
        for i in range(0, len(titlelist)):
            if (titlelist[i] == 'next page'):
                yield scrapy.Request(linklist[i], self.parse)

    def parseNews(self, response):
        header = response.css("div.lts-cntp2 ::text").getall()
        content = response.css("div.lts-txt2 ::text").getall()
        time = response.css('div.time ::text').get()
        docId = response.url.split("/")[3]
        self.writeToJson(header, time, content, docId)
