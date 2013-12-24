from parser_base import Parser
from grab.spider import Spider, Task
import logging

class EdaMollParser(Parser):
    Name = 'edamoll.ru'
    Link = 'http://edamoll.ru'
    Source = None
    
    def parse(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)
        link = self.Link        
        threads = kwargs['threads']
        spider = EdaMollSpider(thread_number=threads, parser=self)
        spider.run()


class EdaMollSpider(Spider):
    
    def __init__(self, *args, **kwargs):
        super(EdaMollSpider, self).__init__(*args, **kwargs)
        self.parser = kwargs['parser']
        
    def task_generator(self):
        yield Task('category', url=self.parser.Link)
    
    def task_category(self, grab, task):
        for root_elem in grab.xpath_list('//ul[@id="horizontal-multilevel-menu"]/li/a[contains(concat(" ", normalize-space(@class), " "), " root-item ")]'):
            category={parent:None, external_id:root_elem.attrib['href'][1:-1], src:self.parser.Source, name: root_elem.text().strip()}
            self.parser.GetCategory(category)
            for parent_elem in root_elem.xpath('./ul/li/a[@class="parent"]'):
                category={parent:root_elem.attrib['href'][1:-1], external_id:parent_elem.attrib['href'][1:-1], src:self.parser.Source, name: parent_elem.text().strip()}    
                self.parser.GetCategory(category)
                for elem in parent_elem.xpath('./ul/li/a'):
                    category={parent:parent_elem.attrib['href'][1:-1], external_id:elem.attrib['href'][1:-1], src:self.parser.Source, name: elem.text().strip()}
                    self.parser.GetCategory(category)
            
        