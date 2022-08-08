import scrapy

class XPATHSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        quote = response.css('div.quote')
        yield {
            'text':quote.xpath("//span[@class='text']/text()").extract(),
            'author':quote.xpath("//small[@class='author']/text()").extract(),
            'tags':quote.xpath("//div[@class='tag']/text() /a[@class='tag']/text()").extract(),
        }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)