from typing import Iterable
import scrapy
from bs4 import BeautifulSoup
import json

from scrapy.http import Request
from IT_Viec.items import ItViecItem

class ItviecSpider(scrapy.Spider):
    name = "itviec"
    allowed_domains = ["itviec.com", "proxy.scrapeops.io"]
    def start_requests(self):
        for page_number in range(1, 10):
            start_url = "https://itviec.com/it-jobs?page=" + str(page_number)
            yield scrapy.Request(start_url, callback=self.parse)
 
    def parse(self, response):
        script_ = response.css('script[type="application/ld+json"]').get()
        soup_ = BeautifulSoup(script_, 'html.parser')
        script_content_ = soup_.find('script', type='application/ld+json').string
        json_data_ = json.loads(script_content_)
        if len(json_data_["itemListElement"]) > 0:
            for cv_count in range(len(json_data_["itemListElement"])):
                job_url = json_data_["itemListElement"][cv_count]["url"]
                yield scrapy.Request(job_url, callback = self.it_parse)
        
    def it_parse(self, response):
        ID = "ITV_" + str(response.url.split("-")[-1])
        Web = "ITViec"
        Nganh = "IT"
        Link = response.url
        TenCV = response.css('div.job-header-info h1::text').get()
        CongTy = response.css('div.job-header-info div.employer-name::text').get()
        #**********************************************************************************
        script = response.css('.flex-grow-1 script').get()
        soup = BeautifulSoup(script, 'html.parser')
        script_content = soup.find('script', type='application/ld+json').string
        json_data = json.loads(script_content)
        #**********************************************************************************
        TinhThanh = json_data["jobLocation"][0]["address"]["addressRegion"]
        Luong = json_data["baseSalary"]["value"]["value"]
        LoaiHinh = json_data["employmentType"]
        if json_data["experienceRequirements"] == "No requirements":
            KinhNghiem = "Không yêu cầu"
        else:
            KinhNghiem = str(round(json_data["experienceRequirements"]["monthsOfExperience"]/12)) + " năm"
        CapBac = json_data["skills"]
        #**********************************************************************************
        des = json_data["description"]
        PhucLoi = des.split("Why You'll Love Working Here")[1]
        YeuCau = des.split("Why You'll Love Working Here")[0].split("Your Skills and Experience")[1]
        MoTa = des.split("The Job")[1].split("Your Skills and Experience")[0]
        #**********************************************************************************
        HanNopCV = json_data["validThrough"]
        SoLuong = "1"
        item = ItViecItem()
        
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
        item["SoLuong"] = SoLuong
        # for key in ['ID', 'Web', 'Nganh', 'Link', 'TenCV', 'CongTy', 'TinhThanh', 'Luong', 'LoaiHinh', 'KinhNghiem', 'CapBac', 'YeuCau', 'MoTa', 'PhucLoi', 'HanNopCV']:
        #     if item[key] is not None:
        #         item[key] = item[key]
        #     else:
        #         item[key] = ''
        yield item