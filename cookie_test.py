import urllib2
import urllib
import cookielib

filename='my_cookie.txt'
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
post_data=urllib.urlencode(
{
	'zjh':'201292198',
	'mm':'178719'
}
)
#loginurl='http://zhjw.dlut.edu.cn/'
loginurl='http://zhjw.dlut.edu.cn/loginAction.do?'+post_data
gradeurl='gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4243'
result=opener.open(loginurl)
print result.read().decode('gbk')
result=opener.open(gradeurl)
print result.read().decode('gbk')
#cookie.save(ignore_discard=True,ignore_expires=True)
#gradeUrl='http://zhjw.dlut.edu.cn/loginAction.do'
#result=opener.open(gradeUrl)
#print result.read()
