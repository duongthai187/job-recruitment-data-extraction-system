import scrapy
from curl_cffi import requests

class HighQualitySpider(scrapy.Spider):
    name = "high_quality"
    def start_requests(self):
        yield scrapy.Request("https://ts.hust.edu.vn/en/program-cate/undergraduate-programs", callback = self.list_parse)

    def list_parse(self, response):
        link_list = response.css('.accordion-item a.read-more::attr(href)').extract()
        for link in link_list:
            yield scrapy.Request(link, callback = self.subparse)

    def subparse(self, response):
        for info in response.css('.col-9 p'):
            if "Training language" in info.css('::text').get():
                Training_language =  info.css('strong::text').get()
            if "Admission code" in info.css('::text').get():
                Admission_code =  info.css('strong::text').get()

        cookies = {
            '_ga_TT1NML6EJM': 'GS1.1.1732677146.8.0.1732677277.0.0.0',
            '_ga_QVKBY6H48C': 'GS1.1.1733122980.6.1.1733122987.0.0.0',
            '_ga': 'GA1.1.1783986823.1725934267',
            '_ga_JMQCRQZJCH': 'GS1.3.1733122980.5.1.1733122987.0.0.0',
            '_ga_CWFTHLQHPT': 'GS1.1.1733217629.17.1.1733217670.0.0.0',
            '_ga_3QT93G99KF': 'GS1.1.1733679119.18.0.1733679119.0.0.0',
            'XSRF-TOKEN': 'eyJpdiI6ImEyalNTTTR2L1oya0xYQUtQMDhKM3c9PSIsInZhbHVlIjoiNnZ3QlBaWE9LUmQ5a0JzSWtoSjBxdzQvS3QrWFMzMW5aWk5kMkhGNzRmNjM5VjI1bU9EcXdJSEJ6V2FxbXNkajQ2a1dpMU9qTVdMMUcrUnMyMC9TRUVNUnhwc0FINGh6d3hkQjdIeXF0aUF5NnBYS0FRWDU3MXU4cXBlOWo5VXgiLCJtYWMiOiI5MzY1Yjg3ZTNiNGI1ODlkZWNkZmVhMDM4MDM5M2I1NDZkODZkOTdkNzg1ZGI3MzYxN2NlMzZkYzI0MmE5MzVmIiwidGFnIjoiIn0%3D',
            'laravel_session': 'eyJpdiI6IlpkMFZuSVZZQW9XZy8zRDhNY3pubFE9PSIsInZhbHVlIjoiUUVXS2ZNYk1ocit4b2xBaUVWdjFFcFJKY2o2TkpqV3ZzRFpSVjdZcENYalZvVWlBNmc2aHhMY3hsWmlGcmJldGpRN1pNWk9XSWRHMC83VzhKZG9PQkp4Q1RwVjhDTlRnM0VaWlRlczBoY2JDYmNSbmF3R3p6UU9RNE93bSs3bWQiLCJtYWMiOiJkODU2MGMzNTE3NTQxMjFhZGEyNWNjYjVlMzdmNjRmNWNmZDdjYmJmYzQyYzdiZjgyZDZlYTExZTdhYzI2ZjlkIiwidGFnIjoiIn0%3D',
            '_ga_33T6RC7PFB': 'GS1.1.1733678491.6.1.1733680505.0.0.0',
        }

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

        data = {
            '_token': 'rcDkWBGGHOUj0dX3E6BOG1dXnC9t917UOYbA5iab',
        }

        Xet_tuyen_cac_nam = {}
        for year in range(2020, 2025):
            data['_year'] = year
            data['_slug'] = response.url.split("/")[-1]
            headers['Referer'] = response.url
            results = requests.post(
                'https://ts.hust.edu.vn/en/training-point',
                cookies=cookies,  # Cookies truyền từ biến 'cookies'
                headers=headers,  # Headers truyền từ biến 'headers'
                data=data,  # Dữ liệu POST
                verify=False
            ).json()

            try:
                Xet_tuyen_cac_nam[year] = {}
                Xet_tuyen_cac_nam[year]["Talent recruitment"] = results["data"]["admission_form"]
                Xet_tuyen_cac_nam[year]["Admissions targets"] = results["data"]["target"]
            except:
                continue

        MoTa_1 = "".join(response.css('.wrap_view ::text').extract())
        MoTa_2 = "".join(response.css('.desc-cont ::text').extract())
        QuanLy = "".join(response.css('.contact_tv ::text').extract())

        yield {
            'Training language': Training_language,
            'Admission code': Admission_code,
            'Recruiement': Xet_tuyen_cac_nam,
            'Description_1': MoTa_1,
            'Description_2': MoTa_2,
            'Management': QuanLy
        }
