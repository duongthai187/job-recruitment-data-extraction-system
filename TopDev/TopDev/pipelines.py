import mysql.connector
from itemadapter import ItemAdapter

class CleanItem:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        value = adapter.get('MoTa')
        value = value.replace("\\r\\n", "")
        value = value.replace("<\\/span>", "")
        value = value.replace("<\\/strong>", "")
        value = value.replace("<\\/p>", "")
        value = value.replace("<\\/li>", "")
        value = value.replace("<\\/ul>", "")
        adapter['MoTa'] = value.strip()
        return item


class SaveToMySQL_test_Pipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='103.200.22.212',
            port='3306',
            user='dulieutu',
            password=':EHr0H1o5.Pro2',
            database='dulieutu_TTTuyenDung'
        )

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """
            REPLACE INTO Stg_ThongTin(Web, Nganh, Link, TenCV, CongTy, TinhThanh, Luong, LoaiHinh, KinhNghiem, CapBac, HanNopCV, YeuCau, MoTa, PhucLoi, SoLuong) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cur.execute(sql, (item['Web'], item['Nganh'], item['Link'], item['TenCV'], item['CongTy'], item['TinhThanh'], item['Luong'], item['LoaiHinh'], item['KinhNghiem'], item['CapBac'], item['HanNopCV'], item['YeuCau'], item['MoTa'], item['PhucLoi'], item['SoLuong']))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()