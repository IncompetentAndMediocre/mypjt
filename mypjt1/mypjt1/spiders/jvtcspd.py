import re

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mypjt1.items import Mypjt1Item

class JvtcspdSpider(CrawlSpider):
    name = 'jvtcspd'
    allowed_domains = ['jvtc.jx.cn']
    start_urls = ['https://www.jvtc.jx.cn/']
    links = LinkExtractor(allow=('[a-zA-z]+://[^\s]*?/info/[^\s]*'),
                          allow_domains=('jvtc.jx.cn'))
    rules = (
        Rule(links, callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = Mypjt1Item()
        # 获取标题
        item['name'] = response.xpath("/html/head/title/text()").extract()

        # 获取url
        link_data = []
        for link in self.links.extract_links(response):
            link_data.append(link.url)
        item['url'] = link_data[0]

        # 获取点击量
        data1 = response.xpath("//p[@class='article-date']/span[4]/script/text()").extract()
        # print(data1)
        it = re.compile("[1-9][0-9]{4,}").finditer(str(data1))
        data2 = []
        for match in it:
            data2.append(match.group())
        url = "https://www.jvtc.jx.cn/system/resource/code/news/click/dynclicks.jsp?clickid=" + data2[1] + "&owner=" + \
              data2[0] + "&clicktype=wbnews"
        resp = requests.get(url=url)
        item['hits'] = resp.json()

        return item
