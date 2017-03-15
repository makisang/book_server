
class HttpResult(object):
	def __init__(self, statusCode, message, data):
		self.statusCode= statusCode
		self.message = message
		self.data = data
