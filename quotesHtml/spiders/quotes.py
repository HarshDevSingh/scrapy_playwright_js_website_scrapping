import scrapy
from scrapy_playwright.page import PageMethod
from quotesHtml.items import QuoteshtmlItem
from scrapy.loader import ItemLoader


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/js/",
            meta=dict(playwright=True,
                      playwright_include_page=True,
                      playwright_page_methods=[
                          PageMethod("wait_for_selector", '//div[contains(@class, "quote")]'),
                      ],
                      ),
            errback=self.errback_close_page
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        quotes_list = response.xpath('//div[contains(@class, "quote")]')
        for quote in quotes_list:
            item = ItemLoader(item=QuoteshtmlItem(), selector=quote)
            item.add_xpath('author', './/span/small[contains(@class, "author")]/text()')
            item.add_xpath('quote', './/span[contains(@class, "text")]/text()')
            yield item.load_item()

        if response.xpath('//li[contains(@class,"next")]'):
            next_page_url = response.urljoin(response.xpath('//li[contains(@class, "next")]/a/@href').get())
            yield scrapy.Request(url=next_page_url,
                                 meta=dict(playwright=True,
                                           playwright_include_page=True,
                                           playwright_page_methods=[
                                               PageMethod("wait_for_selector", '//div[contains(@class, "quote")]'),
                                           ],
                                           ),
                                 errback=self.errback_close_page
                                 )

    async def errback_close_page(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
