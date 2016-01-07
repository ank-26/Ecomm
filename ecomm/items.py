# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TabItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tabName = scrapy.Field()
    
    categories = scrapy.Field()
    subcategories = scrapy.Field()
    #detail2 = scrapy.Field()
    #detail3 = scrapy.Field()
    #detail4 = scrapy.Field()
    pass

class CatItem(scrapy.Item):
    catName = scrapy.Field()

class SubCatItem(scrapy.Item):
    subcatName = scrapy.Field()

   # def __setitem__(self, key, subcat):
    #    if key not in self.fields:
     #       self.fields[key] = scrapy.Field()
      #  self._values[key] = subcat
