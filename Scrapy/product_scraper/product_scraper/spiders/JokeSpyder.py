import scrapy

from product_scraper.items import JokeItem

class JokeSpyder(scrapy.Spider):
    name = 'JokeSpyder'
    #allowed_domains = ['www.laughfactory.com/jokes/family-jokes']
    start_urls = ['http://www.laughfactory.com/jokes/family-jokes/']


    def parse(self, response):
        
        #item = JokeItem()
        
        
        for joke in response.xpath(".//div[@class='joke-text']/p/text()").extract():
            yield {
                'joke_text': joke.strip()
            }
        
        # for joke in response.xpath(".//div[@class='joke-text']/p/text()").extract():
        #     item["joke_text"]=joke.strip()
        #     yield item
        
        next_page= response.xpath("//li[@class='next']/a/@href")
        if next_page:
            next_page_link= next_page.extract_first()
            yield scrapy.Request(url=next_page_link, callback=self.parse)
