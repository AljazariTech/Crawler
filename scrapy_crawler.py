import scrapy

class FridgeSpider(scrapy.Spider):
    name = "fridges"
    start_urls = [
        'https://www.zap.co.il/models.aspx?sog=e-fridge',
    ]

    def parse(self, response):
        for product in response.css('div.ModelRow'):
            title = product.css('a.ModelTitle::text').get()
            prices = product.css('.price-wrapper span::text').get().split('-')
            yield {
                'title': title.strip() if title else title,
                'lowest': int(prices[1].strip().replace(',', '').replace('₪', '').strip()) if len(prices) > 1 else None,
                'highest': int(prices[0].strip().replace(',', '').replace('₪', '').strip()) if prices else None
            }

        next_page = response.css('a.Next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
