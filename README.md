# 抓取网络上《申论》范文爬虫

## 背景

程序基于scrapy框架，用途是抓取网络上优秀的申论范文，并打包成mobi格式，通过git actions自动发布relese。
发布的release包含当日及以前的全部打包，和当日单篇文章的mobi文件，按照不同的抓取平台分类。
目前支持的申论文章平台：

- [人民日报人民时评](http://opinion.people.com.cn/GB/8213/49160/49219/index.html)
- TODO

## 环境

- MacOS Catalina 10.15.2
- Python 3.x
- scrapy 1.8
- pydispatch

其实相对新的scrapy环境都行，除了scrapy和pydispatch外没有引入其他包

## 原理

- 整体程序为scrapy框架，在spiders文件夹当中定义具体的爬虫方法
- 通过pipleline来定义抓取每个元素后的后续工作，总共有两个  
生成打包mobi所需的资源，即toc文件，opf文件，html内容文件。
生成完毕后使用官方的kindlegen进行mobi打包
每抓取完成一篇文章，即会运行上述两个pipleline。

- 本程序默认使用64位的amazon kindlegen。
实际上amazon仅提供32位的kindlegen，而64位的获取方式详见这篇文章：  
[在Mac OS 中使用64bit的KindleGen软件](http://65536.io/2020/01/602.html)

- 本程序对mobi程序的打包详见pipleline文件

## 安装

- git clone https://github.com/SoPudge/shenlun_scraper.git
- pip install scrapy
- pip install pydispatch  

## 使用

- cd shenlun_scraper/shenlun_scraper

第一层为git克隆的程序主目录，第二层则是spider的运行目录

- scrapy crawl opinion

抓取人民时评的爬虫命名为opinion，即运行爬虫，爬虫运行后会按照title-author的方式在。
shenlun_scraper/result目录当中生成单篇文章的目录，里面包含完整的打包mobi所需文件  
和成品的mobi文件，拷贝出来即可使用

## TODO

- 增加其他申论范文的爬虫
- git actions每日自动运行爬虫，并自动release相关的mobi当日及历史压缩包

