import requests
starturl = 'http://tuhh.fileserv.eu/thanks/?dir=Bachelor-MB-Pflichtmodule/Mathematik%20I/Lineare%20Algebra%20I/Klausuren'
pagesource = requests.get(starturl, allow_redirects = True, auth=('student', 'tuhh'))
print(pagesource.text)
list = pagesource.text.split('href="')
for item in list:
    print(item[:item.find('"')])


url = 'http://tuhh.fileserv.eu/thanks/Bachelor-MB-Pflichtmodule/Mathematik%20I/Lineare%20Algebra%20I/Klausuren/klausur_la1%202006%20SS_A_lsg.pdf'
r = requests.get(url, allow_redirects=True)
substring1 = "/"
filename = (url[url.rfind(substring1)+1:])
open(filename, 'wb').write(r.content)
print('saved ' + filename)
