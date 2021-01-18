# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from convert2markdown import convert

class ScrapeFloralesPipeline:
    def process_item(self, item, spider):
        front = f'''
---
title: "{item["title"]}"
date: 2021-01-18T16:08:22-03:00
draft: false
--- 
        ''' 
        res = convert(item['content'], front)
        item['content'] = res
        with open(f"mdfiles/{item['title']}.md", 'w') as mdfile:
            mdfile.write(res)
        return item
