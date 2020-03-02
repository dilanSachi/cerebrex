from scrapy.crawler import CrawlerProcess
import schedule 
import time
import DailyNewsBot, DinaminaBot, ThinakaranBot, ArmyEnglishBot, ArmySinhalaBot, ArmyTamilBot, HiruSinhalaBot, HiruTamilBot,\
    HiruEnglishBot, ITNEnglishBot, ITNSinhalaBot, ITNTamilBot, NewsFirstEnglishBot, NewsFirstSinhalaBot, NewsFirstTamilBot

def rundaily():
    process = CrawlerProcess()
    # process.crawl(ArmyEnglishBot.ArmyEnglishBot)
    # process.crawl(ArmySinhalaBot.ArmySinhalaBot)
    # process.crawl(ArmyTamilBot.ArmyTamilBot)
    # process.crawl(DailyNewsBot.DailyNewsBot)
    # process.crawl(DinaminaBot.DinaminaBot)
    # process.crawl(ThinakaranBot.ThinakaranBot)
    # process.crawl(HiruSinhalaBot.HiruSinhalaBot)
    # process.crawl(HiruTamilBot.HiruTamilBot)
    # process.crawl(HiruEnglishBot.HiruEnglishBot)
    # process.crawl(ITNEnglishBot.ITNEnglishBot)
    # process.crawl(ITNSinhalaBot.ITNSinhalaBot)
    # process.crawl(ITNTamilBot.ITNTamilBot)
    # process.crawl(NewsFirstEnglishBot.NewsFirstEnglishBot)
    # process.crawl(NewsFirstSinhalaBot.NewsFirstSinhalaBot)
    process.crawl(NewsFirstTamilBot.NewsFirstTamilBot)
    process.start()

schedule.every().day.at("23:11").do(rundaily)

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