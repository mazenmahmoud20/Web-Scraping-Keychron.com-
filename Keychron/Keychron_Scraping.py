import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

CSV_FILE="Keychron.csv"

class KScraperSpider(CrawlSpider):

    name = "k_scraper"
    start_urls = ["https://www.keychron.com/collections/all-products"]
    custom_settings={
        'FEEDS':{
            CSV_FILE:{
                'format':'csv',
                'encoding':'utf-8'
            }
        }
    }
    rules=(
        Rule(LinkExtractor(allow='/products',deny=['keychron-add-on','keychron-gift-card']),callback='parse_item'),
        )
    

    def parse_item(self, response):
        items=json.loads(response.css('script[type="application/ld+json"]::text').get())
        for item in items['offers']:
            yield{
                'Name':items['name'],
                'Version':item['name'],
                'Price':item['price'],
                'PriceCurrency':item['priceCurrency'],
                'Availability':item['availability'].replace('https://schema.org/',''),
                'Model':item['sku'],
                'Link':item['url']
            }

process=CrawlerProcess()
process.crawl(KScraperSpider)
process.start()