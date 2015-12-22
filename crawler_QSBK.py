#! /usr/bin/env python
#coding=utf-8

import urllib
import urllib2
import re
import time
class QSBK:
	def __init__(self):
		self.pageIndex=1
		user_agent='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
		self.pattern=re.compile('<div.*?author clearfix">.*?<a.*?<img.*?<h2>(.*?)</h2>.*?'+'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)

		self.headers={'User-Agent':user_agent}
		self.stories=[]
		self.enable=False
	
	def getPage(self,pageIndex):
		
		try:
			url='http://www.qiushibaike.com/hot/page/'+str(pageIndex)
			#建立request对象
			request=urllib2.Request(url,headers=self.headers)
			#利用urlopen获取页面代码
			response=urllib2.urlopen(request)
			#将页面代码转换为utf-8编码读出	
			pageCode=response.read().decode('utf-8')
			return pageCode

		except urllib2.URLError,e:
			if hasattr(e,"code"):
				print u'连接出现问题',e.code
			if hasattr(e,"reason"):
				print u'连接糗事百科失败，错误原因',e.reason
			return None
	
	def getPageItems(self,pageIndex):
		pageCode=self.getPage(pageIndex)
		if not pageCode:
			print '页面加载失败....'
			return None
		
		items=re.findall(self.pattern,pageCode)
		#用来存储每页的段子
		pageStories=[]
		#遍历所有的匹配信息
		for item in items:
			if not re.search('img',item[3]):
				#替换段子内容中的<br/>,可以预先编译匹配模式
				replaceBR=re.compile('<br/>')
				content=re.sub(replaceBR,"\n",item[1].strip())
				pageStories.append([item[0].strip(),content,time.ctime(float(item[2])),item[4].strip()])
		
		return pageStories

	def loadPage(self):
		if self.enable:
			if len(self.stories)<2:
				#获取新一页
				pageStories=self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex+=1

	def getOneStory(self,pageStories,page):
		#遍历一页中的段子
		for story in pageStories:
			input=raw_input()
			if (input=='Q' or input=='q'):
				self.enable=False
				return
			print u'第%d页\t发布人：%s\t发布时间：%s\t赞：%s\n%s' % (page,story[0],story[2],story[3],story[1])

	def start(self):
		print '正在读取糗事百科，按回车查看新段子，Q（q）退出'
		self.enable=True

		nowPage=0
		
		while self.enable:
			#先加载一页的内容
			print '加载中...'
			self.loadPage()
			if len(self.stories)>0:
				pageStories=self.stories[0]
				nowPage+=1
				del self.stories[0]
				self.getOneStory(pageStories,nowPage)
spider=QSBK()
spider.start()
