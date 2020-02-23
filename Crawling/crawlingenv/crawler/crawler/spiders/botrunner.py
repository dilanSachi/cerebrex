import scrapy
from scrapy.crawler import CrawlerProcess
import schedule 
import time

from DailyCrawlingBots import ArmyEnglishBot

def rundaily():
    process = CrawlerProcess()
    process.crawl(ArmyEnglishBot.ArmyEnglishBot)
    process.start()

schedule.every().day.at("15:07").do(rundaily) 

while True: 
  
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending()
    time.sleep(1)
    print("running")