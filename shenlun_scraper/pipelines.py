# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import logging

logger = logging.getLogger(__name__)

class ShenlunScraperPipeline(object):

    def __init__(self):

        self.workdir = os.getcwd()
        logger.info(os.getcwd())
        
    def process_item(self, item, spider):
        return item

class PrepareResPipeline(object):
    '''
    Description:
        根据item内容生成text.html,ncx,opf文件
    '''

    def process_item(self, item, spider):

        title = item['title']
        author = item['author']
        content = ''.join("<p class=\"content\">"+i+"</p>" for i in item['content'])
        pub_date = item['pub_date']
        spider_name = item['spider_name']

        #工作文件夹
        workdir = os.getcwd()+'/../result/%s/' % spider_name

        #检测是否存在result文件夹，如果不存在则新建，用于存放结果，因为dev分支不存放结果
        #git 默认不会提交空文件夹，所以需要检测并新建
        if not 'result' in os.listdir('..'):
            os.mkdir('../result/')
            #os.mkdir(workdir)
        elif not spider_name in os.listdir('../result'):
            os.mkdir(workdir)
        else:
            pass


        #如果目标目录不存在，则证明为新增或者漏抓取，则直接准备资源文件
        try:
            os.mkdir(workdir+'%s-%s-%s' % (pub_date, title, author))

            #读取模板opf文件获取其中内容
            with open('../resources/temp/title.opf','rt') as f:
                opf = f.read()

            #读取css文件
            with open('../resources/temp/style.css','rt') as f:
                stylecss = f.read()

            #写入OPF文件
            with open (workdir+'%s-%s-%s/%s-%s-%s.opf' % (pub_date,title,author,pub_date,title,author),'at') as f:
                opf = opf.replace('$title',title).replace('$author',author)
                f.write(opf)

            #写入css文件
            with open (workdir+'%s-%s-%s/style.css' % (pub_date,title, author),'at') as f:
                f.write(stylecss)

            #写入text.html文件
            pagestart = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>%s</title><link type="text/css" href="style.css" rel="Stylesheet"/></head><body>' % title
            pageend = '</body></html>'
            pagetitle = '<h2>%s</h2>' % title
            with open (workdir+'%s-%s-%s/text.html' % (pub_date, title, author),'at') as f:
                f.write(pagestart)
                f.write(pagetitle)
                f.write(content)
                f.write(pageend)

            logger.info('书籍资源制作完毕：%s' % pub_date+title)

        except:
            logger.info('This article %s-%s-%s exist, skip by PrepareRespipeline' % (pub_date, title, author))

        return item

class PackResToMobiPipeline(object):
    '''
    Description:
        通过amazon kindlegen对mobi资源进行打包
    '''

    def __init__(self):
        '''
        Description:
            列出所有需要的路径信息

        '''

    def process_item(self, item, spider):

        title = item['title']
        author = item['author']
        pub_date = item['pub_date']
        spider_name = item['spider_name']

        workdir = os.getcwd() + '/../result/%s/%s-%s-%s' % (spider_name, pub_date, title, author)

        #如果对应目录当中不存在mobi文件，就需要进行重新打包
        if not bool([i for i in os.listdir(workdir) if 'mobi' in i]):
            opf_name = [i for i in os.listdir(workdir) if 'opf' in i][0]
            workopf = workdir + '/' + opf_name

            workkindlegen = os.getcwd() + '/../resources/kindlegen'
            #out = os.popen("%s -c1 -dont_append_source -locale zh \"%s\"" % (workkindlegen,workopf)).read()
            out = os.popen("%s -c1 -dont_append_source -locale zh \"%s\"" % (workkindlegen,workopf)).read()
            logger.info(out)
            #os.system("%s -c1 -dont_append_source -locale zh \"%s\"" % (workkindlegen,workopf))
        else:
            logger.info('This article %s-%s-%s exist, skip by PackResToMobiPipeline' % (pub_date, title, author))

