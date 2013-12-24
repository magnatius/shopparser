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
        self.ResetUpdateFlag()        
        threads = int(kwargs['threads'])
        spider = EdaMollSpider(thread_number=threads, parser=self)
        spider.run()


class EdaMollSpider(Spider):
    
    def __init__(self, *args, **kwargs):
        self.parser = kwargs['parser']
        del kwargs['parser']
        super(EdaMollSpider, self).__init__(*args, **kwargs)        
        
    def task_generator(self):
        yield Task('category', url=self.parser.Link)
    
    def task_category(self, grab, task):
        for root_elem in grab.doc.select('//ul[@id="horizontal-multilevel-menu"]/li/a[contains(concat(" ", normalize-space(@class), " "), " root-item ")]'):
            category={'parent':None, 'id':root_elem.attr('href')[1:-1], 'src':self.parser.source, 'name': root_elem.text().strip()}
            self.parser.GetCategory(category)
            for parent_elem in root_elem.select('following-sibling::ul/li/a[@class="parent"]'):
                category={'parent':root_elem.attr('href')[1:-1], 'id':parent_elem.attr('href')[1:-1], 'src':self.parser.source, 'name': parent_elem.text().strip()}    
                
                self.parser.GetCategory(category)
                for elem in parent_elem.select('following-sibling::ul/li/a'):
                    category={'parent':parent_elem.attr('href')[1:-1], 'id':elem.attr('href')[1:-1], 'src':self.parser.source, 'name': elem.text().strip()}
                    self.parser.GetCategory(category)
                    yield Task('product', url=self.parser.Link+'/'+category['id']+'/')
    
    def task_product(self, grab, task):
        for product in grab.doc.select('//div[@class="catalog_item"]'):
            item_id = product.select('a').attr('href').split('/')[-1]
            item_name=product.select('.//span[@itemprop="name"]').text()
            product = {'category':task.url.split('/')[-1], 'id':item_id, 'name':item_name}
            self.parser.GetProduct(product)
            yield Task('params', url=self.parser.Link+'/item/'+item_id)
            
    def task_params(self, grab, task):
        