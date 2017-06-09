#-*- coding:utf-8 -*-
import os,codecs,json,re,hashlib,time,gc,zipfile

'''
请确保在windows下运行
'''



def delete_and(mystr):
	try:
		if re.findall(r'.+(&).+',mystr)[0] is not None:
			mystr=re.sub('&','&amp;',mystr)
	except:
		pass
	finally:
		return mystr

def md5(string):
	m=hashlib.md5(string.encode('utf-8'))
	return m.hexdigest()



lib=os.path.join(os.path.dirname(__file__),'lib')
bookdir=os.path.join(os.path.dirname(__file__),'books')
if not os.path.exists(bookdir):
	os.mkdir(bookdir)


src_dir=os.path.join(os.path.dirname(__file__),'src')
with codecs.open(os.path.join(src_dir,'volumes.json'),'r',encoding='utf-8')as src_volumes:
	volumes=json.loads(delete_and(src_volumes.read()))

bookid=1
while bookid<=2202:
	# 可解除注释间断操作
	# if bookid<=400:
	try:
		if volumes[str(bookid)] is not None:
			with codecs.open(os.path.join(src_dir,'menu.json'),'r',encoding='utf-8')as src_menu:
				menu=json.loads(delete_and(src_menu.read()))

			book_name=menu[str(bookid)]['book_name']
			bookname=os.path.join(bookdir,book_name)
			#建立书本文件夹
			if not os.path.exists(bookname):
				os.mkdir(bookname)
				author=menu[str(bookid)]['author']
				painter=menu[str(bookid)]['painter']
				wenku=menu[str(bookid)]['wenku']
				desc=menu[str(bookid)]['desc']
				image_path=re.sub(r'/',r'\\',menu[str(bookid)]['image_path'][0])
				image=re.findall(r'\w+\\\w+\\(.+)',image_path)[0]
				# imagetype=re.findall(r'\.(\w+)',image_path)[0]
				image_path=os.path.join(src_dir,image_path)
				keep=1
				print('create book %d start...' % bookid)
				break
			else:
				keep=0
				bookid+=1
	except:
		bookid+=1
	# else:
	# 	keep=-1
	# 	os.system('cls')
	# 	print('create work 1-400 over.')
	# 	break











