import scrapy
import os



from scrapy.http.request import Request
class ABusSpider(scrapy.Spider):
    name = "abus"
        
    allowed_domains = ["abhibus.com"]
    start_urls = [
        "http://dev.abhibus.com/operators/"
        ]
    if not os.path.exists(name):
            os.makedirs(name)
    
    
    def parse(self, response):

        fobj = open("abus.txt", 'a+')
        link_selector = response.xpath('//div[@class="detrow"]')
        #print link_selector
        temp = link_selector.xpath('.//ul')
        for link in temp.xpath('li/a/@href'):
            #print link.extract()
            url = link.extract().encode('utf-8')
            request =  Request(url,callback=self.parse_link)
            request.meta['fobj'] = fobj
            yield request

        pagenav = response.xpath('//div[@class="pagenav"]')
        nextSel = pagenav.xpath('a[contains(text(),"Next")]')
        if nextSel:
            nextLinkSel = nextSel.xpath('@href').extract()
            
            nextLink = nextLinkSel[0].encode('utf-8')
            print nextLink
            request2 = Request(nextLink,callback=self.parse)
            yield request2
        

    def parse_link(self,response):
        fobj = response.meta['fobj']

        text = response.xpath('//div[@class="about"]/p/text()').extract()

        for para in text:
            print para
            fobj.write(para)
        fobj.write("\n _____________________________________________________________________ \n")
        
        
