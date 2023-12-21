#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
# Parsing and creating xml data
from lxml import etree as et

# Store data as a csv file written out
from csv import writer

# In general to use with timing our function calls to Indeed
import time

# Assist with creating incremental timing for our scraping to seem more human
from time import sleep

# Dataframe stuff
import pandas as pd

# Random integer for more realistic timing for clicks, buttons and searches during scraping
from random import randint

# Multi Threading
import threading

# Threading:
from concurrent.futures import ThreadPoolExecutor, wait
import math
import mysql.connector
from datetime import date, timedelta
import re


# In[2]:


import selenium

# Check version I am running
selenium.__version__


# In[3]:


from selenium import webdriver

# Starting/Stopping Driver: can specify ports or location but not remote access
from selenium.webdriver.chrome.service import Service as ChromeService

# Manages Binaries needed for WebDriver without installing anything directly
from webdriver_manager.chrome import ChromeDriverManager


# In[4]:


# Allows searchs similar to beautiful soup: find_all
from selenium.webdriver.common.by import By

# Try to establish wait times for the page to load
from selenium.webdriver.support.ui import WebDriverWait

# Wait for specific condition based on defined task: web elements, boolean are examples
from selenium.webdriver.support import expected_conditions as EC

# Used for keyboard movements, up/down, left/right,delete, etc
from selenium.webdriver.common.keys import Keys

# Locate elements on page and throw error if they do not exist
from selenium.common.exceptions import NoSuchElementException


# In[5]:


response = requests.get(
  url='https://headers.scrapeops.io/v1/browser-headers',
  params={
      'api_key': 'cca4ced0-490d-41a0-b258-46f2ad7e74b3',
      'num_results': '100'}
)
header_browser_list = response.json()
print(header_browser_list['result'][0])


# In[6]:


response = requests.get(
  url='https://headers.scrapeops.io/v1/user-agents',
  params={
      'api_key': 'cca4ced0-490d-41a0-b258-46f2ad7e74b3',
      'num_results': '100'}
)
user_agent_list = response.json()
print(user_agent_list['result'][0])


# In[7]:


random_index_user_agent = randint(0, len(user_agent_list)-1)
random_index_header_browser = randint(0, len(header_browser_list)-1)
user_agent_random = user_agent_list['result'][random_index_user_agent]
header_browser_random = header_browser_list['result'][random_index_header_browser]


# In[8]:


# Allows you to cusotmize: ingonito mode, maximize window size, headless browser, disable certain features, etc
option = webdriver.ChromeOptions()

# Going undercover:
option.add_argument("--incognito")


# # Consider this if the application works and you know how it works for speed ups and rendering!

option.add_argument('--headless=chrome')
user_agent = user_agent_random
option.add_argument(f"user-agent={user_agent}")

# Thêm header vào Options
headers = header_browser_random

for key, value in headers.items():
    option.add_argument(f"--header={key}:{value}")


# In[9]:


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)

driver.get("https://jobsgo.vn/viec-lam-cong-nghe-thong-tin.html")

job_count = driver.find_element(By.CSS_SELECTOR,'[class="sidebar-widget-title mrg-bot-15"] h1').text
so = re.search(r'\b\d+\b', job_count).group()
if int(so) % 50 == 0:
    max_page = int(so) / 50
else:
    max_page = int(so) // 50 + 1
print("Max page: ", max_page)
driver.quit()


# In[18]:


conn = mysql.connector.connect(
    host='103.56.158.31',
    port = 3306,
    user= 'tuyendungUser',
    password='sinhvienBK',
    database= 'ThongTinTuyenDung'
)
cursor = conn.cursor()


# In[11]:


sql = 'INSERT IGNORE INTO Stg_ThongTin(Web, Nganh, Link, TenCV, CongTy, TinhThanh, Luong, LoaiHinh, KinhNghiem, CapBac, HanNopCV, YeuCau, MoTa, PhucLoi, SoLuong) VALUES (%s, %s, %s, %s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s,%s)'


# In[12]:


sql_link = 'SELECT Link FROM Stg_ThongTin where Web =\'Jobsgo\''


# In[13]:


cursor.execute(sql_link)
result = cursor.fetchall()
remove_url_list = [row[0] for row in result]


# In[14]:


