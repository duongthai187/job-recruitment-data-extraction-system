# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
import mysql.connector

class ImportToMySQL:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='103.200.22.212',
                port='3306',
                user='dulieutu',
                password=':EHr0H1o5.Pro2',
                database='dulieutu_TTTuyenDung'
            )
            # self.conn = mysql.connector.connect(
            #     host='127.0.0.1',
            #     port='3306',
            #     user='root',
            #     password='Camtruykich123',
            #     database='tuyendung'
            # )
            ## Create cursor, used to execute commands
            self.cur = self.conn.cursor()
            print("Connected to MySQL successfully.")
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")

    def process_item(self, item, spider):
        try:
            sql = """
            REPLACE INTO Stg_ThongTin(Web, Nganh, Link, TenCV, CongTy, TinhThanh, Luong, LoaiHinh, KinhNghiem, CapBac, HanNopCV, YeuCau, MoTa, PhucLoi, SoLuong) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cur.execute(sql, (item['Web'], item['Nganh'], item['Link'], item['TenCV'], item['CongTy'], item['TinhThanh'], item['Luong'], item['LoaiHinh'], item['KinhNghiem'], item['CapBac'], item['HanNopCV'], item['YeuCau'], item['MoTa'], item['PhucLoi'], item["SoLuong"]))
            self.conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def close_spider(self, spider):
        try:
            self.cur.close()
            self.conn.close()
            print("MySQL connection closed successfully.")
        except Exception as e:
            print(f"Error closing MySQL connection: {e}")