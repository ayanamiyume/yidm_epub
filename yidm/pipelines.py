# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import json,codecs,scrapy,re,gc,os
from yidm.items import ContentsPicItem,ContentsNovItem


class YidmPipeline(object):
	def process_item(self, item, spider):
		return item



class BookPicPipeline(ImagesPipeline):
	def get_media_requests(self,item,info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self,results,item,info):
		image_paths=[x['path'] for ok,x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no images "+str(image_paths))
		item['image_path']=["images/bookimgs/"+re.findall(r'full/(.+)',image_paths[0])[0]]
		return item

	def close_spider(self,spider):
		olddirname=os.path.join(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),'..'),'images')),'full')
		newdirname=os.path.join(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),'..'),'images')),'bookimgs')
		os.rename(olddirname,newdirname)




class JsonMenuPipeline(object):
	def open_spider(self,spider):
		self.file=codecs.open('menu.json','w',encoding='utf-8')
		self.file.write('{\n')

	def close_spider(self,spider):
		self.file.write('}')
		self.file.close()
		with codecs.open('menu.json','r',encoding='utf-8') as f:
			s=re.sub('},\n}','}\n}',f.read())
		with codecs.open('menu.json','w',encoding='utf-8') as f:
			f.write(s)

		


	def process_item(self,item,spider):
		book_id=re.findall(r'(\d+)?\.html',item['book_url'][0])[0]
		line='"'+book_id+'":'+json.dumps(dict(item),ensure_ascii=False,indent=4)+',\n'
		self.file.write(line)
		return item



class JsonVolumesPipeline(object):
	def open_spider(self,spider):
		self.file=codecs.open('volumes.json','w',encoding='utf-8')
		self.file.write('{\n')

	def close_spider(self,spider):
		self.file.write('}')
		self.file.close()
		with codecs.open('volumes.json','r',encoding='utf-8') as f:
			s=re.sub('},\n}','}\n}',f.read())
		with codecs.open('volumes.json','w',encoding='utf-8') as f:
			f.write(s)


	def process_item(self,item,spider):
		book_id=re.findall(r'(\d+)?/index',item['index_url'][0])[0]
		line='"'+book_id+'":'+json.dumps(dict(item),ensure_ascii=False,indent=4)+',\n'
		self.file.write(line)
		return item



class ContentsPicPipeline(ImagesPipeline):
	def get_media_requests(self,item,info):
		if isinstance(item,ContentsPicItem):
			for image_url in item['picture_url']:
				yield scrapy.Request(image_url)
				del item
				gc.collect()

	def item_completed(self,results,item,info):
		if isinstance(item,ContentsPicItem):
			image_paths=[x['path'] for ok,x in results if ok]
			if not image_paths:
				raise DropItem("ContentsPicItem contains no picture "+str(image_paths))
			item['picture_path']=["images/inbetweenings/"+re.findall(r'full/(.+)',image_paths[0])[0]]
		return item

	def close_spider(self,spider):
		olddirname=os.path.join(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),'..'),'images')),'full')
		newdirname=os.path.join(os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__),'..'),'images')),'inbetweenings')
		os.rename(olddirname,newdirname)


class JsonContentsPicPipeline(object):
	def __init__(self):
		pass
		# self.picture_list=[]
		
	def open_spider(self,spider):
		self.file=codecs.open('inbetweening.json','w',encoding='utf-8')
		self.file.write('{\n')


	def close_spider(self,spider):
		self.file.write('}')
		self.file.close()
		with codecs.open('inbetweening.json','r',encoding='utf-8') as f:
			s=re.sub('},\n}','}\n}',f.read())
		with codecs.open('inbetweening.json','w',encoding='utf-8') as f:
			f.write(s)
		

		# self.file.write(json.dumps(dict(self.picture_list),ensure_ascii=False,indent=4))
		# self.file.close()
		# del self.picture_list
		# gc.collect()


	def process_item(self,item,spider):
		if isinstance(item,ContentsPicItem):
			item['bookid']=re.findall(r'(\d+)?/\d+/\d+\.\w+',item['picture_url'][0])[0]
			item['contentid']=re.findall(r'(\d+)?/\d+\.\w+',item['picture_url'][0])[0]
			item['pictureid']=re.findall(r'attachment/\d+/\d+/\d+/(\d+)?\.',item['picture_url'][0])[0]
			mypic={'picture_path':item['picture_path'],'picture_url':item['picture_url'],'pictureid':item['pictureid'],'contentid':item['contentid']}
			self.file.write('"'+item['bookid']+'":'+json.dumps(mypic,ensure_ascii=False,indent=4)+',\n')
			# self.picture_list.append((item['bookid'],mypic))
		return item


class JsonContentsPipeline(object):
	def __init__(self):
		self.dirname=os.path.join(os.path.join(os.path.dirname(__file__),'..'),'novels')
		if not os.path.exists(self.dirname):
			os.mkdir(self.dirname)


	def close_spider(self,spider):
		# get the maxbookid in menu.json
		with codecs.open(os.path.join(os.path.join(os.path.dirname(__file__),'..'),'menu.json'))as ff:
			menu=json.load(ff)
			maxbookid=1
			count=0
			i=1
			while count<len(menu):
				try:
					if menu[str(i)] is not None:
						if i>maxbookid:
							maxbookid=i
					count+=1
				except:
					pass
				finally:
					i+=1

		bookid=0
		for bookid in range(maxbookid):
			filename=os.path.join(self.dirname,os.path.join(str(bookid+1)+'.json'))
			if os.path.exists(filename):
				with codecs.open(filename,'a',encoding='utf-8')as f:
					f.write('\n}')


	def process_item(self,item,spider):
		if isinstance(item,ContentsNovItem):
			bookid=item['bookid']
			filename=os.path.join(self.dirname,os.path.join(bookid+'.json'))
			if not os.path.exists(filename):
				with codecs.open(filename,'w',encoding='utf-8')as f:
					f.write('{')
			with codecs.open(filename,'r',encoding='utf-8')as g:
				if g.read()=='{':
					add='\n'    
				else:
					add=',\n'
			with codecs.open(filename,'a',encoding='utf-8')as f:
				contents={'content':item['content'],'contenturl':item['contenturl']}
				f.write(add+'"'+item['contentid']+'":'+json.dumps(contents,ensure_ascii=False,indent=4))

		return item