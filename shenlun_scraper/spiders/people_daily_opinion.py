# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from scrapy.exceptions import CloseSpider
from scrapy import signals
from pydispatch import dispatcher
from  shenlun_scraper.items import ShenlunScraperItem

logger = logging.getLogger(__name__)

class PeopleDailyOpinionSpider(scrapy.Spider):
    '''
    Description:
        抓取人民网当中人民时评所有内容，parse方法处理列表，yield到parse_info方法处理详细内容
        交由pipelines方法写入到html，方便直接转换到mobi文件

        通过正则表达式测试当前页是否有“下一页”字样存在，如果有则在url当中加1生成下一页url
    '''

    name = 'opinion'
    allowed_domains = ['opinion.people.com.cn']
    start_urls = ['http://opinion.people.com.cn/GB/8213/49160/49219/index1.html']

    def __init__(self):

        self.count = 1
        
    def parse(self, response):

        opinion_base_url = "http://opinion.people.com.cn/"
        index_base_url = "http://opinion.people.com.cn/GB/8213/49160/49219/index%s.html"

        #opinion_title = response.xpath("//a[@class='abl']//text()").getall()
        opinion_urls = response.xpath("//a[@class='abl']//@href").getall()
        opinion_url = [opinion_base_url + i for i in opinion_urls]

        for content_url in opinion_url:
            yield scrapy.Request(url=content_url, callback=self.parse_info)

        next_url = response.xpath("//td[@class='t10l14bl']").re('下一页')
        if next_url:
            self.count = self.count + 1
            next_page = index_base_url % self.count
            yield scrapy.Request(url=next_page, dont_filter=True, callback=self.parse)

    
    def parse_info(self, response):

        item = ShenlunScraperItem()

        #获取文章title,authr
        content_title = response.xpath("//div[@class='clearfix w1000_320 text_title']/h1/text()").get()
        try: 
            title = re.match(r"人民日报人民时评(:|：)(.*)",content_title).group(2)
        except:
            title = content_title
        author = response.xpath("//p[@class='author']/text()").get().replace('\xa0','')

        #获取文章内容
        origin_content = response.xpath("//div[@class='box_con']/p/text()").getall()
        m = [i.strip('\n\t').strip('\u3000').strip('\xa0') for i in origin_content]
        content = [i for i in m if i!='']

        #获取发布时间
        pub_date = ''.join(re.findall(r".*\/n1\/(\d{4})\/(\d{4,5})\/.*",response.url)[0])

        item['title'] = title
        item['author'] = author
        item['content'] = content
        item['pub_date'] = pub_date

        yield item

    #通过signal方式，定义爬虫在空闲的时候关闭
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PeopleDailyOpinionSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
