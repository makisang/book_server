from bs4 import BeautifulSoup
from urllib import request
import re
import psycopg2
from urllib.error import URLError
from http.client import IncompleteRead

def scrapy_books():
	with open('urls.txt', 'r') as f:
		for url in f.readlines():
				try:
					read_book_info(url)
				except URLError as e:
					print('URLError: ', e)

def read_book_info(url):
	with request.urlopen(url) as resp:
		try:
			html_str = resp.read()
		except IncompleteRead as e:
			print('IncompleteRead: ', e)
			return
		bs = BeautifulSoup(html_str, 'html.parser')
		tag = bs.find_all('div', class_='r fr')
		# 书名 
		title_str = tag[0].a.text.strip()
		# 作者
		author = tag[0].find('a', href=re.compile('http://space')).text.strip()
		# 书籍简介
		description = tag[0].find('div', 'introCon').a.text.strip()
		# 封面图片url
		cover = bs.find_all('a', title=title_str)[0].img.get('src')
		# 字数
		length = bs.find('div', class_='intr').ul.select('li:nth-of-type(2)')[0].text[3:]
		# 章节界面url
		catalog_url = bs.find_all('div', 'inputli')[0].input.get('onclick')[17:-1]
		# 页面url
		home_url = url
		
		# 开启postgresql连接 
		conn = psycopg2.connect(database='books', user='dbuser0', password='dbuser', host='127.0.0.1', port='5432')
		cur = conn.cursor()
		# 执行插入语句
		cur.execute('''INSERT INTO books(title, author, description, cover_url, length, catalog_url, home_url) VALUES 
		(%s, %s, %s, %s, %s, %s, %s)'''
		, (title_str, author, description, cover, length, catalog_url, home_url))
		print('insert book: %s' % (title_str))
		conn.commit()
		cur.close()
		conn.close()

if __name__ == '__main__':
	scrapy_books()

