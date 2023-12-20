import scrapy
from joboko.items import IT_Item

class JobokowebSpider(scrapy.Spider):
    name = "jobokoweb"
    allowed_domains = ["vn.joboko.com"]

    def start_requests(self):
        for page_number in range(1, 60):
            yield scrapy.Request(f"https://vn.joboko.com//viec-lam-nganh-it-phan-mem-cong-nghe-thong-tin-iot-dien-tu-vien-thong-xni124?p={page_number}", callback = self.parse)
    
    def parse(self, response):
        job_url_list = response.css('.item-title a::attr(href)').extract()
        for job_url in job_url_list:
            if 'https://vn.joboko.com' in job_url:
                yield scrapy.Request(job_url, callback = self.it_parse)
            else:
                next = 'https://vn.joboko.com' + job_url
                yield scrapy.Request(next, callback = self.it_parse)
                
    def it_parse(self, response):
        Web = 'Joboko'
        Nganh = 'IT'
        Link = response.url
        TenCV = response.css('[class="nw-company-hero__info"] h2 a::text').get()
        CongTy = response.css('[class="nw-company-hero__info"]  a.nw-company-hero__text::text').get()
        TinhThanh = response.css('[class="nw-company-hero__address"]  a::text').get()
        Luong = response.css('[class="col-12"]  span::text').get()
        KinhNghiem = "Không có"
        CapBac = "Không có"
        for i in range(len(response.css('[class="col-12 col-md-6"]'))):
            if 'Loại hình' in response.css('[class="col-12 col-md-6"]')[i].css('.item-content::text').get():
                LoaiHinh =  response.css('[class="col-12 col-md-6"]')[i].css('span::text').get()
            if 'Kinh nghiệm' in response.css('[class="col-12 col-md-6"]')[i].css('.item-content::text').get():
                KinhNghiem = response.css('[class="col-12 col-md-6"]')[i].css('span::text').get()
            if 'Chức vụ' in response.css('[class="col-12 col-md-6"]')[i].css('.item-content::text').get():
                CapBac = response.css('[class="col-12 col-md-6"]')[i].css('span::text').get()
        
        YeuCau = ""
        YeuCau_List = response.css('[class="text-justify"]')[1].css('*:not(:empty)::text').getall()
        for i in range(len(YeuCau_List)):
            YeuCau += YeuCau_List[i]
        
        MoTa = ""
        MoTa_List = response.css('[class="text-justify"]')[0].css('*:not(:empty)::text').getall()
        for i in range(len(MoTa_List)):
            MoTa += MoTa_List[i]
        
        PhucLoi =""
        PhucLoi_List = response.css('[class="text-justify"]')[0].css('*:not(:empty)::text').getall()
        for i in range(len(PhucLoi_List)):
            PhucLoi += PhucLoi_List[i]
        
        HanNopCV = response.css('[class="item-date"]::attr(data-value)').get().split("T")[0]
        SoLuong= "1"

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