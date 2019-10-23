import scrapy


class IMDBSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/search/title/?title=a'
    ]

    def parse(self, response):
        for movie in response.css('.lister-item'):
            item_content = movie.css('.lister-item-content')
            header = item_content.css('.lister-item-header')
            link = header.css('a:nth-child(2)')
            
            yield {
                'title': link.css('::text').get(),
                'url': link.css('::attr(href)').get(),
                'year': header.css('.lister-item-year.text-muted.unbold::text').get(),
                'rating': item_content.css('.ratings-bar > .inline-block > strong::text').get(),
                'synopsis': item_content.css('p:nth-child(4)::text').get(),
                'image': movie.css('img.loadlate::attr(src)').get()
            }


        next_page = response.css('.next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


