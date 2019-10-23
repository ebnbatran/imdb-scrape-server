# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import psycopg2 as pg

DATABASE_URL = os.environ['DATABASE_URL']

class ScrapeImdbPipeline(object):
	table_name = 'server_movie'

	def __init__(self, database):
		self.database = database

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			database=crawler.settings.get(DATABASE_URL)
		)

	def open_spider(self, spider):
		self.connection = pg.connect(DATABASE_URL)
		self.connection.autocommit = True
		self.cursor = self.connection.cursor()

	def close_spider(self, spider):
		self.cursor.close()
		self.connection.close()

	def rap(self, value):
		if value is None:
			return 'NONE'

		value = str(value).strip()

		if "'" in value:
			value = value.replace("'", "_")
		elif '"' in value:
			value = value.replace('"', '*')

		return value

	def process_item(self, item, spider):
		item_dict = dict(item)

		for key in item_dict:
			item_dict[key] = self.rap(item_dict[key])

		sql = f'INSERT INTO {self.table_name} '
		sql += '(title, url, year, rating, synopsis, image) '
		sql += 'VALUES ('
		sql += f"'{item_dict['title']}', "
		sql += f"'{item_dict['url']}', "
		sql += f"'{item_dict['year']}', "
		sql += f"'{item_dict['rating']}', "
		sql += f"'{item_dict['synopsis']}', "
		sql += f"'{item_dict['image']}'"
		sql += ');'

		self.cursor.execute(sql)

		return item
