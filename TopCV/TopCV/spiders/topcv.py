import scrapy
import math
from TopCV.items import IT_Item
from datetime import date, timedelta
from TopCV.pipelines import DatabaseConnector

class TopcvSpider(scrapy.Spider):
    name = "topcv"

    def start_requests(self):
        # db_connector = DatabaseConnector(host='127.0.0.1', port = 3306, user='root', password='Camtruykich123', database='tuyendung_2')
        db_connector = DatabaseConnector(host='103.56.158.31', port = 3306, user='tuyendungUser', password='sinhvienBK', database='ThongTinTuyenDung')
        remove_url_list_local = db_connector.get_links_from_database()
        self.remove_url_list = remove_url_list_local
        print("Số lượng url trong CSDL: ", len(self.remove_url_list))
        yield scrapy.Request("https://www.topcv.vn/tim-viec-lam-moi-nhat", callback = self.parse)
        
    def parse(self, response):
        job_count = response.css('h1[class="search-job-heading"]::text').get()
        words = job_count.split()
        for word in words:
            if word.replace('.', '').isdigit():  # Kiểm tra xem từ có phải là số sau khi loại bỏ dấu chấm
                job_count = int(word.replace('.', ''))  # Chuyển đổi thành số và loại bỏ dấu chấm
                break
        if (int(job_count) % 50 == 0):
            max_page  = int(job_count) / 50
        else:
            max_page = math.floor(int(job_count) / 50) + 1
        if max_page >= 200:
            max_page = 200
        for page_number in range(1, max_page+1):
            yield scrapy.Request(f"https://www.topcv.vn/tim-viec-lam-moi-nhat?page={page_number}", callback = self.job_parse)
            
    def job_parse(self, response):
        job_list_url = response.css('div.job-item-search-result.job-ta h3.title a::attr(href)').extract()
        for job_url in job_list_url:
            if job_url in self.remove_url_list:
                print("Trùng lặp: ", job_url)
                continue
            else:
                if "https://www.topcv.vn/brand/" in job_url:
                    continue
                else:
                    yield scrapy.Request(job_url, callback = self.it_parse_2)
    
    def it_parse_2(self, response):
        Web = 'TopCV'
        Img = response.css('.company-logo img::attr(src)').get()
        for Nganh_demo in response.css('.box-category'):
            try:
                if Nganh_demo.css('.box-title::text').get() == 'Ngành nghề':
                    Nganh = Nganh_demo.css('.box-category-tags a::text').get()
                    break
            except:
                print("lỗi")
        Link = response.url
        TenCV = "".join(response.css('h1.job-detail__info--title ::text').extract())
        CongTy = "".join(response.css('.company-name-label ::text').extract())
        
        # Lấy thông tin lương, địa điểm, kinh nghiệm
        for section in response.css('.job-detail__info--section-content'):
            title_text = section.css('.job-detail__info--section-content-title::text').get()

            if title_text == 'Mức lương':
                Luong = section.css('.job-detail__info--section-content-value::text').get() or "Không có"
            elif title_text == 'Địa điểm':
                TinhThanh = section.css('.job-detail__info--section-content-value::text').get() or "Không có"
            elif title_text == 'Kinh nghiệm':
                KinhNghiem = section.css('.job-detail__info--section-content-value::text').get() or "Không có"

        # Lấy thông tin cấp bậc, số lượng tuyển, loại hình làm việc
        for info_item in response.css('.box-general-group-info'):
            title_text = info_item.css('.box-general-group-info-title::text').get()

            if title_text == 'Cấp bậc':
                CapBac = info_item.css('.box-general-group-info-value::text').get() or "Không có"
            elif title_text == 'Số lượng tuyển':
                SoLuong = info_item.css('.box-general-group-info-value::text').get() or "Không có"
            elif title_text == 'Hình thức làm việc':
                LoaiHinh = info_item.css('.box-general-group-info-value::text').get() or "Không có"

        
        deadline_text = response.css('.job-detail__info--deadline ::text').getall()
        HanNopCV = deadline_text[-1].strip() if deadline_text else date.today()
        
        for item in response.css('.job-description__item'):
            title = item.css('h3::text').get().lower()  # Lấy tiêu đề và chuyển thành chữ thường để so sánh

            if "mô tả" in title:
                MoTa = " ".join(text.strip() for text in item.css('::text').extract()) or "Không có"

            if "yêu cầu" in title:
                YeuCau = " ".join(text.strip() for text in item.css('::text').extract()) or "Không có"

            if "quyền lợi" in title:
                PhucLoi = " ".join(text.strip() for text in item.css('::text').extract()) or "Không có"

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
        item['Img'] = Img
        yield item
