import scrapy
from bookscrapper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    #We can write this in our setings.py file too, overwrite is for overwriting feed of settings.py
    # custom_setting={
    #     'FEEDS' : {'booksdata.json':{'format':'json', overwrite=True}},
    # }

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        page=response.css(".product_page")
        table_rows=page.css("table tr")
        book_item=BookItem()

        
        book_item['url'] = response.url,
        print("********************")
        print(response.url)
        print("********************")
        book_item['title']= page.css("div.product_main h1::text").get(),
        book_item['upc'] = table_rows[0].css("td::text").get(),
        book_item['product_type'] = table_rows[1].css("td::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css('td::text').get(),
        book_item['price_incl_tax'] = table_rows[3].css('td::text').get(), 
        book_item['tax'] =  table_rows[4].css('td::text').get(),
        book_item['availability'] = table_rows[5].css('td::text').get(),
        book_item['num_reviews'] = table_rows[6].css('td::text').get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css("p.price_color::text").get()
        
        yield book_item

