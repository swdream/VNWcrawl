# -*- coding: utf-8 -*-

import scrapy
from ..items import PyjobItem
from ..pymods import xtract
from ..keywords import KWS

province = u'Nơi làm việc'
wage = u'Mức lương'
experience = u'Kinh nghiệm'
work = u'Mô tả công việc'
welfare = u'Quyền lợi được hưởng'
specialize = u'Yêu cầu công việc'
file_request = u'Yêu cầu hồ sơ'
leadtime = u'Hạn nộp hồ sơ'
language = u'Ngôn ngữ hồ sơ'
website = u' Website: '
phone = u' Điện thoại: '
fax = u' Fax: '
size = u' Số nhân viên: '



class MyworkSpider(scrapy.Spider):
    name = "mywork"
    allowed_domains = ["mywork.com.vn"]
    start_urls = [("http://mywork.com.vn/tim-viec-lam/" + kw + ".html")
                  for kw in KWS]

    def parse(self, resp):
        for href in resp.xpath('//div[@class="item "]/div/a/@href').extract():
            yield scrapy.Request(resp.urljoin(href), self.parse_content)

        if resp.xpath('//div[@class="mywork-pages pagination"]/a/@class').\
            extract()[-1] != u'disabled':
            next_page = resp.xpath('//div[@class="mywork-pages pagination"]'
                                    '/a/@href').extract()[-1]
            yield scrapy.Request(resp.urljoin(next_page), self.parse)

    def parse_content(self, resp):
        item = PyjobItem()
        item["name"] = xtract(resp, '//div[@class="title-job-info"]/text()')
        item["company"] = xtract(resp,
                                 '//h1[@class="fullname-company"]/text()')
        item["address"] = xtract(resp,
                                 '//p[@class="address-company mw-ti"]/text()')
        item["skill"] = ''
        for desjob in resp.xpath('//div[@class="desjob-company"]'):
            kws = xtract(desjob, 'h4/text()')
            if province == kws:
                item["province"] = xtract(desjob, 'span/a/text()')
            if wage == kws:
                if xtract(desjob, 'span/text()'):
                    item["wage"] = xtract(desjob, 'span/text()')
                else:
                    item["wage"] = xtract(desjob, 'text()')
            if experience == kws:
                item["experience"] = xtract(desjob,  'text()')
            if work == kws:
                if xtract(desjob, 'p/text()') != u'':
                    item["work"] = xtract(desjob, 'p/text()')
                else:
                    item["work"] = xtract(desjob, 'div/text()')
            if welfare == kws:
                if xtract(desjob, 'p/text()') != u'':
                    item["welfare"] = xtract(desjob, 'p/text()')
                else:
                    item["welfare"] = xtract(
                        desjob, 'div[@class="job_more_detail"]/text()')
            if specialize == kws:
                if xtract(desjob, 'p/text()') != u' ':
                    item["specialize"] = xtract(desjob, 'p/text()')
                else:
                    item["specialize"] = xtract(desjob, 'div/text()')

            if file_request == kws:
                item["file_request"] = xtract(desjob, 'p/text()')
            if leadtime == kws:
                item["leadtime"] = xtract(desjob, 'p/text()')
            if language == kws:
                item["language"] = xtract(desjob, 'p/text()')

        for mw in resp.xpath('//p[@class="mw-ti"]'):
            ti = mw.xpath('text()').extract()[0]
            if website == ti:
                item["website"] = xtract(mw, 'span/text()')
            if phone == ti:
                item["phone"] = xtract(mw, 'span/a/text()')
            if size == ti:
                item["size"] = xtract(mw, 'span/text()')
            if fax == ti:
                item["fax"] = xtract(mw, 'span/text()')
        item["logo"] = xtract(resp, '//div[@class="logo-company"]/img/@src')

        yield item