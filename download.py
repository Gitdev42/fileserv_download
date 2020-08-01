#!/usr/bin/python3

import os, requests
import urllib.parse
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# general settings
rootUrl = 'http://tuhh.fileserv.eu/thanks/'
filepath = "files/"

# to create a new cookie id, login to the site and copy
# the value of the cookie with the name 'fileserv2012'
# (can be found with Shift+F9 in Firefox)
cookie = 'd8e0b842ea18876511e49e4ac8ae74b8'



# remove url encoding
def toText(url):
	return urllib.parse.unquote(url)


# download file with a given url to a given path
def getFile(session, path, url):
	try:
		r = session.get(rootUrl + url)
		filename = path + toText(url)
		open(filename, 'wb').write(r.content)
	except IOError:
		print('Error: Could not write file.')
	except:
		print('Server Error: Please create a new cookie id.')


# download all files
def downloadFiles(session, path, url):
	try:
		# parse html
		r = session.get(rootUrl + url)
		soup = BeautifulSoup(r.text, "html.parser")

		# create directory
		dirname = path + toText(url[5:])
		if not os.path.exists(dirname):
			try:
				os.makedirs(dirname)
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		
		# download files in current directory
		for link in soup.find_all('a', {"class":"item file"}):
			getFile(session, path, link.get('href'))
		
		# search through subdirectories recursively
		for link in soup.find_all('a', {"class" : "item dir"}):
			downloadFiles(session, path, link.get('href'))
	except:
		print('Server Error: Please create a new cookie id.')


# main function
def main():
	# prepare session with authentication cookie
	cookiejar = requests.cookies.cookiejar_from_dict({'fileserv2012' : cookie})
	session = requests.Session()
	session.cookies = cookiejar
	
	# download all files
	downloadFiles(session, filepath, "")


main()
