import scrapy

class SixSpider(scrapy.Spider):
    name = "six"
    allowed_domains = [""]
    start_urls = [

    ]

    def parse(self, response):
        return 1
