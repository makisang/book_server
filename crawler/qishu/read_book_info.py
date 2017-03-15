from bs4 import BeautifulSoup
from urllib import request
import re
import psycopg2
from urllib.error import URLError
from urllib.error import HTTPError
from http.client import IncompleteRead
import requests

qing_file_url = 'http://book1-files.pek3a.qingstor.com/'
qing_img_url = 'http://book1-covers.pek3a.qingstor.com/'

def read_book_info(url):
	with request.urlopen(url) as resp:
		html_str = resp.read()
		bs = BeautifulSoup(html_str, 'html.parser')
	
	# 封面图片
	cover_url = 'http://www.qisuu.com/' + bs.find('div', 'detail_pic').img.get('src')	
	# 书名
	title = bs.find('div', 'detail_right').h1.text[1:-3]
	# 作者
	author =  bs.find('div', 'detail_right').find_all('li', 'small')[6].text[5:]
	# 页面url
	home_url = url
	# 简介
	str_list = []
	for div_tag in bs.find('div', 'showInfo').find_all('div'):
		str_list.append(div_tag.text)
	description = ''.join(str_list)
	# 字数
	mb_size = bs.find('div', 'detail_right').find_all('li', 'small')[2].text[5:-2]
	try:
		length =int(float(mb_size) * 524288)
	except ValueError as e:
		print('mb_size ValueError: ', e)
		length = 911015
	
	# 上传文件到青云
	download_url = bs.find_all('a', 'downButton')[1].get('href')
	try:
		txt_bytes = requests.get(download_url).content
	except HTTPError as e:
		print('download link missing: ', e)
		return

	headers = {'Content-Type':'text/plain', 'Content-Length':len(txt_bytes)}
	res1 = requests.put(qing_file_url + title + '.txt', data = txt_bytes, headers = headers)
	if res1.status_code == 201:
		print('upload to QingStor success: %s.txt' % (title))
	else:
		print('upload to QingStor failure: %s.txt' % (title))
		return
	img_bytes = requests.get(cover_url).content
	headers = {'Content-Type':'image/*', 'Content-Length':len(img_bytes)}
	res2 = requests.put(qing_img_url + title + '.jpg', data = img_bytes, headers = headers)
	if res2.status_code == 201:
		print('upload to QingStor success: %s.jpg' % (title))
	else:
		print('upload to QingStor failure: %s.jpg' % (title))
		return

	conn = psycopg2.connect(database='d_books', user='amigo', password='amigo', host='127.0.0.1', port='5432')
	cur = conn.cursor()
	cur.execute('''INSERT INTO t_books(title, author, description, length, home_url) VALUES
	(%s, %s, %s, %s, %s)''', (title, author, description, length, home_url))
	print('insert book: %s' % (title))
	conn.commit()
	cur.close()
	conn.close()
	


if __name__ == '__main__':
	with open('urls.txt', 'r') as f:
		for url in f.readlines():
			read_book_info(url)

