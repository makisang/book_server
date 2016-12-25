from bs4 import BeautifulSoup
from urllib import request

url1 = 'http://all.hjsm.tom.com/index.php?&classid=0&mate=0&wordcount=0&time=0&type=total_endfund&novip=0&vip=0&onlyOver=0&onlyWrite=0&onlyNew=0&onlyPub=0'

def get_book_urls(url):
	with request.urlopen(url) as f:
		bs = BeautifulSoup(f.read(), 'html.parser')

	with open('urls.txt', 'w') as url_file:
		L = bs.find_all('a', 'tit')
		for tag in L:
			url_file.write(tag.get('href') + '\n')

if __name__ == '__main__':
	for i in range(1, 18):
		get_book_urls('%s&p=%d' % (url1, i))
		

