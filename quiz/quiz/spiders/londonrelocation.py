import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..items import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                        callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                        callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        boxes = response.xpath("//div[@class='test-box']")
        for box in boxes :
            title = boxes.xpath("normalize-space(.//div[@class='h4-space']/h4/a/text())").get()
            price = boxes.xpath(".//div[@class='bottom-ic']/h5/text()").get()
            link =  box.xpath(".//div[@class='h4-space']/h4/a/@href").get()
            abs_link = response.urljoin(link)
            property = ItemLoader(item=Property(), selector= box)
            property.add_value('title', title)
            property.add_value('price', price)
            property.add_value('link', abs_link)
            yield property.load_item()

        next_page = response.xpath("(//div[@class='pagination']/ul/li)[3]/a/@href").get()

        if next_page:
            yield Request(url=next_page, callback=self.parse_area_pages)