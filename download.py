#!/usr/bin/python3

import os, requests
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


rootUrl = 'http://tuhh.fileserv.eu/thanks/'
cookie = 'd8e0b842ea18876511e49e4ac8ae74b8'


def getFile(session, path, url):
	try:
		r = session.get(rootUrl + url)
		filename = path + url
		open(filename, 'wb').write(r.content)
	except IOError:
		print('Error: Could not write file ' + filename)
	except:
		print('Error: Could not access server. Please create a new cookie.')


def downloadFiles(session, path, url):
	# parse html
	r = session.get(rootUrl + url)
	soup = BeautifulSoup(r.text, "html.parser")

	# create directory
	dirname = path + url[5:]
	if not os.path.exists(dirname):
		try:
			os.makedirs(dirname)
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	
	# download files in current directory
	for link in soup.find_all('a', {"class":"item file"}):
		getFile(session, path, link.get('href'))
	
	# search through subdirectories recursively
	for l in soup.find_all('a', {"class" : "item dir"}):
		link = l.get('href')
		downloadFiles(session, path, link)


def main():
	# prepare session with authenication cookie
	cookiejar = requests.cookies.cookiejar_from_dict({'fileserv2012' : cookie})
	session = requests.Session()
	session.cookies = cookiejar
	
	# download all files
	downloadFiles(session, "files/", "")


main()
