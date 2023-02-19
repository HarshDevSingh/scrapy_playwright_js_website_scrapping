# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3


class QuoteshtmlPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('quotes.db')
        self.conn.execute('''CREATE TABLE quotes
                     (author TEXT, quote TEXT)''')
        self.conn.commit()

    def process_item(self, item, spider):
        self.conn.execute("""
                    INSERT INTO quotes (author, quote) VALUES (?, ?)
                """,
                          (item['author'], item['quote']))
        self.conn.commit()
        return item
