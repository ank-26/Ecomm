from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.project import get_project_settings
 
from spiders.my_spider import my_Spider
    # Scrapy spiders script...
    dispatcher.connect(stop_reactor, signal=signals.spider_closed) 
    spider = my_Spider()
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
     # scrapy instructions stored in log file
    log.start(logfile=config.log_file_name, loglevel=log.DEBUG, crawler=crawler, logstdout=False)   
    reactor.run()
    show_output()  
def loading_web_list():       
    tree = XMLCorpusReader('.', [config.web_list_XML])
    root = tree.xml()
    for web in root.iter(config.web_list_xml_main_tag_name):
        # get xml child nodes name with value(e.g {url:'http://google.com',name:'google'}) - dictionary format
        config.web_list.append(web.attrib)
        # get urls only.
        config.urls_list.append(web.get(config.wel_list_xml_url_attribute))
		
		
def loading_web_content_regex():
    tree = XMLCorpusReader('.', [config.web_content_regex_file])
    root = tree.xml()
    for web in root.iter(config.we_content_regex_list_main_tag_name):
        # web.attrib = dictionary format,{'url:zzz','content':zzz, 'date:zzz',etc...}
        # web.attrib stored in list format
        config.web_content_regex.append(web.attrib)
		
def check_current_product_tag_patterns(cur_domain):
    for web in config.web_content_regex:
        # eg:- cur_domain = www.google.com
        # check the current web pattern in all web content pattern
        check_web = re.findall(str(web.get(config.we_content_regex_xml_url_attribute)), cur_domain)
        # check_web = list format
        # if check_web total length != 0 this is a current web content regex.
        if(len(check_web) != config.init_num) :
            # get current web all products tag
            config.current_products_pattern = web.get('products_all')
            # get current web all products title tag
            config.current_product_name_pattern = web.get('products_title')
            # get current web all products price tag
            config.current_product_price_pattern = web.get('products_price')
            break
def show_output():    
    for web_num in range(len(config.total_products_list)):
    # website = input website
        website = config.total_products_list[web_num]
        print website[config.init_num].get('web')
        for product_num in range(len(website)):
            dic = website[product_num]
            print dic.get('name'),'------------', dic.get('price')

def stop_reactor():
    # scrapy functionality completed
    reactor.stop()