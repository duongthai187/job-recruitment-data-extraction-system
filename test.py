# import asyncio
# import json
# from selenium_driverless import webdriver
# from selenium_driverless.types.by import By
# from selenium_driverless.scripts.network_interceptor import NetworkInterceptor, InterceptedRequest, InterceptedAuth, \
#     RequestPattern, RequestStages
# links = []

# async def on_request(data: InterceptedRequest):
#     if "https://shopee.vn/api/v4/recommend/" in data.request.url:
#         await data.continue_request(intercept_response=True)
    

# async def main():
#     async with webdriver.Chrome() as driver:


#         async with NetworkInterceptor(driver, on_request=on_request, patterns=[RequestPattern.AnyRequest],
#                                       intercept_auth=False) as interceptor:
#             asyncio.ensure_future(driver.get("https://shopee.vn/Thi%E1%BA%BFt-B%E1%BB%8B-%C4%90i%E1%BB%87n-T%E1%BB%AD-cat.11036132", wait_load=True))
#             await driver.sleep(2)

#             try:
#                 elements = await driver.find_elements(By.CSS_SELECTOR, 'a.shopee-category-list__sub-category')
#                 # In ra các href và text của mỗi phần tử
#                 for elem in elements:
#                     href = await elem.get_attribute("href")
#                     text = await elem.text
#                     print(f"Link: {href}, Text: {text}")
#                     links.append(href)
#             except Exception as e:
#                 print(f"Error: {e}")
#             for link in links:
#                 for page in range(0, 9):
#                     link_page = f"{link}?page={page}"
#                     driver.get(link_page)


#                     async for data in interceptor:
#                         if "https://shopee.vn/api/v4/recommend/" in data.request.url:
#                             if data.stage == RequestStages.Response:
#                                 # print(json.loads(await data.body))
#                                 break
            
#             await driver.sleep(2)

#             try:
#                 elements = await driver.find_elements(By.CSS_SELECTOR, 'a.shopee-category-list__sub-category')

#                 # In ra các href và text của mỗi phần tử
#                 for elem in elements:
#                     href = await elem.get_attribute("href")
#                     text = await elem.text
#                     print(f"Link: {href}, Text: {text}")

#             except Exception as e:
#                 print(f"Error: {e}")

# asyncio.run(main())

import asyncio
import json
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from selenium_driverless.scripts.network_interceptor import NetworkInterceptor, InterceptedRequest, InterceptedAuth, \
    RequestPattern, RequestStages
from curl_cffi import requests

async def on_request(data: InterceptedRequest, driver):
    if "https://shopee.vn/api/v4/recommend/" in data.request.url:
        await data.continue_request(intercept_response=True)


async def main():
    async with webdriver.Chrome() as driver:
        # for cookie in cookies:
        #     driver.add_cookie(cookie)

        async with NetworkInterceptor(driver, on_request=lambda data: on_request(data, driver), patterns=[RequestPattern.AnyRequest],
                                      intercept_auth=False) as interceptor:

            asyncio.ensure_future(driver.get("https://shopee.vn/Th%E1%BB%9Di-Trang-N%E1%BB%AF-cat.11035639", wait_load=True))
            async for data in interceptor:
                if "https://shopee.vn/api/v4/recommend/" in data.request.url:
                    if data.stage == RequestStages.Response:
                        print(json.loads(await data.body))
                        break
asyncio.run(main())

# links = []
# all_json_data = []  # Danh sách để lưu tất cả dữ liệu JSON

# async def on_request(data: InterceptedRequest):
#     if "https://shopee.vn/api/v4/recommend/" in data.request.url:
#         await data.continue_request(intercept_response=True)

# async def main():
#     async with webdriver.Chrome() as driver:

#         # Khởi động NetworkInterceptor
#         async with NetworkInterceptor(driver, on_request=on_request, patterns=[RequestPattern.AnyRequest], intercept_auth=True) as interceptor:
            
#             # Truy cập vào trang chính
#             await driver.get("https://shopee.vn/Thi%E1%BA%BFt-B%E1%BB%8B-%C4%90i%E1%BB%87n-T%E1%BB%AD-cat.11036132")
#             await driver.sleep(5)  # Chờ trang tải xong

#             try:
#                 # Tìm tất cả các liên kết trong phần tử với class "shopee-category-list__sub-category"
#                 elements = await driver.find_elements(By.CSS_SELECTOR, 'a.shopee-category-list__sub-category', timeout=10)
                
#                 # In ra các href và text của mỗi phần tử
#                 for elem in elements:
#                     href = await elem.get_attribute("href")
#                     text = await elem.text
#                     print(f"Link: {href}, Text: {text}")
#                     links.append(href)
#             except Exception as e:
#                 print(f"Error: {e}")

#             # Lặp qua các liên kết và tải các trang
#             for link in links:
#                 for page in range(0, 9):  # Lặp qua 9 trang (page từ 1 đến 9)
#                     link_page = f"{link}?page={page}"
#                     print(f"Loading page: {link_page}")
#                     await driver.get(link_page)  # Truy cập vào trang mới
                    
#                     # Lắng nghe response từ API
#                     async for data in interceptor:
#                         if "https://shopee.vn/api/v4/recommend/" in data.request.url:
#                             if data.stage == RequestStages.Response:
#                                 # Lấy dữ liệu JSON từ response
#                                 json_data = json.loads(await data.body)
#                                 print(json.loads(await data.body))
#                                 all_json_data.append(json_data)  # Thêm dữ liệu vào danh sách all_json_data
#                                 break

#             # Lưu tất cả dữ liệu JSON vào file sau khi xử lý xong
#             try:
#                 with open('data.json', 'w', encoding='utf-8') as f:
#                     json.dump(all_json_data, f, ensure_ascii=False, indent=4)  # Ghi tất cả dữ liệu vào file
#                 print("Data saved to data.json")
#             except Exception as e:
#                 print(f"Error saving data to file: {e}")

# # Chạy chương trình
# asyncio.run(main())


