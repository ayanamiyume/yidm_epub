#-*- coding:utf-8 -*-
import scrapy,re,sys,json,codecs,logging,os,gc
from yidm.items import ContentsPicItem,ContentsNovItem


reload(sys)
sys.setdefaultencoding('utf8')


class Contents(scrapy.Spider):
	name='contents'
	custom_settings={
	'ITEM_PIPELINES':{
	'yidm.pipelines.ContentsPicPipeline':15,
	'yidm.pipelines.JsonContentsPicPipeline':17,
	'yidm.pipelines.JsonContentsPipeline':20,
	}}
	bookid=1
	count=0
	filename=os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__),'..'),'..'),'volumes.json'))
	start_urls=[]
	try:
		with codecs.open(filename,'r',encoding='utf-8')as f:
			volumes=json.load(f)
			while count<len(volumes):
				try:
					if volumes[str(bookid)] is not None:
						count+=1
						j=0
						for j in range(len(volumes[str(bookid)]['volumes'])):
							myvolume='myvolume'+str(j+1)
							k=0
							for k in range(len(volumes[str(bookid)]['volumes'][myvolume])-1):
								part='part'+str(k+1)
								url=volumes[str(bookid)]['volumes'][myvolume][part]['content_url'][0]
								start_urls.append(url)
						bookid+=1
				except:
					print "bookid "+str(bookid)+" not exist!"
					bookid+=1
	except:
		print "file volumes.json not exist!"




	def parse(self,response):
		bd=response.xpath('//div[@class="bd"]')[0]
		try:
			if bd.xpath('count(//a[@class="lightbox"])')[0] is not None:
				pictures=bd.xpath('//a[@class="lightbox"]/@href')
				pic_count=int(re.findall(r'(\d+)?\.',str(bd.xpath('count(//a[@class="lightbox"])')[0]))[0])
				i=0
				for i in range(pic_count):
					pic_item=ContentsPicItem()
					pic_item['picture_url']=[str(pictures[i].extract())]
					yield pic_item
					del pic_item
					gc.collect()
		except:
			print 'no picture in '+str(response.url)

		nov_item=ContentsNovItem()
		nov_item['content']=str(bd.xpath('string(.)').extract_first())
		nov_item['contenturl']=[response.url]
		nov_item['contentid']=re.findall(r'(\d+)?\.html',response.url)[0]
		nov_item['bookid']=re.findall(r'(\d+)?/\d+\.html',response.url)[0]
		yield nov_item
		del nov_item
		gc.collect()
