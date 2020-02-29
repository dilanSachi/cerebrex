import scrapy
from scrapy.crawler import CrawlerProcess
import schedule 
import time
import DailyNewsBot, DinaminaBot, ThinakaranBot, ArmyEnglishBot, ArmySinhalaBot, ArmyTamilBot

def rundaily():
    process = CrawlerProcess()
    # process.crawl(ArmyEnglishBot.ArmyEnglishBot)
    # process.crawl(ArmySinhalaBot.ArmySinhalaBot)
    # process.crawl(ArmyTamilBot.ArmyTamilBot)
    # process.crawl(DailyNewsBot.DailyNewsBot)
    # process.crawl(DinaminaBot.DinaminaBot)
    process.crawl(ThinakaranBot.ThinakaranBot)
    process.start()

schedule.every().day.at("20:43").do(rundaily)

while True: 
  
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending()
    time.sleep(1)
    print("running")


# print("------------------------------------------------------------------------------")
# print(self.oldLink)
# print(link)
# print("------------------------------------------------------------------------------")