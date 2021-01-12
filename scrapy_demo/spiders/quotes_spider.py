import scrapy
from scrapy_demo.items import ScrapyDemoItem

class QuotesSpider(scrapy.Spider):

    name = 'eastbay'
    start_urls = ['https://www.eastbay.com/category/sale.html?query=sale%3Arelevance%3AstyleDiscountPercent%3ASALE%3Agender%3AMen%27s%3Abrand%3AASICS+Tiger']

    def parse(self, response):
	li_list = response.css('ul.row.row-2cols--xs.row-3cols--sm.row-4cols--lg.gutter').css('li')
        for li in li_list:
	    detail_url = li.css('div.ProductCard a::attr(href)').extract_first()
            if detail_url is not None:
                yield scrapy.Request(
		    response.urljoin(detail_url),
                    callback=self.parse_detail
                )

    def parse_detail(self, response):
	a_item = ScrapyDemoItem()
        a_item["title"] = response.css('.ProductName-primary::text').get()
        a_item["price"] = response.css('.ProductPrice-final::text').get()
        a_item["size"] = response.css('.c-form-label-content::text').get()        
        yield a_item 
