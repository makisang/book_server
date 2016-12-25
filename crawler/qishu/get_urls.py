from bs4 import BeautifulSoup
from urllib import request
import re

url1 = 'http://www.qisuu.com/soft/sort02/index';


def get_book_urls(url):
	with request.urlopen(url) as f:
		bs = BeautifulSoup(f.read(), 'html.parser')

	with open('urls.txt', 'a') as url_file:
		for tag in bs.find_all(name='a', href=re.compile('^/[0-9]{4,5}.html')):
			url_file.write('http://www.qisuu.com/%s\n' % (tag.get('href')))
			print(tag.get('href'))

if __name__ == '__main__':
	for i in range(1, 20):
		if i==1:
			get_book_urls('%s.html' % (url1))
		else:
			get_book_urls('%s_%d.html' % (url1, i))
