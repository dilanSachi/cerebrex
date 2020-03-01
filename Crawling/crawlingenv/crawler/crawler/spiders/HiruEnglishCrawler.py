import scrapy
import json
from pathlib import Path

class HiruEnglishCrawler(scrapy.Spider):
    name = "HiruEnglishCrawler"

    data = {}
    data['news'] = []

    start_urls = [
        'http://www.hirunews.lk/international-news.php',
        'http://www.hirunews.lk/local-news.php'
    ]

    def writeToJson(self, header, time, content, docId, url):
        obj = {  
            'Header': header,
            'Time': time,
            'Url': url,
            'Content': content
        }
        Path("./data/hiru_news/english").mkdir(parents=True, exist_ok=True)
        with open("./data/hiru_news/english/" + docId + ".json", 'a', encoding="utf8") as outfile:  
            json.dump(obj, outfile, ensure_ascii=False)

    def parse(self, response):
        for link in response.css('div.all-section-tittle ::attr(href)').getall():
            if link is not None:
                yield scrapy.Request(response.urljoin(link), callback = self.parseNews)
        titlelist = response.css('div.pagi ::attr(title)').getall()
        linklist = response.css('div.pagi ::attr(href)').getall()
        for i in range(0, len(titlelist)):
            if (titlelist[i] == 'next page'):
                yield scrapy.Request(linklist[i], self.parse)

    def parseNews(self, response):
        header = response.css("div.container center h1 ::text").get()
        time = response.css("div.container center p ::text").get()
        content = response.css("#article-phara ::text").getall()
        docId = response.url.split("/")[3]
        url = response.url
        self.writeToJson(header, time, content, docId, url)