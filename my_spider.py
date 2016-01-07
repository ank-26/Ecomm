# get parent folder path
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
 
import config
import start_scrapy
 
#--- Third-Party Libraries
 
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
 
#--- Python Libraries 
 
import re
 
# 
class my_Spider(Spider):
    # spider name
    name = config.scrapy_name
    # allowed_domains = list format (like domain1.com, domain2.com)
    allowed_domains = config.domains_list 
    # start_urls - crawling single or multiple websites , list formate
    start_urls = config.urls_list
 
    def parse(self, response):
        # scrapy Init function 
        # response = get HTML content 
        sel = Selector(response) 
        # split only domain name from crawl url.
 
        domain_str = response.url.split(config.url_domain_split_start)[config.url_domain_split_start_num].split(config.url_domain_split_end)[config.url_domain_split_end_num]
        # check the current crawling website all products tag, product title tag, product price tag
        start_scrapy.check_current_product_tag_patterns(domain_str)
        # 
        # sites = current all product tag content in website
        if config.current_products_pattern != '' :
            products_all = sel.xpath(config.init_div+config.current_products_pattern)
            # current website products list
            products_list = []
 
            for product_tag in products_all:
                # get all the products in "all products tag"
                # and stored in dictionary format like 
                product_name_with_price = {}
                product_name_with_price[config.web_name] = domain_str
                #print product_tag.xpath(config.in_div+config.current_product_name_pattern+config.extract_text)
                try:
                    # get the product name
                    product_name_with_price[config.product_name] = product_tag.xpath(config.in_div+config.current_product_name_pattern+config.extract_text).extract()[0].strip()
                except:
                    # get the product name
                    product_name_with_price[config.product_name] = config.none_value
                try:
                    # get the product price 
                    product_name_with_price[config.price_name] = product_tag.xpath(config.in_div+config.current_product_price_pattern+config.extract_text).extract()[0].strip()
                except:
                    # get the product price
                    product_name_with_price[config.price_name] = config.none_value
                products_list.append(product_name_with_price)
            # website all product name with prices stroed in main list     
            config.total_products_list.append(products_list)
