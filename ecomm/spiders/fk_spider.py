# -*- coding: utf-8 -*-
import scrapy

import os
from scrapy.utils.trackref import iter_all
from scrapy.utils.markup import remove_tags
from urlparse import urljoin	
from scrapy.http.request import Request



class FKSpider(scrapy.Spider):

    name = "fk"
    allowed_domains = ["flipkart.com"]

    start_urls = [
	    "http://www.flipkart.com/"
	    ]
    def parse_link(self, response):
		body = response.xpath('//body//div[@id="fk-mainbody-id"]')
		texts = body.xpath('.//title/text() | .//p/text() | .//span/text() | .//a/text()').extract()
		for text in texts:
			if text:
				
				text = text.rstrip()
				print text.encode('utf-8')
		linkTags = body.xpath('.//li')
		
		
		for linkTag in linkTags:
			linkTitle = linkTag.xpath('a/text()').extract()
			if linkTitle:
				print linkTitle[0].strip()
				
			linkSel = linkTag.xpath('.//@href').extract()
			if linkSel:
				link = linkSel[0]
				abslink=urljoin("http://www.flipkart.com/",link)
				
				#print abslink
				request = Request(abslink,callback=self.parse_link)
				yield request
	
    def parse(self, response):
    	
		texts = response.xpath('//title/text() | //p/text() | //span/text() | //a/text()').extract()
		for text in texts:
			if text:
				#text = ''.join(text.split(' '))
				text = text.strip('/').rstrip()
				print text.encode('utf-8')
		#[r.url for r in iter_all('HtmlResponse')]
		#print_live_refs()
		linkTags = response.xpath('//li')
		
		
		for linkTag in linkTags:
			linkTitle = linkTag.xpath('a/text()').extract()
			if linkTitle:
				print linkTitle[0].rstrip()
				
			linkSel = linkTag.xpath('.//@href').extract()
			if linkSel:
				link = linkSel[0]
				abslink=urljoin("http://www.flipkart.com/",link)
				
				#print abslink
				request = Request(abslink,callback=self.parse_link)
				yield request
	
	