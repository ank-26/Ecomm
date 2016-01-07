import scrapy
import os
import xlsxwriter
#from ecomm.items import TabItem
#from ecomm.items import CatItem
#from ecomm.items import SubCatItem
from scrapy.http.request import Request
currDir = "/Users/ankita/ecomm/snapdeal"
class SDSpider(scrapy.Spider):
    name = "snapdeal"
        
    allowed_domains = ["snapdeal.com"]
    start_urls = [
        "http://www.snapdeal.com/page/sitemap"
        ]
    if not os.path.exists(name):
            os.makedirs(name)
    os.chdir(name)
    
    def parse(self, response):
        
        dirname = os.getcwd()
        tabs= []
        tab_selector = response.xpath('//div[contains(@id, "SMWrapr")]')
        ### loop for all tabs
        for tab in tab_selector.xpath('.//div[contains(@id, "Tab")]'):
           # tabItem = TabItem()
           
            tabNameSel = tab.xpath('div/span[2]/text()').extract()
                       
            if tabNameSel:
                tabName = tabNameSel[0]
                
                
            os.chdir(dirname)
            if not os.path.exists(currDir+"/"+tabName):
            	os.makedirs(currDir+"/"+tabName)         
            #os.chdir(tabName)
            fobj = open(currDir+"/"+tabName+".txt", 'w')
            cat_selector = tab.xpath('div[2]/div[contains(@class, "SMSubCat")]')
            ### loop for all categories
            for category in cat_selector.xpath('div'): #'.//div[contains(@class, "ht180")]
             #   catItem = CatItem()
                catNameSel = category.xpath('div/a/@title').extract()
                if catNameSel:
                    catName = catNameSel[0]
                    
                subcat_selector = category.xpath('.//ul')
                ### loop for all subcategories
                for subcat in subcat_selector.xpath('.//li'):
                    subcatNameSel = subcat.xpath('.//a/@title').extract()
                    if subcatNameSel:
                        subcatName = subcatNameSel[0]
                    subcatLinkSel = subcat.xpath('.//a/@href').extract()
                    if subcatLinkSel:
                        subcatLink = subcatLinkSel[0]+"?sort=plrty"
                        
                    request = Request(subcatLink,callback=self.parse_subcatpage)
                    request.meta['fobj'] = fobj
                    request.meta['tabName'] = tabName
                    request.meta['catName'] = catName
                    request.meta['subcatName'] = subcatName
                    yield request
            
                    
                        #(response,tabName,catName,subcatName)
                  
                    #print subcatLink
                    #print tabName, ":", catName, ":", subcatName
              #  categories.append(catItem)
            #return categories
            #categories = [dict(categories)]
            #tabs.append(tabItem)
        #return tabs
        	
        	os.chdir(dirname)
        	
        fobj.close()
         
    def parse_subcatpage(self, response):
        fobj = response.meta['fobj']
        tabName = response.meta['tabName']
        catName = response.meta['catName']
        subcatName = response.meta['subcatName']
        filter_selector = response.xpath('//div[contains(@class, "filters-outer")]')
        os.chdir(currDir+"/"+tabName)
        for filtr in filter_selector.xpath('.//div'):
            filterNameSel = filtr.xpath('.//span[contains(@class, "filtersHeading")]/text()').extract()
            if filterNameSel:
                filterName = filterNameSel[0]
                result = str("\n"+tabName+" -> "+catName+" -> "+subcatName+" -> "+filterName+" -> ")
                #print result.encode('utf-8')
                
                if fobj.closed:
                    fobj = open(fobj.name, "a+")
                fobj.write("\n"+result.encode('utf-8'))

                """
                worksheet.write(row,col, tabName)
                worksheet.write(row+1,col, catName)
                worksheet.write(row+1,col, subcatName)
                worksheet.write(row+1,col, filterName)
                """
            valueSelector = filtr.xpath('.//div[contains(@class, "visible-filter")]') ##fliters = filters(error in SD site)
            #print valueSelector.extract()
            for value in valueSelector.xpath('.//div[contains(@class, "fliters-list")]'):
                valueNameSel = value.xpath('label/a/text()').extract()
                if valueNameSel:
                    valueName = valueNameSel[0].strip()+" | "                    
                    #print valueName.encode('utf-8')
                    fobj.write(valueName.encode('utf-8'))
        
        
        fprod = open(currDir+"/"+tabName+"/"+subcatName+".txt", 'w+')             
        prodSelector = response.xpath('//div[@id="products-main4"]')
        #print "------------------------------------"
        for product in prodSelector.xpath('.//div[@class="product_grid_box"]'):
        
        	
            prodNameSel = product.xpath('div[2]/div[2]/a/p/text()').extract()
            
            prodPrice = product.xpath('.//div[@class="product-price"]/p/text()').extract()
            
            prodLinkSel = product.xpath('div[2]/div[2]/a/@href').extract()
            
                        
            if prodNameSel:
                prodName = prodNameSel[0]
            	resProd = str("\n"+prodName+ " -> ")
            
                
            """
            prodFeaturesSel = product.xpath('.//ul[@id="highLights"]')
            for feature in prodFeaturesSel.xpath('li'):
            	featNameSel = feature.xpath('text()').extract()
            	if featNameSel:
            		featName = featNameSel[0].strip()+" | "
            		print featName.encode('utf-8')
            		fobj.write(featName.encode('utf-8')) 
            		"""
            
            
            if prodLinkSel:
            	prodLink = prodLinkSel[0]			                  
            	request = Request(prodLink,callback=self.parse_prodpage)
            	request.meta['fprod'] = fprod
            	request.meta['resProd'] = resProd
            	yield request
    	fprod.close()        
    def parse_prodpage(self, response):
    	fprod = response.meta['fprod'] 
    	resProd = response.meta['resProd']   
    	#prodName : 
    	selector = response.xpath('//section[@id="productSpecs"]')
    	spectitleSel = selector.xpath('.//div[contains(@class, "spec-section")]')
    	if fprod.closed:
            	fprod = open(fprod.name, "a+")
        fprod.write("\n -------------------------------------------")
        fprod.write(resProd.encode('utf-8'))
    	for title in spectitleSel.xpath('div'):
    		titleSel = title.xpath('h3/text()').extract()
    		
    		if titleSel:
    			resTitle = titleSel[2].strip()
    			if fprod.closed:
            			fprod = open(fprod.name, "a+")
    			fprod.write("\n"+resTitle.encode('utf-8')+"\n_____________________")
    		for line in title.xpath('ul/li | .//tr/th | .//tr/td | .//span'):
    			lineText = line.xpath('.//text()').extract()
    			
    			if lineText:
    				resLine = lineText[0].strip()
    				if fprod.closed:
            				fprod = open(fprod.name, "a+")
    				fprod.write("\n"+resLine.encode('utf-8'))
    				#print lineText[0]
    		        
