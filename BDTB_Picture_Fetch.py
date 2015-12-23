
#coding=utf-8
import urllib2
import urllib
import re

class TBShenQi:
	def __init__(self):
		self.baseURL='http://tieba.baidu.com/photo/g'
		self.tbName=None
		self.fileName=None
		self.savePath=None
		self.defaultPath='~/Documents/pictures/'
		self.catalogPattern=re.compile('.*?<li class="catalog_li.*?href="(.*?)".*?<span class="catalog_a_inner">(.*?)<.*?',re.S)
		self.catalogInfo={}
		self.albumsPattern=re.compile('.*?<div class="grbm_ele_title.*?href="(.*?)".*?>(.*?)</a>.*?',re.S)
		self.albumsNumPattern=re.compile('.*?<span class="grbh_left_amount">(.*?)</span>.*?',re.S)
		self.totalAlbumsNum=None
		self.currentPage=1
		self.albumInfo={}

	def getPage(self,url):
		if url is None:
			print '请输入url地址'
			return None
		try:
			request=urllib2.Request(url)
			response=urllib2.urlopen(request)
			return response.read().decode('gbk')
	
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print "获取页面源码失败",e.reason
				return None
		finally:
			request=None
			response=None

	def enterTBAlbums(self,tbName=None):
		if tbName is None:
			print '请输入贴吧名字'
			return None
		self.tbName=tbName
		request=urllib2.Request(self.baseURL+'/?kw='+tbName+'&ie=utf-8')
		response=urllib2.urlopen(request)
		return response.read().decode('gbk')

	def getCatalog(self,pageCode):
		if pageCode is None:
			print '页面代码为空'
			return None
		#print pageCode
		items=re.findall(self.catalogPattern,pageCode)
		for item in items:
			#print type(item[0].encode('utf-8'))
			albumURL=self.baseURL+'/?kw='+self.tbName+'&ie=utf-8'+item[0].encode('utf-8')
			self.catalogInfo[item[1]]=albumURL
			print albumURL,item[1]
	
	def getAlbumsInfo(self,catalogURL):
		
		if catalogURL is None:
			print '请输入相册目录'
			return None

		homePage=self.getPage(catalogURL)
		self.totalAlbumsNum=re.search(self.albumsNumPattern,homePage).group(1)
		currentNum=0
		print self.totalAlbumsNum
		homePage=None

		#baseUrl='http://tieba.baidu.com'
		while int(currentNum) < int(self.totalAlbumsNum):

			print currentNum,self.totalAlbumsNum

			tmp=catalogURL+'#!/g/catidall/'+'p'+str(self.currentPage)
			print tmp
			pageCode=self.getPage(tmp)

			items=re.findall(self.albumsPattern,pageCode)
			for item in items:
				self.albumInfo[item[1]]=item[0]
				print item[0],item[1]
			currentNum+=len(items)
			items=[]
			self.currentPage+=1
			pageCode=None


tbTest=TBShenQi()
tbTest.getCatalog(tbTest.enterTBAlbums('刘涛'))
tbTest.getAlbumsInfo('http://tieba.baidu.com/photo/g?kw=%E5%88%98%E4%BA%A6%E8%8F%B2&cat_id=all')
