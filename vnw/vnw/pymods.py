# -*- coding: utf-8 -*-

def xtract(resp, xpath):
    li = []
    xtracts = resp.xpath(xpath).extract()
    for xts in xtracts:
        xts = xts.strip()
        li.append(xts)
    return u'|'.join(li)

