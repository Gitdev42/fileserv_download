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
username = 'student'
password = 'tuhh'


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


# download all files
def downloadFiles(session, path, url):
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


# main function
def main():
	# prepare session with authentication cookie
	loginData = {'user_name' : username, 'user_pass' : password}
	session = requests.Session()
	session.post(rootUrl, loginData)
	
	# download all files
	downloadFiles(session, filepath, "")
	print(r.text)


main()
