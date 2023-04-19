# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy.utils.project import get_project_settings
class VideosPipeline:
    def open_spider(self,spider):
        settings = get_project_settings()
        self.host = settings["DB_HOST"]
        self.user = settings["DB_USER"]
        self.password = settings["DB_PASSWORD"]
        self.name = settings["DB_NAME"]
        self.connect()
    #   连接数据库
    def connect(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.name
        )
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        sql = f'insert into anime (id,name,src,url,page_url) values({item.get("page_id")},"{item.get("name")}","{item.get("src")}","{item.get("url")}","{item.get("page_url")}")'
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()