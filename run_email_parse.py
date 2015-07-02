import scrapy
from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from scrapy.utils.log import configure_logging
import logging
import re,sys
from scrapy.conf import settings

settings.set('LOG_LEVEL', 'INFO')

class EmailSpider(CrawlSpider):
    name = 'email'

    rules = (
        Rule(LinkExtractor(allow=(), allow_domains=(['jana.com'])), callback='parse_start_url', follow=True),
    )
      
    def __init__(self, **kwargs):
        CrawlSpider.__init__(self) 
	self.allowd_domains = [kwargs['domain']]
	self.start_urls= ["http://www."+kwargs['domain']]
        self.driver = webdriver.Chrome()
	self.filename = kwargs['output']
        dispatcher.connect(self.spider_closed, signals.spider_closed)
	self.visited = {}
	self.email_list = set()

    def spider_closed(self, spider):
	with open(self.filename,'w') as f:
	    f.write('\n'.join(self.email_list))
        self.driver.quit() 
    
    def parse_start_url(self, response):
	#extract ng-click web-page
        additional_pages = response.css('span::attr(ng-click)').re(r'changeRoute\(\'(\w+)\'\)')
        for url in additional_pages:
	    if url not in self.visited:
		self.visited[url] = 1
                yield Request(response.url+'/'+url, callback=self.parse_jssite_url)
	
	#handle static dom
	for sel in response.css('a[href*="'+self.allowd_domains[0]+'"]::attr(href)'):
	    self.add_to_list(sel.extract())
	
    
    def parse_jssite_url(self,response):
	#handle dynamic dom
        self.driver.get(response.url)
        elms = self.driver.find_elements_by_partial_link_text('@jana.com')
	for elm in elms:
	    self.add_to_list(elm.get_attribute('href'))

    def add_to_list(self, s):
	m = re.match('(mailto\:)?([\w\.]+)@'+self.allowd_domains[0], s)
	if m:
            self.email_list.add('{0}@{1}'.format(m.groups()[1],self.allowd_domains[0]))


if __name__ == "__main__":
    process = CrawlerProcess(settings)
    process.crawl(EmailSpider, domain=sys.argv[1], output=sys.argv[2])
    process.start()
