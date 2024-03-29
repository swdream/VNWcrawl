# -*- coding: utf-8 -*-

import datetime

import scrapy
from ..keywords import KWS
from ..items import PyjobItem
from ..pymods import xtract
from ..convert_month import convert


class ItviecSpider(scrapy.Spider):
    name = "itviec"
    allowed_domains = ["itviec.com"]
    start_urls = [
        ("https://itviec.com/jobs/" + kw) for kw in KWS
    ]

    def parse(self, resp):
        url = resp.url
        keyword = url.split('/jobs/')[1]
        for href in resp.xpath('//h2[@class="title"]/a/@href').extract():
            request = scrapy.Request(resp.urljoin(href), self.parse_content)
            request.meta["keyword"] = keyword
            yield request

    def parse_content(self, resp):
        item = PyjobItem()
        item["keyword"] = resp.meta["keyword"]
        item["url"] = resp.url
        item["name"] = xtract(resp, '//h1[@class="job_title"]/text()')
        item["company"] = xtract(resp, '//h3[@class="name"]/text()')
        item["address"] = resp.xpath('//div[@class="address"]/'
                                     'text()').extract()[0].strip()
        expiry_date = xtract(resp, '//div[@class="created_at"]/text()')
        day = expiry_date.split(' ')[-1]
        month = expiry_date.split(' ')[-2]
        month_convert = convert(month)
        item["expiry_date"] = '-'.join([str(datetime.date.today().year),
                                       month_convert, day])
        item["province"] = resp.xpath('//div[@class="address"]'
                                      '/text()').extract()[0].split(',')[0]
        item["work"] = xtract(resp, '//div[@class="description"]/p/text()')
        item["specialize"] = xtract(resp, '//div[@class="experience"]/'
                                          'p/text()')
        item["welfare"] = xtract(resp, '//div[@class="culture_description"]/'
                                       'p/text()')
        item["size"] = xtract(resp, '//p[@class="group-icon"]/text()')

        yield item
