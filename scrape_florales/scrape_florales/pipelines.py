# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from convert2markdown import convert
import re
class ScrapeFloralesPipeline:
    bold_regx = re.compile(r'(\*\*.*?\*\*)')
    tag_targets = [re.compile(string, re.DOTALL) for string in [r'<script>.*</script>', r'<a.*>.*</a>']]
    bold_targets = [re.compile(string) for string in [r'(Positivo:)\s', r'(Negativo:)\s', r'(Resumen:)\s', r'(Cuando se da en un test intuitivo:)\s']]
    @classmethod
    def bolden(cls, string):
        for regx in cls.bold_targets:
            string = regx.sub(lambda mo: '**' + mo.group(1) + '**' , string)
        return string

    @classmethod
    def del_tags(cls, string):
        for regx in cls.tag_targets:
            string = regx.sub('', string)
        return string
        
    @classmethod
    def prettify(cls, string):
        string = cls.bolden(string)
        result = cls.bold_regx.sub(lambda mo: '\n\n' + mo.group(0) + ' ' , string)
        return result

    def process_item(self, item, spider):
        front = f'''
---
title: "{item["title"]}"
date: 2021-01-18T16:08:22-03:00
draft: false
--- 
        ''' 
        clean_html = self.del_tags(item['content'])
        res = convert(clean_html, front)
        with open(f"mdfiles/{item['title']}.md", 'w') as mdfile:
            mdfile.write(self.prettify(res))
        with open(f"mdfiles/{item['title']}.html", 'w') as htmlfile:
            htmlfile.write(clean_html)
        item['content'] = res
        return item
