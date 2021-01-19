import scrapy

class FloralesSpider(scrapy.Spider):
    name = 'florales'
    start_urls = ['https://web.archive.org/web/20200922142824/http://www.floralesmisioneras.com/']

    def parse(self, response):
        #links = response.css('#imPageExtContainer a::attr(href)')
        links = response.css('#imHeader_imMenuObject_04_container > ul > li:nth-child(3) > div.multiple-column > ul > li:nth-child(4) > ul > li:nth-child(2) > ul > li:nth-child(2) > ul a::attr(href)')
        yield from response.follow_all(links, self.parse_item)

    def parse_item(self, response):
        title = response.css('#imPgTitle::text').get()
        yield {
                'title': title if title else response.css('title::text').get(),
                'content': '\n'.join(response.css('#imContent > *:not(script):not(header):not(a)').getall())
        }

