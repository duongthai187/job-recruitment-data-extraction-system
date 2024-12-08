import scrapy
from curl_cffi import requests

class HustCtdtSpider(scrapy.Spider):
    name = "hust_ctdt"

    def start_requests(self):
        yield scrapy.Request("https://ts.hust.edu.vn/training-cate/nganh-dao-tao-dai-hoc", callback = self.list_parse)

    def list_parse(self, response):
        link_list = response.css('.accordion-item a.read-more::attr(href)').extract()
        for link in link_list:
            yield scrapy.Request(link, callback = self.subparse)

    def subparse(self, response):
        for info in response.css('.col-9 p'):
            if "Ngôn ngữ đào tạo" in info.css('::text').get():
                NgonNgu =  info.css('strong::text').get()
            if "Mã xét tuyển" in info.css('::text').get():
                MaXetTuyen =  info.css('strong::text').get()

        cookies = {
            '_ga_TT1NML6EJM': 'GS1.1.1732677146.8.0.1732677277.0.0.0',
            '_ga_QVKBY6H48C': 'GS1.1.1733122980.6.1.1733122987.0.0.0',
            '_ga': 'GA1.1.1783986823.1725934267',
            '_ga_JMQCRQZJCH': 'GS1.3.1733122980.5.1.1733122987.0.0.0',
            '_ga_CWFTHLQHPT': 'GS1.1.1733217629.17.1.1733217670.0.0.0',
            '_ga_3QT93G99KF': 'GS1.1.1733365482.16.1.1733367215.0.0.0',
            '_ga_33T6RC7PFB': 'GS1.1.1733665317.5.1.1733672016.0.0.0',
            'XSRF-TOKEN': 'eyJpdiI6ImZRMk1jSjZXVHVtNXVzUkxHNFV2WVE9PSIsInZhbHVlIjoiQjE0Ti9oeUx5Sm85amNLajNmdDgwNjNWSXRPUW9MY0ptKzd1TEpyRGhRRkRISlFDYUV2azVGYUtaMm1MZktaU1Fyc0tEWkVPeXRsSGFXcjJ0OW1CTkh1RStEVlVNMEJZRUIwR2IyYWQ1N2N0R0cwUG5adHVNeUh6Y0JoZ1ZVbjkiLCJtYWMiOiJiYzIyNDRmOWNiZjMzYmEzZDE1NGQ3ZTBiNTAwZjBmZTQ4OTE0MzQyZTcwNGJkOWJhYzMxYzc4YWFjZjAzMzgxIiwidGFnIjoiIn0%3D',
            'laravel_session': 'eyJpdiI6IkxxaWI5am9qUUNWZllqZE1UZ0VSVUE9PSIsInZhbHVlIjoiaGhjREpwQk1EQXdMeVhkSVY3THBWdU1hbzdrZjBXU21rYUsrVlJJZFNGWTdFZ0lOTWZicTVQR3o3Q0VGc0pPRFBnelpsNWtmQ3MzWFB2ZFlScDlXREpNMUNGclFKcmVlejMwbU9wc0tHR3VxTWNOZS8wMFlLS3liTXR6MGtaRlciLCJtYWMiOiIyNzk5YmM1OGY1NTEwMTU0MTEwYTI0NDIwMDVmZmY2NTE3YjA4MTg2NTFmMmE0ZjkzMjAyNjQ5YmM5Y2QwMmE1IiwidGFnIjoiIn0%3D',
        }

        # Headers
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,fr-FR;q=0.7,fr;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://ts.hust.edu.vn',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        # Form data (POST data)
        data = {
            '_token': 'rcDkWBGGHOUj0dX3E6BOG1dXnC9t917UOYbA5iab',
        }

        Chi_tieu_cac_nam = {}
        for year in range(2020, 2025):
            data['_year'] = year
            data['_slug'] = response.url.split("/")[-1]
            headers['Referer'] = response.url
            results = requests.post(
                'https://ts.hust.edu.vn/training-point',
                cookies=cookies,  # Cookies truyền từ biến 'cookies'
                headers=headers,  # Headers truyền từ biến 'headers'
                data=data,  # Dữ liệu POST
                verify=False
            ).json()

            try:
                Chi_tieu_cac_nam[year] = {}
                Chi_tieu_cac_nam[year]["Xét tuyển tài năng"] = results["data"]["admission_form"]
                Chi_tieu_cac_nam[year]["Chỉ tiêu tuyển sinh"] = results["data"]["target"]
                Chi_tieu_cac_nam[year]["Xét tuyển theo KQ Kỳ thi ĐGTD"] = {}
                Chi_tieu_cac_nam[year]["Xét tuyển theo KQ Kỳ thi TN THPT"] = {}
                for ToHop in response.css('.meta .row'):
                    if "Xét tuyển theo KQ Kỳ thi ĐGTD" in ''.join(ToHop.css(' ::text').extract()) and "Tổ hợp xét tuyển" in ''.join(ToHop.css(' ::text').extract()):
                        Chi_tieu_cac_nam[year]["Xét tuyển theo KQ Kỳ thi ĐGTD"]["Tổ hợp"] = ToHop.css('strong::text').extract()
                    Chi_tieu_cac_nam[year]["Xét tuyển theo KQ Kỳ thi ĐGTD"]["Điểm chuẩn"] = results["data"]["point_dgtd"]

                    if "Xét tuyển theo KQ Kỳ thi TN THPT" in ''.join(ToHop.css(' ::text').extract()) and "Tổ hợp xét tuyển" in ''.join(ToHop.css(' ::text').extract()):
                        Chi_tieu_cac_nam[year]["Xét tuyển theo KQ Kỳ thi TN THPT"]["Tổ hợp"] = ToHop.css('strong::text').extract()
                    Chi_tieu_cac_nam[year]["Xét tuyển theo KQ Kỳ thi TN THPT"]["Điểm chuẩn"] = results["data"]["point_tn"]
            except:
                continue

        MoTa_1 = "".join(response.css('.wrap_view ::text').extract())
        MoTa_2 = "".join(response.css('.desc-cont ::text').extract())
        QuanLy = "".join(response.css('.contact_tv ::text').extract())

        yield {
            'NgonNgu': NgonNgu,
            'MaXetTuyen': MaXetTuyen,
            'Chi_tieu_cac_nam': Chi_tieu_cac_nam,
            'MoTa_1': MoTa_1,
            'MoTa_2': MoTa_2,
            'QuanLy': QuanLy
        }
