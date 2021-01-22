import scrapy

class FloralesSpider(scrapy.Spider):
    name = 'florales'
    #start_urls = ['https://web.archive.org/web/20200922142824/http://www.floralesmisioneras.com/']
    def __init__(self, *args, **kwargs): 
          super(FloralesSpider, self).__init__(*args, **kwargs) 

          self.start_urls = [kwargs.get('url')] 
    def parse(self, response):
        links = response.css('#imContent a::attr(href)')
        yield from response.follow_all(links, self.parse_item)

    def parse_item(self, response):
        title = response.css('#imPgTitle::text').get()
        yield {
                'title': title if title else response.css('title::text').get(),
                'content': '\n'.join(response.css('#imContent > *:not(script):not(header):not(a)').getall())
        }

