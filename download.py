#!/usr/bin/python3

import os, requests
import urllib.parse
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


rootUrl = 'http://tuhh.fileserv.eu/thanks/'
cookie = 'd8e0b842ea18876511e49e4ac8ae74b8'


def toText(text):
	# remove url encoding
	return urllib.parse.unquote(text)
	

def getFile(session, path, url):
	# download file with a given url to a given path
	try:
		r = session.get(rootUrl + url)
		filename = path + toText(url)
		open(filename, 'wb').write(r.content)
	except IOError:
		print('Error: Could not write file.')
	except:
		print('Error: Could not access server. Please create a new cookie.')


def downloadFiles(session, path, url):
	# parse html
	r = session.get(rootUrl + url)
	soup = BeautifulSoup(r.text, "html.parser")

	# create directory
	dirname = path + toText(url[5:])
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
	for link in soup.find_all('a', {"class" : "item dir"}):
		downloadFiles(session, path, link.get('href'))


def main():
	# prepare session with authenication cookie
	cookiejar = requests.cookies.cookiejar_from_dict({'fileserv2012' : cookie})
	session = requests.Session()
	session.cookies = cookiejar
	
	# download all files
	downloadFiles(session, "files/", "")


main()