job_urls = []
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
for page_number in range(1, int(max_page) +1):
    driver.get(f"https://jobsgo.vn/viec-lam-cong-nghe-thong-tin.html?&page={page_number}")
    sleep(randint(1, 3))
    url_list = driver.find_elements(By.CSS_SELECTOR, "div.item-click")
    for url in url_list:
        t = url.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
        job_urls.append(t)
driver.quit()
print("Số lượng url cào về: ", len(job_urls), "url")
for job_url in  remove_url_list:
    if job_url in job_urls:
        job_urls.remove(job_url)
print("Số lượng tin mới lấy được: ", len(job_urls))


# In[20]:


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=option)
if len(job_urls) > 0:
    for i in range(len(job_urls)):
        link = job_urls[i]
        driver.get(link)
        print("Đang xử lí...", link)
        Web = 'Jobsgo'
        Nganh = 'IT'
        Link = link
        TenCV = driver.find_element(By.CSS_SELECTOR, "div.media-body-2 h1").text
        CongTy = driver.find_elements(By.CSS_SELECTOR, 'div[class="panel-body"]')[1].find_element(By.CSS_SELECTOR, 'div.media div.media-body h2 a').get_attribute('text')
        TinhThanh = driver.find_element(By.CSS_SELECTOR, 'div[class="data giaphv"]').text
        Luong = driver.find_element(By.CSS_SELECTOR, '[class="saraly text-bold text-green"]').text
        for i in range(len(driver.find_elements(By.CSS_SELECTOR, 'div[class="col-sm-4 col-xs-6"]'))):
            if 'Tính chất công việc' in driver.find_elements(By.CSS_SELECTOR, 'div[class="col-sm-4 col-xs-6"]')[i].text:
                LoaiHinh = driver.find_elements(By.CSS_SELECTOR, 'div[class="col-sm-4 col-xs-6"]')[i].text.replace("Tính chất công việc", "")
            if "Yêu cầu kinh nghiệm" in driver.find_elements(By.CSS_SELECTOR, 'div[class="col-sm-4 col-xs-6"]')[i].text:
                KinhNghiem = driver.find_elements(By.CSS_SELECTOR, 'div[class="col-sm-4 col-xs-6"]')[i].text.replace("Yêu cầu kinh nghiệm", "")
            if "Vị trí/chức vụ" in driver.find_elements(By.CSS_SELECTOR, 'div[class="col-sm-4 col-xs-6"]')[i].text:
                CapBac = driver.find_elements(By.CSS_SELECTOR, 'div[class="col-sm-4 col-xs-6"]')[i].text.replace("Vị trí/chức vụ", "")
        try:        
            deadline = driver.find_element(By.CSS_SELECTOR, '[class="deadline text-bold text-orange"]').text
        except:
            continue
        HanNopCV = date.today() + timedelta(days = int(deadline))
        for i in range(len(driver.find_elements(By.CSS_SELECTOR, 'div[class="content-group"]'))):
            if 'Yêu cầu công việc' in driver.find_elements(By.CSS_SELECTOR, 'div[class="content-group"]')[i].text:
                YeuCau = driver.find_elements(By.CSS_SELECTOR, 'div[class="content-group"]')[i].text
            if 'Mô tả công việc' in driver.find_elements(By.CSS_SELECTOR, 'div[class="content-group"]')[i].text:
                MoTa = driver.find_elements(By.CSS_SELECTOR, 'div[class="content-group"]')[i].text
            if 'Quyền lợi được hưởng' in driver.find_elements(By.CSS_SELECTOR, 'div[class="content-group"]')[i].text:
                PhucLoi = driver.find_elements(By.CSS_SELECTOR, 'div[class="content-group"]')[i].text
        SoLuong = '1'
        if YeuCau is None:
            YeuCau = ""
        if MoTa is None:
            MoTa = ""
        if PhucLoi is None:
            PhucLoi = ""
        cursor.execute(sql, (Web, Nganh, Link, TenCV, CongTy, TinhThanh, Luong, LoaiHinh, KinhNghiem, CapBac, HanNopCV, YeuCau, MoTa, PhucLoi, SoLuong))
        conn.commit()
else:
    print("Không có tin mới để thêm.")
driver.quit()
cursor.close()
conn.close()

