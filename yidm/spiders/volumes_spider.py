#-*- coding:utf-8 -*-
import scrapy,re,sys,json,codecs,logging,os
from yidm.items import VolumesItem


reload(sys)
sys.setdefaultencoding('utf8')
logger=logging.getLogger(__name__)



class Volumes(scrapy.Spider):
	name='volumes'
	custom_settings={
	'ITEM_PIPELINES':{
	'yidm.pipelines.JsonVolumesPipeline':10
	}}
	start_urls=[]
	filename=os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),'..'),'..'),'menu.json'))
	try:
		with codecs.open(filename,'r',encoding='utf-8') as f:
			menu=json.load(f)
			count=0
			i=1
			while count<len(menu):
				try:
					if menu[str(i)] is not None:
						url=menu[str(i)]['index_url'][0]
						if url is not None:
							start_urls.append(url)
						else:
							book_name=menu[str(i)]['book_name']
							print "bookid "+str(i)+" "+book_name.encode('utf-8')+" ———— 受到了版权限制"
					count+=1
				except:
					print "bookid "+str(i)+" not exist!"
				finally:
					i+=1
	except:
		print "file menu.json not exist!"


	def parse(self,response):
		volumes_list=response.xpath('//div[@class="volumes_list"]')[0]
		volumes=volumes_list.xpath('count(//div[@class="volume"])').extract_first()
		volumes=int(re.findall(r'(\d+)?\.',str(volumes))[0])
		book_list=[]
		i=0
		for i in range(volumes):

			volume_title=volumes_list.xpath('//div[@class="vname"]/text()')[i].extract()

			lis=[("volume_title",volume_title),]
			xpathstr='count(//div[@class="volume"]'+str([i+1])+'/div[@class="chapters clearfix"]/a)'
			chapters=volumes_list.xpath(xpathstr)
			chapters=int(re.findall(r'(\d+)?\.',str(chapters))[0])
			j=0
			for j in range(chapters):
				
				chapter_title=volumes_list.xpath('//div[@class="volume"]'+str([i+1])+'/div[@class="chapters clearfix"]/a/text()')[j].extract()
				content_url=volumes_list.xpath('//div[@class="volume"]'+str([i+1])+'/div[@class="chapters clearfix"]/a/@href')[j].extract()
				part_value={'chapter_title':chapter_title,'content_url':[content_url]}
				lis.append(("part"+str(j+1),part_value))
			myvolume_value=dict(lis)
			myvolume="myvolume"+str(i+1)
			book_list.append((myvolume,myvolume_value))
		item=VolumesItem()
		item['index_url']=[response.url]
		item['volumes']=dict(book_list)
		yield item