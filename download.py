import os
import requests
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

# file the name of the file
def fixFileName(s):
	s = str.replace(s, "<", "-")
	s = str.replace(s, ">", "-")
	s = str.replace(s, "*", "-")
	s = str.replace(s, "|", "-")
	s = str.replace(s, "\\", "-")
	s = str.replace(s, "\"", "-")
	s = str.replace(s, "?", "-")
	s = str.replace(s, ":", "-")

	return s

# download file with a given url to a given path
def getFile(session, path, url):
	try:
		filename = path + fixFileName(toText(url))

		if os.path.isfile(filename):
			print('File "', filename, '" already exist in current directory. Skipping.')
			return

		r = session.get(rootUrl + url)
		print('Downloading "', filename, '".')
		open(filename, 'wb').write(r.content)

	except IOError:
		print('Error when writing file.')


# download all files
def downloadFiles(session, path, url):
	r = session.get(rootUrl + url)
	soup = BeautifulSoup(r.text, "html.parser")

	# create directory
	dirname = path + toText(url[5:])
	dirname = fixFileName(dirname)
	print('Creating directory named "', dirname, '".')

	if not os.path.exists(dirname):
		try:
			os.makedirs(dirname)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise

	# download files in current directory
	for link in soup.find_all('a', {"class":"item file"}):
		print('Found link containing file. Attempting download...')
		getFile(session, path, link.get('href'))

	# search through subdirectories recursively
	for link in soup.find_all('a', {"class" : "item dir"}):
		downloadFiles(session, path, link.get('href'))


def main():
	print('Preparing session with authentication cookie.')
	loginData = {'user_name' : username, 'user_pass' : password}
	session = requests.Session()
	session.post(rootUrl, loginData)

	print('Downloading files...')
	downloadFiles(session, filepath, "")
	print('Done!')

main()
