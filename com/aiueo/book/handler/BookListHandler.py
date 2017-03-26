import tornado.web
import psycopg2
import psycopg2.extras
import json
import sys
sys.path.append('..')
from bean.Book import Book
from bean.HttpResult import HttpResult

class BookListHandler(tornado.web.RequestHandler):
	def get(self):
		page_size = 20
		page_index = self.get_argument('page', 1)
		conn = psycopg2.connect(database='d_books', user='amigo', password='amigo', host='127.0.0.1', port='5432')
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute('SELECT * FROM book_qishu LIMIT %s OFFSET %s;', (page_size, 0))
		
		db_books = cur.fetchall()
		# book_list = [Book(d['title'], d['author'], d['cover_url'], d['description'], d['length']) for d in db_books]	
				
		cur.close()
		conn.close()
		
		http_result = HttpResult(-1, "success", db_books)
		self.write(json.dumps(http_result.__dict__))

