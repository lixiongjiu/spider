#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import re


class Tool:
        #删除img标签和7位空格
        removeImg=re.compile('<img.*?>|\s{7}')
        #删除超链接
        removeAddr=re.compile('<a.*?>|</a>')
        #替换换行标签为\n
        replaceLine=re.compile('<tr>|<div>|</div>|</p>')
        #将制表<td>替换为\t
        replaceTD=re.compile('<td>')
        #把段落开头替换为\n加两个空格
        replacePara=re.compile('<p.*?>')
        #将换行符替换为\n
        replaceBR=re.compile('<br>|<br/>')
        #将其余标签删除
        removeOther=re.compile('<.*?>')

        def replace(self,target):
                target=re.sub(self.removeImg,"",target)
                target=re.sub(self.removeAddr,"",target)
                target=re.sub(self.replaceLine,"\n",target)
                target=re.sub(self.replaceTD,"\t",target)
                target=re.sub(self.replacePara,"\n\s[2]",target)
                target=re.sub(self.replaceBR,"\n",target)
                target=re.sub(self.removeOther,"",target)
                return target.strip()


class BDTB:
	#初始化，只传入基地址，和是否只看楼主的参数
	def __init__(self,baseUrl,see_lz):
		self.baseURL=baseUrl
		self.seeLZ='?see_lz='+str(see_lz)
		self.tool=Tool()
		self.file=None
		self.floor=1
		self.default_fileName=u'百度贴吧'
	def getPage(self,pageNum):
		try:
			url=self.baseURL+self.seeLZ+'&pn='+str(pageNum)
			request=urllib2.Request(url)
			response=urllib2.urlopen(request)
			#print response.read()
			return response.read()

		except urllib2.URLError,e:
			if hasattr(e,'reason'):
				print u'连接百度贴吧失败，错误原因',e.reason
				return None
	
	def getTitle(self):
		pageCode=self.getPage(1)
		pattern=re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
		result=re.search(pattern,pageCode)
		if result:
			return result.group(1).strip()
		else:
			return None
	
	def getPageNum(self):
		pageCode=self.getPage(1)
		pattern=re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result=re.search(pattern,pageCode)
		if result:
			return result.group(1).strip()
		else:
			return None


	def setFileName(self,name):
		if name is not None:
			self.file=open(name+'.txt',"w+")
		else:
			self.file=open(self.default_fileName+'.txt','w+')
		

	def write_data(self,data):
		try:
			self.file.write(data)
		except Exception:
			print 'write failed'
			
	def getContent(self,pageCode):
		pattern=re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items=re.findall(pattern,pageCode)
		#floor=1
		for item in items:
			self.write_data('\n\n------------------------第%s楼----------------------------\n' % self.floor)
			self.write_data(self.tool.replace(item))
			self.floor+=1
'''
class Tool:
	#删除img标签和7位空格
	removeImg=re.compile('<img.*?>|\s{7}')
	#删除超链接
	removeAddr=re.compile('<a.*?>|</a>')
	#替换换行标签为\n
	replaceLine=re.compile('<tr>|<div>|</div>|</p>')
	#将制表<td>替换为\t
	replaceTD=re.compile('<td>')
	#把段落开头替换为\n加两个空格
	replacePara=re.compile('<p.*?>')
	#将换行符替换为\n
	replaceBR=re.compile('<br>|<br/>')
	#将其余标签删除
	removeOther=re.compile('<.*?>')
	
	def replace(self,target):
		target=re.sub(removeImg,"",target)
		target=re.sub(removeAddr,"",target)
		target=re.sub(replaceLine,"\n",target)
		target=re.sub(replaceTD,"\t",target)
		target=re.sub(replacePara,"\n\s[2]",target)
		target=re.sub(replaceBR,"\n",target)
		target=re.sub(removeOther,"",target)
		return target.strip()
'''

baseURL='http://tieba.baidu.com/p/3138733512'
bdtb=BDTB(baseURL,1)
bdtb.setFileName('百度贴吧-NBA')
bdtb.getContent(bdtb.getPage(1))

