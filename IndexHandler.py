import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import psycopg2
import psycopg2.extras
import json

from tornado.options import define, options
define('port', default=8631, help='run on the given port', type=int)

class Book(object):
	def __init__(self, title, author, cover_url, description, length):
		self.title = title
		self.author = author
		self.cover_url = cover_url
		self.description = description
		self.length = length 

class HttpResult(object):
	def __init__(self, statusCode, message, dataList):
		self.statusCode= statusCode
		self.message = message
		self.dataList= dataList


class BookListHandler(tornado.web.RequestHandler):
	def get(self):
		page_size = 20
		page_index = self.get_argument('page', 1)
		conn = psycopg2.connect(database='books', user='dbuser0', password='dbuser', host='127.0.0.1', port='5432')
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		cur.execute('SELECT * FROM books LIMIT %s OFFSET %s;', (page_size, 0))
		# 构造json响应
		db_books = cur.fetchall()
		# book_list = [Book(d['title'], d['author'], d['cover_url'], d['description'], d['length']) for d in db_books]	
				
		cur.close()
		conn.close()
		
		http_result = HttpResult(-1, "success", db_books)
		self.write(json.dumps(http_result.__dict__))

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r'/booklist', BookListHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

class Book(object):
	def __init__(self, title, author, cover_url, description, length):
		self.title = title
		self.author = author
		self.cover_url = cover_url
		self.description = description
		self.length = length

