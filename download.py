#!/usr/bin/env python3

import os
import requests
import urllib.parse
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# general settings
root_url = 'http://tuhh.fileserv.eu/thanks/'
filepath = "files/"
username = 'student'
password = 'tuhh'

# replace spaces with specified char, set to None to keep spaces
space_replacement = '-'


# remove url encoding
def to_text(url):
	return urllib.parse.unquote(url)


# sanitize the file name input
def fix_filename(s):
	forbidden_chars = '<>:"\\|?*'
	for c in forbidden_chars:
		s = str.replace(s, c, '-')
	if space_replacement is not None:
		s = str.replace(s, ' ', space_replacement)
	return s


# download file with a given url to a given path
def get_file(session, path, url):
	try:
		filename = path + fix_filename(to_text(url))

		if os.path.isfile(filename):
			print('File "', filename, '" already exist in current directory. Skipping.')
			return

		r = session.get(root_url + url)
		print('Downloading "', filename, '".')
		open(filename, 'wb').write(r.content)

	except IOError:
		print('Error when writing file.')


# download all files
def download_files(session, path, url):
	r = session.get(root_url + url)
	soup = BeautifulSoup(r.text, "html.parser")

	# create directory
	dirname = fix_filename(path + to_text(url[5:]))
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
		get_file(session, path, link.get('href'))

	# search through subdirectories recursively
	for link in soup.find_all('a', {"class" : "item dir"}):
		download_files(session, path, link.get('href'))


def main():
	print('Preparing session with authentication cookie.')
	login_data = {'user_name' : username, 'user_pass' : password}
	session = requests.Session()
	session.post(root_url, login_data)

	print('Downloading files...')
	download_files(session, filepath, "")
	print('Done!')


main()
