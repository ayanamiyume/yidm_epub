# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YidmItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	pass



class MenuItem(YidmItem):
	book_url=scrapy.Field()
	image_urls=scrapy.Field()
	image_path=scrapy.Field()
	book_name=scrapy.Field()
	wenku=scrapy.Field()
	author=scrapy.Field()
	painter=scrapy.Field()
	click=scrapy.Field()
	collect=scrapy.Field()
	all_vote=scrapy.Field()
	lastchapter=scrapy.Field()
	lastuptime=scrapy.Field()
	desc=scrapy.Field()
	index_url=scrapy.Field()



class VolumesItem(YidmItem):
	index_url=scrapy.Field()
	volumes=scrapy.Field()


class ContentsItem(YidmItem):
	bookid=scrapy.Field()
	contents=scrapy.Field()


class ContentsNovItem(YidmItem):
	bookid=scrapy.Field()
	contenturl=scrapy.Field()
	content=scrapy.Field()
	contentid=scrapy.Field()


class ContentsPicItem(YidmItem):
	bookid=scrapy.Field()
	pictureid=scrapy.Field()
	contentid=scrapy.Field()
	picture_path=scrapy.Field()
	picture_url=scrapy.Field()




	