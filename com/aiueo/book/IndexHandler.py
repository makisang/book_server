import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
from handler.BookListHandler import BookListHandler

from tornado.options import define, options
define('port', default=8631, help='run on the given port', type=int)

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