#用keep判断后续是否继续执行
if keep==1:
	#创建核心文件夹
	oebps=os.path.join(bookname,'OEBPS')
	os.mkdir(oebps)
	os.mkdir(os.path.join(oebps,'Images'))
	os.mkdir(os.path.join(oebps,'Styles'))
	os.mkdir(os.path.join(oebps,'Text'))
	
	#创建mimetype
	with codecs.open(os.path.join(bookname,'mimetype'),'w',encoding='utf-8')as mimetype:
		mimetype.write('application/epub+zip')

	#创建MeTA-INF和里面的container.xml
	os.mkdir(os.path.join(bookname,'META-INF'))
	with open(os.path.join(os.path.join(bookname,'META-INF'),'container.xml'),'wb')as f_container:
		with open(os.path.join(lib,'container.xml'),'rb')as lib_container:
			f_container.write(lib_container.read())

	#创建css文件
	with open(os.path.join(os.path.join(oebps,'Styles'),'style.css'),'wb')as f_css:
		with open(os.path.join(lib,'style.css'),'rb')as lib_css:
			f_css.write(lib_css.read())



	#把封面图移动到book里，并修改名称
	imagedir=os.path.join(oebps,'Images')
	os.system('copy "%s" "%s"'%(image_path,imagedir))
	os.rename(os.path.join(imagedir,image),os.path.join(imagedir,'cover.jpg'))


	#记录除目录TOC.xhtml外所有xhtml的数目，并以此生成xhtml文件
	xhtml_page_num=0

	#记录卷数并生成目录TOC.xhtml
	volume_count=len(volumes[str(bookid)]['volumes'])
	textdir=os.path.join(oebps,'Text')
	with codecs.open(os.path.join(textdir,'TOC.xhtml'),'w',encoding='utf-8')as text_toc:
		with codecs.open(os.path.join(lib,'text_head.xhtml'),'r',encoding='utf-8')as lib_text_head:
			#写入头部
			#text_head是通用head文本
			text_head=lib_text_head.read()
			text_toc.write(text_head+'\n<div class="ttoc">\n<h2 title="目录">目  录</h2>\n<div>\n')
		volume_i=0
		for volume_i in range(volume_count):
			text_toc.write('\n<div><p>\n')
			myvolume_name='myvolume%d' % (volume_i+1)
			myvolume_content=volumes[str(bookid)]['volumes'][myvolume_name]
			#卷标题,使用第一章的url
			volume_title=myvolume_content['volume_title']
			part_j=0
			for part_j in range(len(myvolume_content)-1):
				xhtml_page_num+=1
				if part_j==0:
					volume_str='<a href="%d.xhtml">%s</a>'% (xhtml_page_num,volume_title)
					text_toc.write(volume_str+'\n')
				part_name='part%d' % (part_j+1)
				chapter_title=myvolume_content[part_name]['chapter_title']
				chapter_str='<blockquote><a href="%d.xhtml">%s</a></blockquote>'% (xhtml_page_num,chapter_title)
				text_toc.write(chapter_str+'\n')
			text_toc.write('</p></div>\n\n')
		text_toc.write('</div>\n</div>\n</body>\n</html>')
		del text_toc,lib_text_head,lib_container,lib_css
		gc.collect()




	#生成唯一书籍标识
	uid=md5(book_name+str(time.time()))
	uid_1=uid[0:8]
	uid_2=uid[8:12]
	uid_3=uid[12:16]
	uid_4=uid[16:20]
	uid_5=uid[20:32]
	uid='%s-%s-%s-%s-%s'% (uid_1,uid_2,uid_3,uid_4,uid_5)

	#生成toc.ncx文件
	with codecs.open(os.path.join(oebps,'toc.ncx'),'w',encoding='utf-8')as ncx_toc:
		ncx_head='<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" \n"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n<head>\n<meta content="%s" name="dtb:uid"/>\n<meta content="2" name="dtb:depth"/>\n<meta content="0" name="dtb:totalPageCount"/>\n<meta content="0" name="dtb:maxPageNumber"/>\n</head>\n<docTitle>\n<text>%s</text>\n</docTitle>\n'% (uid,book_name)
		ncx_toc.write(ncx_head)
		nav_id=1
		#添加封面和简介
		ncx_summary='<navMap>\n<navPoint id="navPoint-%d" playOrder="%d">\n<navLabel>\n<text>封面</text>\n</navLabel>\n<content src="Text/cover.xhtml"/>\n</navPoint>\n<navPoint id="navPoint-%d" playOrder="%d">\n<navLabel>\n<text>简介</text>\n</navLabel>\n<content src="Text/summary.xhtml"/>\n</navPoint>\n' % (nav_id,nav_id,nav_id+1,nav_id+1)
		ncx_toc.write(ncx_summary)
		nav_id+=2
		ncx_menu='<navPoint id="navPoint-%d" playOrder="%d">\n<navLabel>\n<text>目录</text>\n</navLabel>\n<content src="Text/TOC.xhtml"/>\n</navPoint>\n' % (nav_id,nav_id)
		ncx_toc.write(ncx_menu)
		xhtml_page_num=0
		volume_i=0
		for volume_i in range(volume_count):
			myvolume_name='myvolume%d' % (volume_i+1)
			myvolume_content=volumes[str(bookid)]['volumes'][myvolume_name]
			#卷标题,使用第一章的url
			volume_title=myvolume_content['volume_title']
			part_j=0
			for part_j in range(len(myvolume_content)-1):
				xhtml_page_num+=1
				nav_id+=1
				if part_j==0:
					volume_str='<navPoint id="navPoint-%d" playOrder="%d">\n<navLabel>\n<text>%s</text>\n</navLabel>\n<content src="Text/%d.xhtml"/>\n</navPoint>\n'% (nav_id,nav_id,volume_title,xhtml_page_num)
					ncx_toc.write(volume_str)
					nav_id+=1
				part_name='part%d' % (part_j+1)
				chapter_title=myvolume_content[part_name]['chapter_title']
				chapter_str='<navPoint id="navPoint-%d" playOrder="%d">\n<navLabel>\n<text>%s</text>\n</navLabel>\n<content src="Text/%d.xhtml"/>\n</navPoint>\n'% (nav_id,nav_id,chapter_title,xhtml_page_num)
				ncx_toc.write(chapter_str)
		ncx_toc.write('</navMap>\n</ncx>')






	#将插画移动到相应的文件夹下，并制作插画对应的contentid列表
	with codecs.open(os.path.join(src_dir,'inbetweening.json'),'r',encoding='utf-8')as src_bet:
		bet=json.loads(delete_and(src_bet.read()))
	pic_i=0
	#制作插画对应的contentid列表，后面要用来插画到页面
	contentid_list=[]
	try:
		for pic_i in range(len(bet[str(bookid)])):
			#获取插画路径
			picture_path=bet[str(bookid)][str(pic_i+1)]['picture_path'][0]
			picture_path=re.sub(r'/',r'\\',picture_path)
			picture_path=os.path.join(src_dir,picture_path)
			#将插画移动到相应的文件夹下
			os.system('copy "%s" "%s"'%(picture_path,imagedir))
			#制作插画对应的contentid列表，后面要用来插画到页面
			pic_contentid=bet[str(bookid)][str(pic_i+1)]['contentid']
			contentid_list.append(pic_contentid)
			have_inbetweening=1
	except:
		print('not any inbetweening')
		have_inbetweening=0





	

	#生成content.opf
	with codecs.open(os.path.join(oebps,'content.opf'),'w',encoding='utf-8')as opf:
		opf_head='<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">\n<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n<dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:%s</dc:identifier>\n<dc:title>%s</dc:title>\n<dc:creator opf:role="aut">%s</dc:creator>\n<dc:language>zh-CN</dc:language>\n<meta name="cover" content="cover.jpg" />\n</metadata>\n'%(uid,book_name,author)
		opf.write(opf_head)
		#开始写入manifest
		#先写入toc.ncx,css,cover,summary,TOC.xhtml
		opf_manifest_1='<manifest>\n<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml" />\n<item href="Styles/style.css" id="style.css" media-type="text/css" />\n<item href="Text/cover.xhtml" id="cover.xhtml" media-type="application/xhtml+xml" />\n<item href="Text/summary.xhtml" id="summary.xhtml" media-type="application/xhtml+xml" />\n<item href="Text/TOC.xhtml" id="TOC.xhtml" media-type="application/xhtml+xml" />\n'
		opf.write(opf_manifest_1)

		#写入所有文本页面
		opf_i=0
		for opf_i in range(xhtml_page_num):
			opf_manifest_2='<item href="Text/%d.xhtml" id="%d.xhtml" media-type="application/xhtml+xml" />\n'%(opf_i+1,opf_i+1)
			opf.write(opf_manifest_2)

		#单独写入封面图
		opf.write('<item href="Images/cover.jpg" id="cover.jpg" media-type="image/jpeg" />\n')
		#若存在则写入插画
		if have_inbetweening==1:
			opf_j=0
			for opf_j in range(len(bet[str(bookid)])):
				picture_path=bet[str(bookid)][str(opf_j+1)]['picture_path'][0]
				picture=re.findall(r'images/inbetweenings/(.+)',picture_path)[0]
				opf_manifest_3='<item href="Images/%s" id="%s" media-type="image/jpeg" />\n'%(picture,picture)
				opf.write(opf_manifest_3)
		#manifest结束，并开始写spine
		opf.write('</manifest>\n<spine toc="ncx">\n<itemref idref="cover.xhtml" />\n<itemref idref="summary.xhtml" />\n<itemref idref="TOC.xhtml" />\n')
		opf_i=0
		for opf_i in range(xhtml_page_num):
			opf.write('<itemref idref="%s.xhtml" />\n'% str(opf_i+1))
		#spine结束，写guide并结束opf
		opf.write('</spine>\n<guide>\n<reference href="Text/cover.xhtml" title="封面" type="cover" />\n<reference href="Text/TOC.xhtml" title="目录" type="toc" />\n</guide>\n</package>')


	#生成cover.xhtml
	with codecs.open(os.path.join(textdir,'cover.xhtml'),'w',encoding='utf-8')as cover_f:
		cover_f.write(text_head+'\n<div><br/></div>\n<div><img src="../Images/cover.jpg" /></div></body></html>')

	#生成summary.xhtml
	with codecs.open(os.path.join(textdir,'summary.xhtml'),'w',encoding='utf-8')as summary:
		summary.write(text_head+'\n<div>\n<h1>%s</h1>\n<h2>文库：%s</h2>\n<h2>作者：%s</h2>\n<h2>插画：%s</h2>\n<h2>简介：</h2>\n<p>%s</p></div></body></html>'%(book_name,wenku,author,painter,desc))





	#生成内容文件
	xhtml_i=0
	with codecs.open(os.path.join(os.path.join(src_dir,'novels'),str(bookid)+'.json'),'r',encoding='utf-8')as novel_src:
		novel=json.loads(novel_src.read())
	while xhtml_i<xhtml_page_num:
		volume_i=0
		for volume_i in range(volume_count):
			myvolume_name='myvolume%d' % (volume_i+1)
			myvolume_content=volumes[str(bookid)]['volumes'][myvolume_name]
			part_j=0
			for part_j in range(len(myvolume_content)-1):
				part_name='part%d' % (part_j+1)
				content_url=myvolume_content[part_name]['content_url'][0]
				contentid=re.findall(r'/(\d+)?.html',content_url)[0]
				chapter=novel[contentid]['content']
				chapter=chapter.replace('\n\t\t','<h4>',1)
				chapter=chapter.replace('\n\t\t','</h4>\n')
				chapter=chapter.replace('\r\n\r\n','<br/>\n')
				chapter=chapter.replace('\n','<br/>\n')
				chapter=chapter.replace('\t','<br/>\n')
				chapter=re.sub(r'\s+','',chapter)

				#此书存在插画
				if have_inbetweening==1:
					if contentid in contentid_list:
						content=text_head+'\n<p>%s'%chapter
						pic_i=0
						for pic_i in range(len(bet[str(bookid)])):
							pic_contentid=bet[str(bookid)][str(pic_i+1)]['contentid']
							if pic_contentid==contentid:
								picture_path=bet[str(bookid)][str(pic_i+1)]['picture_path'][0]
								picture=re.findall(r'images/inbetweenings/(.+)',picture_path)[0]
								content+='<img src="../Images/%s" /><br/>\n'% picture
						content+='</p>\n</body>\n</html>'
						with codecs.open(os.path.join(textdir,str(xhtml_i+1)+'.xhtml'),'w',encoding='utf-8')as content_page:
							content_page.write(content)
					#此书存在插画但此页面没有插画
					else:
						content=text_head+'\n<p class="ttoc">%s</p>\n</body>\n</html>'% chapter
						with codecs.open(os.path.join(textdir,str(xhtml_i+1)+'.xhtml'),'w',encoding='utf-8')as content_page:
							content_page.write(content)
				#此书没有插画
				else:
					content=text_head+'\n<p class="ttoc">%s</p>\n</body>\n</html>'% chapter
					with codecs.open(os.path.join(textdir,str(xhtml_i+1)+'.xhtml'),'w',encoding='utf-8')as content_page:
						content_page.write(content)
				xhtml_i+=1




