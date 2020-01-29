#!/bin/bash

#准备环境
python3 -m pip install scrapy
python3 -m pip install pydispatch

#运行程序
cd shenlun_scraper
scrapy crawl opinion

#打包结果
zip -r -0 ../result.zip ../result

#将结果拷贝到上级文件夹，方便覆盖到release分支
cp -rf ../result* ../..

#切换分支release
git checkout release

#复制文件到当前文件夹，即合并目录，保持原有文件，仅新增
cp -rf ../../result* ../
