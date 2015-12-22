#! /usr/bin/env python
#coding=utf-8

import urllib
import urllib2
import re
import time
page=1
url='http://www.qiushibaike.com/hot/page/'+str(page)
user_agent='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
pattern=re.compile('<div.*?author clearfix">.*?<a.*?<img.*?<h2>(.*?)</h2>.*?'+
	'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)

headers={'User-Agent':user_agent}
try:
	request=urllib2.Request(url,headers=headers)
	response=urllib2.urlopen(request)
	content=response.read().decode('utf-8')
	items=re.findall(pattern,content)
	i=1
	for item in items:
		print '第',i,'个笑话：'
		#haveImg=re.search('img',item[3])
		print '作者：',item[0]
		
		print '内容：\n',re.sub('<br/>','\n',item[1].strip()),'\n'
		print '发布时间：',time.ctime(float(item[2]))
		print '赞数：',item[4],'\n'
		i+=1

except urllib2.URLError,e:
	if hasattr(e,"code"):
		print e.code
	if hasattr(e,"reason"):
		print e.reason

