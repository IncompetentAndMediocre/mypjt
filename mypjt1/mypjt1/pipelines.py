# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class Mypjt1Pipeline:
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="jvtc",
                                    charset="utf8mb4")

    def process_item(self, item, spider):
        url = item["url"]
        hits = str(item["hits"])

        for j in range(0, len(item["name"])):
            name = item["name"][j]
            sql = "insert into jvtc_data(name,url,hits) VALUES ('" + name + "','" + url + "','" + hits + "')"
        self.conn.query(sql)
        self.conn.commit()

        return item


def close_spider(self, spider):
    self.conn.close()
