# -*- coding: utf-8 -*-
import scrapy
import json,urllib
import os

from json import JSONEncoder
from scrapy.utils.trackref import iter_all
from scrapy.utils.markup import remove_tags
from urlparse import urljoin
from scrapy.http.request import Request
from scrapy.http import FormRequest



class SDSpider(scrapy.Spider):

    name = "sd"
    allowed_domains = ["snapdeal.com"]

    start_urls = [
	    "http://www.snapdeal.com/offers/diwali-home?MID=19OCT_HOURLY_PriceStore_WEB"
	    ]
##    def parse_link(self, response):
##	body = response.xpath('//body/div[@id="content_wrapper"]')
##        apikey = "345c1d09fc2d94cfa2cc1ad0a97560e02154"
##        language = "hindi"
##	texts = body.xpath('.//title/text() | .//p/text() | .//span/text() | .//a/text() | .//div/text()').extract()
##	for text in texts:
##	    if text:
##                text = text.rstrip()
##   
##                #yield locRequest
##                #print response.body
##                #print text.encode('utf-8')
##		linkTags = body.xpath('.//li')
##
##
##		for linkTag in linkTags:
##			linkTitle = linkTag.xpath('a/text()').extract()
##			if linkTitle:
##				print linkTitle[0].strip()
##
##			linkSel = linkTag.xpath('.//@href').extract()
##			if linkSel:
##				link = linkSel[0]
##				abslink=urljoin("http://www.snapdeal.com/",link)
##
##				#print abslink
##				#request = Request(abslink,callback=self.parse_link)
##				#yield request

    def parse(self, response):

		textTags = response.xpath('//title | //p | //span | //a | //div | //li')
		
 
		
		for textTag in textTags:
                        textSel = textTag.xpath('text()').extract()
                        
			if textSel:
                            text = textSel[0].strip('/').rstrip()
                            print text.encode('utf-8')
		#[r.url for r in iter_all('HtmlResponse')]
		#print_live_refs()

 
		#[
                boxes = response.xpath('//li[contains(@class,"OffersContentBoxLi")] ')
                for box in boxes:
                    textSel = box.xpath('//a/div/text()').extract()
                    if textSel:
                        text = textSel[0].strip('/').rstrip()
                        print text.encode('utf-8')
		
		linkTags = response.xpath('//li')
                

		for linkTag in linkTags:
			linkTitle = linkTag.xpath('a/text()').extract()
			if linkTitle:
				linkText =  linkTitle[0].rstrip()
				print linkText.encode('utf-8')
			#linkSel = linkTag.xpath('.//@href').extract()
			#if linkSel:
				#link = linkSel[0]
				#abslink=urljoin("http://www.snapdeal.com/",link)

				#print abslink
				#request = Request(abslink,callback=self.parse_link)
				#yield request

                
    
    
