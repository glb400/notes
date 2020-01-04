# WSGI.py
# 运行WSGI服务

# hello.py
# 实现Web应用程序的WSGI处理函数
def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	return [b'<h1>Hello, web!</h1>']

# server.py
from wsgiref.simple_server import make_server
from hello import application

# 创建服务器，IP地址为空，端口8000，处理函数application
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')

# 开始监听http请求
httpd.serve_forever()

# 如果你觉得这个WEB应用太简单，可以稍微改造一下，从environ里读取PATH_INFO
# 这样可以显示更加动态的内容

# hello.py

def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
	return [body.encode('utf-8')]