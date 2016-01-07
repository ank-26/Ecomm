import scrapy
import os



from scrapy.http.request import Request
class AMZSpider(scrapy.Spider):
    name = "amazon"
        
    allowed_domains = ["amazon.in"]
    start_urls = [
        "http://www.amazon.in/gp/site-directory/"
        ]
    if not os.path.exists(name):
            os.makedirs(name)
    
    
    def parse(self, response):
        
        
        tabs= []
        tab_selector = response.xpath('//div[@id="siteDirectory"]') 
        ### loop for all tabs
        for tab in tab_selector.xpath('.//div[@class="popover-grouping"]'):
            tabNameSel = tab.xpath('h2/text()').extract()
                       
            if tabNameSel:
                tabName = tabNameSel[0]
                
                fobj = open(tabName+".txt", 'a+')   
                       
            cat_selector = tab.xpath('.//ul')
            
            ### loop for all categories
            for category in cat_selector.xpath('li'): #'.//div[contains(@class, "ht180")]
                catNameSel = category.xpath('a/text()').extract() #//div[contains(@class, "top-menu unit")]/ul/li/div/div/div/ul/li[@class="heading"]
                #print category.extract()
                if catNameSel:
                    catName = catNameSel[0]
                catLinkSel = category.xpath('a/@href').extract()
                if catLinkSel:
                        catLink ="http://www.amazon.in"+catLinkSel[0]
                        
                
                request = Request(catLink,callback=self.parse_subcatpage)
                request.meta['fobj'] = fobj
                request.meta['tabName'] = tabName
                request.meta['catName'] = catName
                yield request
                
        fobj.close()   
    def parse_subcatpage(self, response):
        fobj = response.meta['fobj']
        tabName = response.meta['tabName']
        catName = response.meta['catName']

        subcatSel = response.xpath('//div[@id="refinements"]')
        if subcatSel: ## in few categories subcategories are not present 
            subcatNameSel = subcatSel.xpath('div/ul/li/a/span[1]/text()').extract()
            if subcatNameSel:
                subcatName = subcatNameSel[0]
                print subcatName + "sub category......"
        
        
        filter_selector = subcatSel
        index = 1
        for filtr in filter_selector.xpath('.//h2'):
            filterNameSel = filtr.xpath('text()').extract()
            #print  filterNameSel
            if filterNameSel:
                filterName = filterNameSel[0]
                result = str("\n"+tabName+" -> "+catName+" -> "+filterName+" -> ")
                
            #valueSelector = filter_selector.xpath('.//ul['+str(index)+']') ##fliters = filters(error in SD site)
            valueSelector = filtr.xpath('.//following-sibling::ul[1]')
            valueLinkSel = valueSelector.xpath('.//a[span[contains(@class, "seeMore")]]/@href').extract()
            if valueLinkSel:
                valueLink = "http://www.amazon.in"+valueLinkSel[0]
                requestValue = Request(valueLink,callback=self.parse_valuepage)
                requestValue.meta['fobj'] = fobj
                requestValue.meta['tabName'] = tabName
                requestValue.meta['catName'] = catName
                requestValue.meta['filterName'] = filterName
            
                yield requestValue
            #print valueSelector.extract()
            else:
                print result.encode('utf-8')
                if fobj.closed:
                    fobj = open(fobj.name, "a+")
               
                fobj.write(result.encode('utf-8'))
                for value in valueSelector.xpath('li'):
                    valueNameSel = value.xpath('.//span/text()').extract()
                    if valueNameSel:
                        valueName = valueNameSel[0].strip()+" | "                    
                        print valueName.encode('utf-8')
                        fobj.write(valueName.encode('utf-8'))
                
            index += 1
        #### brand filter has a different structure here, hence extra code for that
        brand_sel = response.xpath('//ul[@id="ref_3837712031"]')
        print brand_sel.extract()
        
        brandLinkSel = brand_sel.xpath('li/a[span[contains(@class, "seeMore")]]/@href').extract()
        print "brand link "
        print brandLinkSel
        if brandLinkSel:
            brandLink = "http://www.amazon.in"+brandLinkSel[0]
            print brandLink
            requestBrand = Request(brandLink,callback=self.parse_valuepage)
            requestBrand.meta['fobj'] = fobj
            requestBrand.meta['tabName'] = tabName
            requestBrand.meta['catName'] = catName
            requestBrand.meta['filterName'] = "Brands"
            yield requestBrand
        else:
            
            filterName = "Brands"
            result = str("\n"+tabName+" -> "+catName+" -> "+filterName+" -> ")
            print result.encode('utf-8')
            for value in brand_sel.xpath('ul[@class="groupMultiSel"]/li'):
                valueNameSel = value.xpath('.//a/span[1]/text()').extract()
                if valueNameSel:
                    valueName = valueNameSel[0].strip()+" | "                    
                    print valueName.encode('utf-8')
                    fobj.write(valueName.encode('utf-8'))
        
    def parse_valuepage(self, responseValue):
        fobj = responseValue.meta['fobj']
        tabName = responseValue.meta['tabName']
        catName = responseValue.meta['catName']
        filterName = responseValue.meta['filterName']
        result = str("\n"+tabName+" -> "+catName+" -> "+filterName+" -> ")
        print result.encode('utf-8')
        if fobj.closed:
           fobj = open(fobj.name, "a+")
        fobj.write(result.encode('utf-8'))
            
        valueSel = responseValue.xpath('//ul[@class="column"]')
        for value in valueSel.xpath('li'):
            valueNameSel = value.xpath('.//a/span[1]/text()').extract()
            if valueNameSel:
                    valueName = valueNameSel[0].strip()+" | "                    
                    print valueName.encode('utf-8')
                    fobj.write(valueName.encode('utf-8'))

    
