# -*- coding: utf-8 -*-

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
        for div in resp.xpath('//div[@class="job_content"]'):
            try:
                data_post_date = xtract(div, 'div/div[@class="text"]/text()')
                day = data_post_date.split(' ')[1]
                month = data_post_date.split(' ')[0]
                month_convert = convert(month)
                post_date = month_convert + '-' + day
            except IndexError:
                post_date = 'Hot Job'
            for href in div.xpath('div/h2/a/@href').extract():
                request = scrapy.Request(resp.urljoin(href), self.parse_content)
                request.meta["keyword"] = keyword
                request.meta["post_date"] = post_date
                yield request

    def parse_content(self, resp):
        item = PyjobItem()
        item["keyword"] = resp.meta["keyword"]
        item["url"] = resp.url
        item["post_date"] = resp.meta["post_date"]
        item["name"] = xtract(resp, '//h1[@class="job_title"]/text()')
        item["company"] = xtract(resp, '//h3[@class="name"]/text()')
        item["address"] = resp.xpath('//div[@class="address"]/'
                                     'text()').extract()[0].strip()
        expiry_date = xtract(resp, '//div[@class="created_at"]/text()')
        day = expiry_date.split(' ')[-1]
        month = expiry_date.split(' ')[-2]
        month_convert = convert(month)
        item["expiry_date"] = month_convert + '-' + day
        item["province"] = resp.xpath('//div[@class="address"]'
                                      '/text()').extract()[0].split(',')[0]
        item["work"] = xtract(resp, '//div[@class="description"]/p/text()')
        item["specialize"] = xtract(resp, '//div[@class="experience"]/'
                                          'p/text()')
        item["welfare"] = xtract(resp, '//div[@class="culture_description"]/'
                                       'p/text()')
        item["size"] = xtract(resp, '//p[@class="group-icon"]/text()')

        yield item
