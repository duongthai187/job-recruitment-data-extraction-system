import scrapy
import re
from job3s.items import IT_Item

class Job3swebSpider(scrapy.Spider):
    name = "job3sweb"
    allowed_domains = ["job3s.vn"]

    def start_requests(self):
        yield scrapy.Request("https://job3s.vn/tim-viec-lam-it-phan-mem-c13?sort=1&page=1", callback = self.parse)
        
    def parse(self, response):
        job_count = response.css('.count_title::text').get()
        count = re.search(r'\b\d+\b', job_count).group()
        if int(count)%15 == 0:
            max_page = int(count) / 15
        else:
            max_page = int(count) // 15 + 1
        for page_number in range(1, max_page+1):
            yield scrapy.Request(f"https://job3s.vn/tim-viec-lam-it-phan-mem-c13?sort=1&page={page_number}", callback = self.it_parse)
        
    def it_parse(self, response):
        job_list_url = response.css('[class="content_news_title"] a::attr(href)').extract()
        for job_url in job_list_url:
            if "https://job3s.vn" in job_url:
                yield scrapy.Request(job_url, callback = self.it_parse_2)
            else:
                next = "https://job3s.vn" + job_url
                yield scrapy.Request(next, callback = self.it_parse_2)
    
    def it_parse_2(self, response):
        Web = 'Job3s'
        Nganh = 'IT'
        Link = response.url
        TenCV = response.css('[class="cl_primary pd_b12"]::text').get().replace("\n", "").strip()
        CongTy = response.css('[class="font_s20 line_h23 font_w400 cl_55"] a::text').get()
        TinhThanh = response.css('[class="my-3"] p::text').get().replace("\n", "").strip().split(":")[0].replace("-", "").strip()
        for i in range(len(response.css('[class="d_flex align_s box-item"]'))):
            text = response.css('[class="d_flex align_s box-item"]')[i].css('[class="font_s16 line_h19 font_w400 cl_55 block"]::text').get().replace("\n", "").strip()
            if "Mức" in text and "lương" in text:
                Luong = response.css('[class="d_flex align_s box-item"]')[i].css('[class="font_s16 line_h19 font_w400 cl_primary block mt_8"]::text').get().replace("\n", "").strip()
            if 'Hình' in text and 'thức làm việc' in text:
                LoaiHinh = response.css('[class="d_flex align_s box-item"]')[i].css('[class="font_s16 line_h19 font_w400 cl_primary block mt_8"]::text').get().replace("\n", "").strip()
            if 'Kinh' in text and 'nghiệm' in text:
                try:
                    KinhNghiem = response.css('[class="d_flex align_s box-item"]')[i].css('[class="font_s16 line_h19 font_w400 cl_primary block mt_8"]::text').get().replace("\n", "").strip()
                except:
                    KinhNghiem = "Không có"
            if 'Cấp' in text and 'bậc' in text:
                try:
                    CapBac = response.css('[class="d_flex align_s box-item"]')[i].css('[class="font_s16 line_h19 font_w400 cl_primary block mt_8"]::text').get().replace("\n", "").strip()
                except:
                    CapBac = "Không có"
            if 'Số' in text and 'lượng tuyển' in text:
                SoLuong = response.css('[class="d_flex align_s box-item"]')[i].css('[class="font_s16 line_h19 font_w400 cl_primary block mt_8"]::text').get().replace("\n", "").strip()
        YeuCau = ""
        YeuCau_List = response.css('[class="item_box item-box-content"]')[1].css('::text').getall()
        for i in range(len(YeuCau_List)):
            YeuCau += YeuCau_List[i]
        
        MoTa = ""
        MoTa_List = response.css('[class="item_box item-box-content"]')[0].css('::text').getall()
        for i in range(len(MoTa_List)):
            MoTa += MoTa_List[i]
            
        PhucLoi = ""
        PhucLoi_List = response.css('[class="item_box item-box-content"]')[2].css('::text').getall()
        for i in range(len(PhucLoi_List)):
            PhucLoi += PhucLoi_List[i]
        
        HanNopCV = response.css('[class="box-header-job__time"] .hight-light::text').get()

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