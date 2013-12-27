from parser_base import Parser
from grab.spider import Spider, Task
from grab import Grab
import logging

class EdaMollParser(Parser):
    Name = 'edamoll.ru'
    Link = 'http://edamoll.ru'
    Source = None
    
    def parse(self, *args, **kwargs):
        logger = logging.getLogger('grab')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)        
        link = self.Link
        self.ResetUpdateFlag()
        threads = int(kwargs['threads'])
        spider = EdaMollSpider(thread_number=threads, parser=self)
        proxy_types = ['http','socks4','socks5']
        if 'proxies' in kwargs:
            proxies = kwargs['proxies']
            spider.load_proxylist(source=proxies, source_type='list', proxy_type=proxy_types[int(kwargs['ptype'])])
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
            product = {'category':task.url.split('/')[-2], 'id':item_id, 'name':item_name}
            self.parser.GetProduct(product)
            yield Task('params', url=self.parser.Link+'/item/'+item_id)
        if grab.doc.select('//a[@class="nav-next"]').count()>0:
            yield Task('product', url=self.parser.Link+grab.doc.select('//a[@class="nav-next"]').attr('href'))
            
    def task_params(self, grab, task):
        product = task.url.split('/')[-1]
        pname = 'image'
        pval = self.parser.Link+grab.doc.select('//div[@class="catalog-element-image"]/img').attr('src')
        param={'name':pname, 'value':pval, 'product':product}
        self.parser.UpdateParam(param);
        price_item= grab.doc.select('//span[@itemprop="price"]')
        param = {'name':'price', 'value':str(float(price_item.text())/100), 'product':product}
        self.parser.UpdateParam(param);
        propnames = grab.doc.select('//div[contains(concat(" ", normalize-space(@class), " "), " catalog-element-prop ")]/b[@class="propname"]')[1:]
        propvalues = grab.doc.select('//div[contains(concat(" ", normalize-space(@class), " "), " catalog-element-prop ")]/span[@class="propval"]')
        i=0
        while i<len(propnames):
            self.parser.UpdateParam({'name':propnames[i].text().strip(), 'value':propvalues[i].text().strip(), 'product':product });
            i+=1
        self.parser.CleanDeleted()
        
