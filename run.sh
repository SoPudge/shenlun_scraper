#!/bin/bash

#准备环境
python3 -m pip install scrapy
python3 -m pip install pydispatch

#运行程序
cd shenlun_scraper
scrapy crawl opinion

#打包结果
zip -r -0 ../result.zip ../result
