# -*- coding: utf-8 -*-
import scrapy, re
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class FitnessauSpiderSpider(CrawlSpider):
    name = 'fitnessau_spider'
    #allowed_domains = ['libreriatemasylibros.py']
    start_urls = ['http://fitness.org.au/directory/business/category/personal-training/2/38']

    rules = (
        #Rule (LinkExtractor(allow=[r'http://www.jomstay.com/category']), follow= True),
        Rule (LinkExtractor(restrict_xpaths=('//ul[@class="pagination"]'),), callback='parse_start_url', follow=True),
        )

    
    def parse_start_url(self, response):
        for item in response.css('div.search-item div.frame'):
            request = Request(url=response.urljoin(item.xpath('.//a[@class="no-hover-underline"]/@href').extract_first()), callback=self.parse_details)
            request.meta["BusinessName"] = item.xpath('.//a[@class="no-hover-underline"]/h2/text()').extract_first()
            request.meta["Location"] = item.xpath('.//span[@class="loc"]/strong/text()').extract_first()
            request.meta["Phone"] = item.xpath('.//span[@class="phone"]/text()').extract_first()
            request.meta["Website"] = item.xpath('.//a[@class="web"]/@href').extract_first()
            yield request
    
    def parse_details(self, response):
        yield {
        "BusinessName" : response.meta["BusinessName"],
        "Name" : response.css('div.text-holder p a::text').extract_first(),
        "Location" : response.meta["Location"],
        "Website" : response.meta["Website"],
        "Phone" : response.meta["Phone"]
        }