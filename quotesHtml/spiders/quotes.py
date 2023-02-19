import scrapy
from scrapy_playwright.page import PageMethod


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
            author = quote.xpath('.//span/small[contains(@class, "author")]/text()').get()
            text = quote.xpath('.//span[contains(@class, "text")]/text()').get()
            yield {"author": author,
                   "quote": text}
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
