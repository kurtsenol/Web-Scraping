import scrapy
from scrapy.loader import ItemLoader
from quotes.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']


    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        # quotes = response.xpath("//div[@class='quote']")
        quotes = response.css('div.quote')

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            # pay attention to the dot .// to use relative xpath
            # loader.add_xpath('quote_content', ".//span[@class='text']/text()")
            loader.add_css('quote_content', '.text::text')
            # loader.add_xpath('author', './/small//text()')
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()
            author_url = quote.css('.author + a::attr(href)').get()
            # go to the author page and pass the current collected quote info
            yield response.follow(author_url, self.parse_author, meta={'quote_item': quote_item}, dont_filter =True)

        # go to Next page
        for a in response.css('li.next a'):
            yield response.follow(a, self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_bornlocation', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')
        yield loader.load_item()



#♦ scrape without itemloader
# =============================================================================
#         for quote in quotes:
#             yield {
#                 'text': quote.css('.text::text').get(),
#                 'author': quote.css('.author::text').get(),
#                 'tags': quote.css('.tag::text').getall(),
#             }
#             
#             
#             author_url = quote.css('.author + a::attr(href)').get()
#             self.logger.info('get author page url')
#             
#             # go to the author page
#             yield response.follow(author_url, callback=self.parse_author)
#         
#         #scrape all next pages
#         yield from response.follow_all(css='li.next a', callback=self.parse)
# =============================================================================

        
# scrape all next pages  
# =============================================================================
#         for a in response.css('li.next a'):
#             yield response.follow(a, callback=self.parse)
# =============================================================================

# scrape all next pages  
# =============================================================================
#         next_page = response.css('li.next a::attr(href)').get()
# 
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)
# =============================================================================


# scrape all next pages          
# =============================================================================
#         next_page = response.css('li.next a::attr(href)').get()
# 
#         if next_page:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)
# =============================================================================

    # def parse_author(self, response):
    #     yield {
    #         'author_name': response.css('.author-title::text').get(),
    #         'author_birthday': response.css('.author-born-date::text').get(),
    #         'author_bornlocation': response.css('.author-born-location::text').get(),
    #         'author_bio': response.css('.author-description::text').get(),
    #     }    