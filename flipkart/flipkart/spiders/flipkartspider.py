import scrapy
from scrapy import Request
import re
from ..items import FlipkartItem


class FlipkartspiderSpider(scrapy.Spider):
    name = 'flipkartspider'
    count = 1
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    #allowed_domains = ['flipkart.com']
    #start_urls = ['http://flipkart.com/']

    def start_requests(self):
        start_url = "https://www.flipkart.com/search?q=headphone"
        yield scrapy.Request(start_url, headers=self.headers, callback=self.product_page_list, dont_filter=True)

    def product_page_list(self, response):
        meta = response.meta
        product_links = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div/a[2]/@href').extract()

        for product_link in product_links:
            product_link = "https://www.flipkart.com" + product_link
            meta['product_link'] = product_link
            yield Request(product_link, headers=self.headers, callback=self.product_page, dont_filter=True, meta=meta)

        next_page = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[12]/div/div/nav/a[11]/@href').extract_first()
        if next_page:
            next_page_link = "https://www.flipkart.com" + next_page
            FlipkartspiderSpider.count+=1
            if FlipkartspiderSpider.count < 30:
                yield Request(next_page_link, headers=self.headers, callback=self.product_page_list, dont_filter=True, meta=meta)
    
    def product_page(self, response):
        meta = response.meta
        product = FlipkartItem()
        
        name = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span/text()[1]').extract_first(default='')
        num_ratings = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/div/span/div/text()').extract_first(default='')
        price = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[1]/text() | //*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]/text()').extract_first(default='')
        if isinstance(price, str):
            clnd_price = re.sub(r',', '', price)
        else:
            clnd_price = None
        mrp =  response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]/text()[2] | //*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[2]/text()[2]').extract_first(default='')
        clnd_mrp = "₹" + re.sub(r',', '', mrp)
        offer = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[3]/span/text() | //*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div[3]/span/text()').extract_first(default='')
        clnd_offer = re.sub(r'\s*off\s*', '', offer)
        image_url = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/img/@src').extract_first(default='')
        num_reviews = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]/span/span[3]/text()').extract_first(default='')
        clnd_reviews = None
        if num_reviews:
            match = re.search(r'(\d+)', num_reviews)
            if match:
                clnd_reviews = int(match.group(1))
        delivery_status = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[6]/div/div/div[2]/div/text() | //*[@id="container"]/div/div[3]/div[1]/div[2]/div[5]/div/div/div[2]/div/text() | //*[@id="container"]/div/div[3]/div[1]/div[2]/div[5]/div/div/div[2]/div[1]/ul/div/div[1]/span[1]/text()').extract_first(default='')

        product["p_name"] = name
        product["p_num_ratings"] = num_ratings
        product["p_price"] = clnd_price
        product["p_mrp"] = clnd_mrp
        product["p_offer"] = clnd_offer
        product["p_image_url"] = image_url
        product["p_num_reviews"] = clnd_reviews
        product["p_delivery_status"] = delivery_status
        product["p_product_link"] = meta["product_link"]

        yield product

