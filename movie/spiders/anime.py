import scrapy
from scrapy import signals
from pydispatch import dispatcher
import json

class QuotesSpider(scrapy.Spider):
    name = "onepiece"
    resutls = []

    start_urls = [
        'https://myanimelist.net/anime/21/One_Piece/episode?offset=0',
    ]

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    
    def parse(self, resonse):
        for i in range(0, 1001, 100):
            nextPage = self.start_urls[0].split('=')[0]+"="+str(i)
            yield scrapy.Request(url=nextPage, callback=self.parseEp)

    def parseEp(self, response):
        for episode in response.css("tr.episode-list-data"):
            num = episode.css("td.episode-number::text").get()
            title = episode.css('td.episode-title > a::text').get()
            aired = episode.css('td.episode-aired::text').get()
            vote =  episode.css('td.episode-poll::attr(data-raw)').get()
            watched = "No"

            self.resutls.append({"num":num, "info": {"title":title, "aired":aired, "vote":vote}})
        
    
    def spider_closed(self, spider):
        with open('onepiece.json', 'w') as fp:
            self.resutls = sorted(self.resutls, key=lambda d: int(d['num']))
            json.dump(self.resutls, fp)
            print("saved!")







#css selectors:
#info: response.css("tr.episode-list-data")

