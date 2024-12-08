import scrapy
import math
import json
from hust_ts.items import Hust_Item

class HustSpider(scrapy.Spider):
    name = "hust"

    def start_requests(self):
        yield scrapy.Request("https://ts.hust.edu.vn/", callback = self.parse)
        
    def parse(self, response):
        link_tree = {}
        for tab in response.css('.main-menu li'):
            if tab.css('a span::text').get() in ['Hướng nghiệp', 'Tuyển sinh Đại học', 'International Admissions', 'Học phí - Học bổng', 'Liên hệ']:
                link_tree[tab.css('a span::text').get()] = {}
                link_tree[tab.css('a span::text').get()]['Link'] = tab.css('a::attr(href)').get()
                for subtab in tab.css('ul li'):
                    link_tree[tab.css('a span::text').get()][subtab.css('a span::text').get()] = subtab.css('a ::attr(href)').get()

            if tab.css('a span::text').get() == 'Tuyển sinh Sau đại học':
                link_tree[tab.css('a span::text').get()] = {}
                link_tree[tab.css('a span::text').get()]['Link'] = 'https://ts.hust.edu.vn/p/sau-dai-hoc'
                link_tree[tab.css('a span::text').get()]['Tuyển sinh Kỹ sư chuyên sâu'] = 'https://ts.hust.edu.vn/b/tuyen-sinh-ky-su-chuyen-sau'
                link_tree[tab.css('a span::text').get()]['Tuyển sinh cao học'] = {}
                link_tree[tab.css('a span::text').get()]['Tuyển sinh cao học']['Link'] = 'https://ts.hust.edu.vn/b/tuyen-sinh-cao-hoc'
                link_tree[tab.css('a span::text').get()]['Tuyển sinh cao học']['Đăng ký thạc sĩ online'] = 'https://sdh.hust.edu.vn/default.aspx?scid=61'
                link_tree[tab.css('a span::text').get()]['Tuyển sinh cao học']['Ngành đào tạo thạc sĩ'] = 'https://ts.hust.edu.vn/tin-tuc/danh-muc-chuyen-nganh-dao-tao-thac-si-ap-dung-tu-nam-2022'
                link_tree[tab.css('a span::text').get()]['Tuyển sinh nghiên cứu sinh'] = {}
                link_tree[tab.css('a span::text').get()]['Tuyển sinh nghiên cứu sinh']['Link'] = 'https://ts.hust.edu.vn/b/tuyen-sinh-ncs'
                link_tree[tab.css('a span::text').get()]['Tuyển sinh nghiên cứu sinh']['Mẫu hồ sơ Nghiên cứu sinh'] = 'https://drive.google.com/file/d/1HJzXv98VfoP89LjZeLpfxkjTWzZUeRIF/view?usp=sharing'

        for Tab in link_tree.keys():
            for SubTab in link_tree[Tab].keys():
                if SubTab not in ['Tuyển sinh cao học', 'Tuyển sinh nghiên cứu sinh'] :
                    yield scrapy.Request(link_tree[Tab][SubTab], callback=self.Hust_parse_page, meta={'Tab': Tab, 'SubTab': SubTab})
                else:
                    for SubSubTab in link_tree[Tab][SubTab].keys():
                        yield scrapy.Request(link_tree[Tab][SubTab][SubSubTab], callback=self.Hust_parse_page, meta={'Tab': Tab, 'SubTab': SubTab, 'SubSubTab': SubSubTab})
        

    def Hust_parse_page(self, response):
        try:
            max_page = int(response.css('.page-item a::text').extract()[-2])
            for page in range (1, max_page+1):
                yield scrapy.Request(f"{response.url}?page={page}", callback=self.Hust_parse, meta = response.meta)
        except:
            yield scrapy.Request(response.url, callback=self.Hust_parse, meta = response.meta)
        

    def Hust_parse(self, response):
        Tab = response.meta.get('Tab')
        SubTab = response.meta.get('SubTab') if response.meta.get('SubTab') != 'Link' else ""
        SubSubTab = response.meta.get('SubSubTab', "")
        if response.css('.description .list-item .item'):
            for item in response.css('.description .list-item .item'):
                Img = item.css('img::attr(src)').get()
                Title = item.css('.desc h3 a::text').get()
                SubDescription = item.css('.desc p:not(.date-created) ::text').get()
                Link = item.css('.desc h3 a ::attr(href)').get()
                meta = {'Tab': Tab, 'SubTab': SubTab, 'Img': Img, 'Title': Title, 'SubDescription': SubDescription, 'Link': Link, 'SubSubTab': SubSubTab}
                yield scrapy.Request(Link, callback=self.Hust_parse_content, meta=meta)
    
    def Hust_parse_content(self, response):
        DateCreated = response.css('.date-created ::text').get()
        HTML_Content = response.css('div[id="content"]').get()

        Item = Hust_Item()
        Item['Tab'] = response.meta.get('Tab')
        Item['SubTab'] = response.meta.get('SubTab')
        Item['SubSubTab'] = response.meta.get('SubSubTab')
        Item['Img'] = response.meta.get('Img')
        Item['Title'] = response.meta.get('Title')
        Item['DateCreated'] = DateCreated
        Item['SubDescription'] = response.meta.get('SubDescription')
        Item['Link'] = response.url
        Item['HTML_Content'] = HTML_Content
        
        yield Item