#压缩函数，使用时调用zip_path
def dfs_get_zip_file(input_path,result):
	if os.path.isdir(input_path):
		files = os.listdir(input_path)
		for file in files:
			if os.path.isdir(os.path.join(input_path,file)):
				dfs_get_zip_file(os.path.join(input_path,file),result)
			else:
				result.append(os.path.join(input_path,file))
	else:
		result.append(input_path)


def zip_path(input_path,output_path,output_name):
	if os.path.exists(os.path.join(output_path,output_name)):
		f = zipfile.ZipFile(os.path.join(output_path,output_name),'a',zipfile.ZIP_DEFLATED)
	else:
		f = zipfile.ZipFile(os.path.join(output_path,output_name),'w',zipfile.ZIP_DEFLATED)
	filelists = []
	dfs_get_zip_file(input_path,filelists)
	for file in filelists:
		f.write(file)
	f.close()
	return os.path.join(output_path,output_name)



if keep==1:
	#进入该书目录下，压缩制作成epub
	os.chdir(bookname)
	epubname=book_name+'.epub'
	zip_path('META-INF','.',epubname)
	zip_path('OEBPS','.',epubname)
	zip_path('mimetype','.',epubname)
	os.chdir(os.path.join(os.path.join('.','..'),'..'))
	epubdir=os.path.join(os.path.dirname(__file__),'epubs')
	if not os.path.exists(epubdir):
		os.mkdir(epubdir)
	os.system('move "%s" "%s"'%(os.path.join(bookname,epubname),epubdir))
	os.system('cls')
	print('create book %d finished.'% bookid)



elif keep==0:
	os.system('cls')
	print("create all books finished.")

