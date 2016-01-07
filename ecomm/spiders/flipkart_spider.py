import scrapy
import os
import xlsxwriter
#from ecomm.items import TabItem
#from ecomm.items import CatItem
#from ecomm.items import SubCatItem
from scrapy.http.request import Request
class FKSpider(scrapy.Spider):
    name = "flipkart"
        
    allowed_domains = ["flipkart.com"]
    start_urls = [
        "http://www.flipkart.com"
        ]
    if not os.path.exists(name):
            os.makedirs(name)
    
    
    def parse(self, response):
        
        
        tabs= []
        tab_selector = response.xpath('//div[contains(@class, "top-menu unit")]') 
        ### loop for all tabs
        for tab in tab_selector.xpath('ul/li'):
            tabNameSel = tab.xpath('a/span/text()').extract()
                       
            if tabNameSel:
                tabName = tabNameSel[0]
                
                fobj = open(tabName+".txt", 'a+')   
            print tabName
           
            cat_selector = tab.xpath('.//div')
            print cat_selector.extract()
            ### loop for all categories
            for index,category in cat_selector.xpath('div/div'): #'.//div[contains(@class, "ht180")]
                catNameSel = category.xpath('ul/li[@clsss="heading"]').extract() #//div[contains(@class, "top-menu unit")]/ul/li/div/div/div/ul/li[@class="heading"]
                print category.extract()
                if catNameSel:
                    catName = catNameSel[0]
                print "catname" + catName 
                #subcat_selector = category.xpath('.//ul')
            
