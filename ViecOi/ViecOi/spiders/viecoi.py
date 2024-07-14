import scrapy
from ViecOi.items import ViecOi
from ViecOi.pipelines import DatabaseConnector

class ViecoiSpider(scrapy.Spider):
    name = "viecoi"
    
    
    def start_requests(self):
        db_connector = DatabaseConnector(host='103.56.158.31', port = 3306, user='tuyendungUser', password='sinhvienBK', database='ThongTinTuyenDung')
        remove_url_list_local = db_connector.get_links_from_database()
        self.remove_url_list = remove_url_list_local
        print("Số lượng url trong CSDL: ", len(self.remove_url_list))
        yield scrapy.Request("https://viecoi.vn/tim-viec/all.html", callback = self.parse)
    
    def parse(self, response):
        job_count = int(response.css('.job_number-grid b::text').get().replace(',', ""))
        if job_count % 10 == 0:
            max_page_number = job_count / 10
        else:
            max_page_number = job_count // 10 +1
        for page_number in range(1, max_page_number+1):
            yield scrapy.Request(f"https://viecoi.vn/tim-viec/all.html?page={page_number}", callback=self.list_job_parse)
    
    def list_job_parse(self, response):            
        list_job_url = response.css('.list_job_detail .title-jobs-home ::attr(href)').extract()
        for job_url in list_job_url:
            if job_url in self.remove_url_list:
                continue
            else:
                yield scrapy.Request(job_url, callback = self.job_parse)
    
    def job_parse(self, response):
        ID = "V_O_" + response.url.split("-")[-1].replace(".html", "")
        Web = "ViecOi"
        Link = response.url
        Luong = "".join(response.css('.div-salary ::text').extract())
        TenCV = response.css('.title-jobs-home ::text').get()
        for li_tag in response.css('.ul-sub-detail .hide-mobi'):
            text_content = li_tag.css('::text').get().lower()

            if 'công ty' in text_content:
                CongTy = ", ".join(text.strip() for text in li_tag.xpath('../..').css('.d-table-cell.d-table-padding ::text').extract()) or "Không có"

            if 'lĩnh vực' in text_content:
                # Sử dụng get() trực tiếp để lấy text từ thẻ <a>
                Nganh = li_tag.xpath('../..').css('.d-table-cell.d-table-padding a::text').get() or "Không có"

            if 'nơi làm việc' in text_content:
                TinhThanh = ", ".join(text.strip() for text in li_tag.xpath('../..').css('.d-table-cell.d-table-padding ::text').extract()) or "Không có"

            if 'kinh nghiệm' in text_content:
                KinhNghiem = li_tag.xpath('../..').css('.d-table-cell.d-table-padding ::text').get() or "Không có"

            if 'vị trí' in text_content:
                CapBac = li_tag.xpath('../..').css('.d-table-cell.d-table-padding ::text').get() or "Không có"

            if 'hạn nộp' in text_content:
                HanNopCV = li_tag.xpath('../..').css('.d-table-cell.d-table-padding ::text').get() or "Không có"

            if 'số lượng' in text_content:
                SoLuong = li_tag.xpath('../..').css('.d-table-cell.d-table-padding ::text').get() or "Không có"
        LoaiHinh = 'Toàn thời gian'
        Img = 'https://viecoi.vn/' + response.css('.grid-company .grid-image img::attr(src)').get()
        MoTa = "\n".join(response.css('div[id="des_company"] ::text').extract())
        YeuCau = ", ".join(response.xpath('//div[@id="kn"]/following-sibling::div').css('.tag ::text').extract())
        PhucLoi = ", ".join(response.css('div[id="prf"] .tag ::text').extract())
        item = ViecOi()
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
        
        