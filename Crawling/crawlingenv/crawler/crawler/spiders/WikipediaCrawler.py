import scrapy
import json

class WikipediaCrawler(scrapy.Spider):
    name = "WikipediaCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'https://si.wikipedia.org/wiki/%E0%B7%80%E0%B7%92%E0%B7%81%E0%B7%9A%E0%B7%82:%E0%B7%83%E0%B7%92%E0%B6%BA%E0%B7%85%E0%B7%94_%E0%B6%B4%E0%B7%92%E0%B6%A7%E0%B7%94',
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
        for link in response.css('div.mw-allpages-body ::attr(href)').getall():
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
