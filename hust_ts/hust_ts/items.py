import scrapy

class Hust_Item(scrapy.Item):
    Tab = scrapy.Field() #
    SubTab = scrapy.Field() # 
    SubSubTab = scrapy.Field() # 
    Img = scrapy.Field() #
    Title = scrapy.Field()  #
    DateCreated = scrapy.Field() #
    SubDescription = scrapy.Field() #
    Link = scrapy.Field() #
    HTML_Content = scrapy.Field() #

