#-*- coding:utf-8 -*-
import scrapy,re,sys
from yidm.items import MenuItem

reload(sys)
sys.setdefaultencoding('utf8')


class Menu(scrapy.Spider):
	name='menu'
	custom_settings={
	'ITEM_PIPELINES':{'yidm.pipelines.JsonMenuPipeline':5,
	'yidm.pipelines.BookPicPipeline':2,
	}}
	start_urls=[]
	i=0
	url_count=2202
	for i in range(url_count):
		start_urls.append("http://www.yidm.com/article/info/0/"+str(i+1)+".html")

	def parse(self,response):
		title=response.css('title').extract_first().encode('utf-8')
		if(title=='<title>出现错误！ - 迷糊动漫</title>'):
			print title
		else:
			bd=response.xpath('//div[@class="wrap"]/div[1]/div[1]/div[1]/div[@class="bd clearfix"]')[0]
			
			image_urls=bd.xpath('//div[@class="ml"]//img[1]/@src').extract_first()
			book_name=bd.xpath('//div[@class="tit"]/h2/text()').extract_first()
			wenku=bd.xpath('//div[@class="tit"]/h4[1]/text()').extract_first()
			author=bd.xpath('//div[@class="tit"]/h4[2]/a/text()').extract_first()
			painter=bd.xpath('//div[@class="tit"]/h4[3]/a/text()').extract_first()
			click=int(re.findall(r'(\d+)',bd.xpath('//div[@class="hot_data"]/span[1]/text()').extract_first())[0])
			collect=int(re.findall(r'(\d+)',bd.xpath('//div[@class="hot_data"]/span[2]/text()').extract_first())[0])
			all_vote=int(bd.xpath('//div[@class="hot_data"]/span[3]/em/text()').extract_first())
			lastchapter=bd.xpath('//div[@class="lastchapter"]/a/text()').extract_first()
			try:
				if re.findall(r'(&nbsp;)?',lastchapter)[0] is not None:
					lastchapter=re.sub('&nbsp;',r' ',lastchapter)
			except:
				pass
			lastuptime=bd.xpath('//div[@class="lastchapter"]/span/text()').extract_first()
			desc=bd.xpath('//div[@id="desc"]/text()').extract_first()
			index_url=bd.xpath('//div[@class="btns"]/a[1]/@href').extract_first()

			item=MenuItem()
			item['book_url']=[response.url]
			item['image_urls']=[image_urls]
			item['book_name']=book_name
			item['wenku']=wenku
			item['author']=author
			item['painter']=painter
			item['click']=click
			item['collect']=collect
			item['all_vote']=all_vote
			item['lastchapter']=lastchapter
			item['lastuptime']=lastuptime
			item['desc']=desc
			item['index_url']=[index_url]
			yield item
