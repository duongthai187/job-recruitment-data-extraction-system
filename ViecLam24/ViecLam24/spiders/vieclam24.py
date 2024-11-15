import scrapy
import math
from ViecLam24.items import ViecLam24Item
from ViecLam24.pipelines import DatabaseConnector

class Vieclam24Spider(scrapy.Spider):
    name = "vieclam24"
    
    def start_requests(self):
        # db_connector = DatabaseConnector(host='127.0.0.1', port = 3306, user='root', password='Camtruykich123', database='tuyendung_2')
        db_connector = DatabaseConnector(host='103.56.158.31', port = 3306, user='tuyendungUser', password='sinhvienBK', database='ThongTinTuyenDung')
        remove_url_list_local = db_connector.get_links_from_database()
        self.remove_url_list = remove_url_list_local
        print("Số lượng url trong CSDL: ", len(self.remove_url_list))
        url_get_job = "https://vieclam24h.vn/tim-kiem-viec-lam-nhanh"
        yield scrapy.Request(url_get_job, callback = self.parse)
        
    def parse(self, response):
        num_job = int(response.css('.flex.items-center.gap-4 strong::text').get().replace(",", ""))
        if num_job % 30 == 0:
            num_page = num_job/30
        else:
            num_page = math.floor(num_job/30) + 1
        for page_number in range(1, min(50, int(num_page) +1)):
        # for page_number in range(1, 200):
            url_page = f"https://vieclam24h.vn/tim-kiem-viec-lam-nhanh?page={page_number}"
            yield scrapy.Request(url_page, callback = self.get_job_list)
    
    def get_job_list(self, response):
        job_list_url = response.css('div[class="flex flex-col gap-3 sm_cv:gap-2"] a::attr(href)').extract()
        for url_job in job_list_url:
            if "https://vieclam24h.vn"in url_job:
                url_job = url_job
            else:
                url_job = "https://vieclam24h.vn" + url_job
                
            if url_job in self.remove_url_list:
                print("Trùng lặp: ", url_job)
                continue
            else:
                yield scrapy.Request(url_job, callback = self.job_parse)
    
    def job_parse(self, response):
        ID = "VL24_"+ (response.url).split("-")[-1].split(".")[0]
        Web = "Vieclam24h"
        Link = response.url
        Img = response.css('img[alt="logo"]::attr(src)').get()
        Nganh = response.css('a[class="jsx-5b2773f86d2f74b hover:text-se-accent"]::text').get()
        TenCV = response.css('.leading-snug::text').get()
        CongTy = response.css('.font-normal.text-16.text-se-neutral-64.mb-4::text').get()
        TinhThanh = response.css('a[class="hover:text-se-accent"] span::text').get()
        Luong = response.css('[class="font-semibold text-14 text-[#8B5CF6]"]::text').get()
        HanNopCV = response.css('p[class="text-14 text-[#414045]"]::text').get()
        #****************************************************************
        for col in response.css('.flex.items-center.mb-4'):
            if (cap_bac_text := col.css('p[class="mr-1 text-se-neutral-64 text-12"]::text').get()) == "Cấp bậc":
                CapBac = col.css('p[class="text-14"]::text').get() or "Không có"
            if (loai_hinh_text := col.css('p[class="mr-1 text-se-neutral-64 text-12"]::text').get()) == "Hình thức làm việc":
                LoaiHinh = col.css('p[class="text-14"]::text').get() or "Không có"
            if (kinh_nghiem_text := col.css('p[class="mr-1 text-se-neutral-64 text-12"]::text').get()) == "Yêu cầu kinh nghiệm":
                KinhNghiem = col.css('p[class="text-14"]::text').get() or "Không có"
            if (so_luong_text := col.css('p[class="mr-1 text-se-neutral-64 text-12"]::text').get()) == "Số lượng tuyển":
                SoLuong = col.css('p[class="text-14"]::text').get() or "Không có"
        #******************************************************************
        for YC_MT_PL in response.css('[class="jsx-5b2773f86d2f74b text-24 font-semibold py-4"]'):
            text_content = YC_MT_PL.css('::text').get().lower()  # Lấy nội dung text và chuyển thành chữ thường
            if "mô tả" in text_content:
                MoTa = ", ".join(text.strip() for text in YC_MT_PL.xpath('..').css('::text').extract()) or "Không có"
            if "yêu cầu" in text_content:
                YeuCau = ", ".join(text.strip() for text in YC_MT_PL.xpath('..').css('::text').extract()) or "Không có"
            if "quyền lợi" in text_content:
                PhucLoi = ", ".join(text.strip() for text in YC_MT_PL.xpath('..').css('::text').extract()) or "Không có"
                
        item = ViecLam24Item()
        item['ID'] = ID
        item['Web'] = Web
        item['Link'] = Link
        item['Nganh'] = Nganh
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
        item['Img'] = Img
        
        yield item