import scrapy
from CareerLink.items import CareerLinkItem
from datetime import date, timedelta

class CareerlinkSpider(scrapy.Spider):
    name = "careerlink"
    allowed_domains = ["www.careerlink.vn"]
    
    def start_requests(self):
        for page_number in range(1, 101):
            page_url = "https://www.careerlink.vn/vieclam/list?page=" + str(page_number)
            yield scrapy.Request(url=page_url, callback=self.job_url_parse)
            
    def job_url_parse(self, response):
        job_url_list = response.css('li.list-group-item a.job-link::attr(href)').extract()
        for job_url in job_url_list:
            if "https://www.careerlink.vn" in job_url:
                job_next_url = job_url
            else:
                job_next_url = "https://www.careerlink.vn" + job_url
            yield scrapy.Request(url=job_next_url, callback=self.job_parse)
    
    def job_parse(self, response):
        ID = "CareerLink_" + (response.url).split("/")[-1].split("?")[0]
        Web = "CareerLink"
        for i in range(len(response.css('div[class="col-6 pl-1 pr-3 pl-md-2"]').css('div[class="job-summary-item d-block"]'))):
            if response.css('div[class="col-6 pl-1 pr-3 pl-md-2"]').css('div[class="my-0 summary-label"]')[i].css('::text').get() == "Ngành nghề":
                Nganhs_TG = response.css('div[class="col-6 pl-1 pr-3 pl-md-2"]').css('div[class="job-summary-item d-block"]')[i].css('div')[2].css('*:not(:empty)::text').getall()
        Nganh = ''
        for Nganh_TG in Nganhs_TG:
            if Nganh_TG != '\n':
                Nganh += Nganh_TG
        if 'CNTT' in Nganh:
            Nganh = 'IT'
        Link = response.url
        TenCV = response.css('h1[class="job-title mb-0"]::text').get()
        CongTy = response.css('p[class="org-name mb-2"] span::text').get()
        TinhThanh = ''
        TinhThanhs_TG = response.css('div[class="d-flex align-items-start mb-2"] *:not(:empty)::text').getall()
        for TinhThanh_TG in TinhThanhs_TG:
            if TinhThanh_TG != '\n':
                TinhThanh += TinhThanh_TG
        Luong = response.css('div[class="d-flex align-items-center mb-2"]')[0].css('span::text').get()
        KinhNghiem = response.css('div[class="d-flex align-items-center mb-2"]')[1].css('span::text').get()
        deadline = response.css('div[class="d-flex align-items-center mb-2"]')[2].css('b::text').get().split("\n")[1]
        HanNopCV = date.today() + timedelta(days = int(deadline))
        for i in range(len(response.css('div[class="col-6 pr-1 pl-3 pr-md-2"] div[class="job-summary-item d-block"]'))):
            if response.css('div[class="col-6 pr-1 pl-3 pr-md-2"] div[class="job-summary-item d-block"]')[i].css('div[class="my-0 summary-label"]::text').get() == "Cấp bậc":
                CapBac = response.css('div[class="col-6 pr-1 pl-3 pr-md-2"] div[class="job-summary-item d-block"]')[i].css('div')[2].css('::text').get()
            if response.css('div[class="col-6 pr-1 pl-3 pr-md-2"] div[class="job-summary-item d-block"]')[i].css('div[class="my-0 summary-label"]::text').get() == "Loại công việc":
                LoaiHinh = response.css('div[class="col-6 pr-1 pl-3 pr-md-2"] div[class="job-summary-item d-block"]')[i].css('div')[2].css('::text').get()
        SoLuong = 1
        MoTa = ''
        MoTas_TG = response.css('div[id="section-job-description"] *:not(:empty)::text').getall()
        for MoTa_TG in MoTas_TG:
            if MoTa_TG != '\n':
                MoTa += MoTa_TG
        YeuCau = ''
        YeuCaus_TG = response.css('div[id="section-job-skills"] *:not(:empty)::text').getall()
        for YeuCau_TG in YeuCaus_TG:
            if YeuCau_TG != '\n':
                YeuCau += YeuCau_TG
        PhucLoi = ''
        PhucLois_TG = response.css('div[id="section-job-benefits"] *:not(:empty)::text').getall()
        for PhucLoi_TG in PhucLois_TG:
            if PhucLoi_TG != '\n':
                PhucLoi += PhucLoi_TG
        item = CareerLinkItem()
        item['ID'] = ID
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
        
