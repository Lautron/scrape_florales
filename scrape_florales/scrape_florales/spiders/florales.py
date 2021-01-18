import scrapy

class FloralesSpider(scrapy.Spider):
    name = 'florales'
    start_urls = ['https://web.archive.org/web/20200922142824/http://www.floralesmisioneras.com/']

    def parse(self, response):
        links = response.css('#imPageExtContainer a::attr(href)')
        yield from response.follow_all(links, self.parse_item)

    def parse_item(self, response):
        title = response.css('#imPgTitle::text').get()
        yield {
                'title': title if title else response.css('title::text').get(),
                'content': '\n'.join([res.get() for res in response.css('#imContent *:not(#imPgTitle)') if not res.get().startswith('<script>')]),
        }
