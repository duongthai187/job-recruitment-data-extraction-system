from typing import Iterable
import scrapy
from scrapy.http import Request
from techwork.items import IT_Item

class TechworkwebSpider(scrapy.Spider):
    name = "techworkweb"
    allowed_domains = ["techworks.vn"]

    def start_requests(self):
        for page_number in range(1, 650):
            yield scrapy.Request(f"https://techworks.vn/viec-lam?p={page_number}", callback = self.parse)

    def parse(self, response):
        job_url_list = response.css('.job-tittle.job-tittle2 a[target="_blank"]::attr(href)').extract()
        for job_url in job_url_list:
            if 'https://techworks.vn' in job_url:
                yield scrapy.Request(job_url, callback = self.it_parse)
            else:
                next = 'https://techworks.vn' + job_url
                yield scrapy.Request(next, callback = self.it_parse)
    
    def it_parse(self, response):
        Web = 'TechWorks'
        Nganh = 'IT'
        Link = response.url
        TenCV = response.css('.job-title::text').get().replace("\\r\\n", "").strip()
        CongTy = response.css('a[class="company-name"]::text').get().replace("\\r\\n", "").strip()
        TinhThanh = response.css('[class="company-location"] a::text').get().split(",")[-1]
        Luong = response.css('[class="salary"] span::text').get()
        for i in range(len(response.css('[class="summary-content"]'))):
            if 'Loại công việc' in response.css('[class="summary-content"]')[i].css('.content-label::text').get():
                LoaiHinh = response.css('[class="summary-content"]')[i].css('.content::text').get()
        KinhNghiem = "Không có"
        CapBac = "Không có"
        
        YeuCau = ""
        YeuCau_List = response.css('.job-experience  *::text').getall()
        for i in range(len(YeuCau_List)):
            YeuCau += YeuCau_List[i]
        
        MoTa = ""
        MoTa_List = response.css('.job-description  *::text').getall()
        for i in range(len(MoTa_List)):
            MoTa += MoTa_List[i]
            
        PhucLoi = ""
        PhucLoi_List = response.css('.job-benefits  *::text').getall()
        for i in range(len(PhucLoi_List)):
            PhucLoi += PhucLoi_List[i]
        
        HanNopCV = response.css('[class="expiry"]::text').get().split()[-1]
        SoLuong ="1"
        
        item = IT_Item()
        item['Web'] = Web
        item['Nganh'] = Nganh
        item['Link'] = Link
        item['TenCV'] = TenCV
        item['CongTy'] = CongTy
        item['TinhThanh'] = TinhThanh
        item['Luong'] = Luong
        item['LoaiHinh'] = LoaiHinh
        item['KinhNghiem'] = KinhNghiem
        item['CapBac'] = CapBac
        item['YeuCau'] = YeuCau
        item['MoTa'] = MoTa
        item['PhucLoi'] = PhucLoi
        item['HanNopCV'] = HanNopCV
        item['SoLuong'] = SoLuong
        
        yield item