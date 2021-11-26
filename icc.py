from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class icc(CrawlSpider):
    name = 'icc_rank'
    allowed_domains = ['icc-cricket.com']
    start_urls = ['https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting']
    rules = [Rule(LinkExtractor(allow='rankings/mens',deny='player-rankings')),
            Rule(LinkExtractor(allow='player-rankings'),callback='parse_item', follow=True)]
     
    def parse_item(self,response):
        yield{
            'Name':response.xpath('//h2[@class="rankings-player-bio__name"]/text()').extract()[0],
            'DOB':response.xpath('//span[@class="rankings-player-bio__entry"]/text()').extract()[0],
            'Role':response.xpath('//span[@class="rankings-player-bio__entry"]/text()').extract()[1],
            'Batting_Style':response.xpath('//span[@class="rankings-player-bio__entry"]/text()').extract()[2],
            'Bowling_style':response.xpath('//span[@class="rankings-player-bio__entry"]/text()').extract()[3]
        }

from scrapy.crawler import CrawlerProcess

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
    'DEPTH_LIMIT': 2,
    'CLOSESPIDER_PAGECOUNT': 3,


})
c.crawl(icc, urls_file='input.txt')
c.start()