#! /usr/bin/env python
#coding=utf-8
import urllib2
import urllib
import re

class TbMMSpider:
	def __init__(self):
		user_agent='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
		self.siteURL='http://mm.taobao.com/json/request_top_list.htm'
		self.baseImgName='MM'
		self.headers={'User-Agent':user_agent}
	def getPage(self,pageIndex):
		url=self.siteURL+'?page='+str(pageIndex)
		print url
		request=urllib2.Request(url)
		response=urllib2.urlopen(request)
		return response.read().decode('gbk')

	def getContents(self,pageIndex):
		pageCode=self.getPage(pageIndex)
		pattern=re.compile('.*?<div class="personal-info.*?<div class="pic s60".*?<img src="(.*?)".*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<em><strong>(.*?)</strong>.*?',re.S)
		items=re.findall(pattern,pageCode)
		flag=1
		for item in items:
			#print item[0],item[1],item[2],item[3]

			filename=self.baseImgName+"%3d" % flag
			self.saveImg(item[0],filename)
			flag+=1
	
	def saveImg(self,imageURL,filename):
		suffix=re.match('.*(\..*)$',imageURL).groups()[0]
		print '图片后缀为：',suffix
		imageURL=re.sub('^\/\/','',imageURL)
		print imageURL
		u=urllib2.urlopen(imageURL,headers=self.headers)
		img=u.read()
		with open(filename+suffix,'wb') as f:
			f.write(img)
spider=TbMMSpider()
spider.getContents(1)
