#!/usr/bin/python3

import requests

cookie = 'd8e0b842ea18876511e49e4ac8ae74b8'


def getFile(session, url):
	try:
		r = session.get(url)
		substring1 = "/"
		filename = (url[url.rfind(substring1)+1:])
		open(filename, 'wb').write(r.content)
	except:
		print('Error: Could not access server. Please create a new cookie.')


def main():
	cookiejar = requests.cookies.cookiejar_from_dict({'fileserv2012' : cookie})
	session = requests.Session()
	session.cookies = cookiejar
	
	url='http://tuhh.fileserv.eu/thanks/Bachelor-MB-Pflichtmodule/Elektrische%20Maschinen/Klausuren/2008_09%20WS.pdf'
	getFile(session, url)


main()
