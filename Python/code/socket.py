#socket-client.py
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.sina.com.cn', 80))

s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

buffer = []
while True:
	d = s.recv(1024)
	if d:
		buffer.append(d)
	else:
		break
data = b''.join(buffer)

s.close()

# 将http头和网页分离并打印http头，网页内容保存至文件
header, html = data.split(b'\r\n\r\n',1)
print(header.decode('utf-8'))
with open('sina.html','wb') as f:
	f.write(html)

#socket-server.py
# 服务器进程首先要绑定一个端口并监听来自其他客户端的连接。
# 如果某个客户端连接过来了，服务器就与该客户端建立Socket连接，随后的通信就靠这个Socket连接了。
# 所以，服务器会打开固定端口（比如80）监听，每来一个客户端连接，就创建该Socket连接。
# 由于服务器会有大量来自客户端的连接，所以，服务器要能够区分一个Socket连接是和哪个客户端绑定的。
# 一个Socket依赖4项：服务器地址、服务器端口、客户端地址、客户端端口来唯一确定一个Socket。
# 但是服务器还需要同时响应多个客户端的请求，所以，每个连接都需要一个新的进程或者新的线程来处理，否则，服务器一次就只能服务一个客户端了。

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 监听端口:
s.bind('127.0.0.1',9999)

# 调用listen()方法开始监听端口，传入的参数指定等待连接的最大数量：
s.listen(5)
print('Waiting for connection...')

while True:
	# 接收一个新连接
	sock,addr = s.accept()
	# 创建新线程来处理TCP连接
	t = threading.Thread(target=tcplink, args=sock, addr)
	t.start()

# 每个连接都必须创建新线程（或进程）来处理，否则，单线程在处理连接的过程中，无法接受其他客户端的连接
def tcplink(sock, addr):
	print('Accept new connection from %s:%s...' % addr)
	sock.send(b'Welcome!')
	while True:
		data = sock.recv(1024)
		time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
	sock.close()
	print('Connection from %s:%s closed.' %addr)

# 要测试这个服务器程序，我们还需要编写一个客户端程序
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()

# 我们需要打开两个命令行窗口，一个运行服务器程序，另一个运行客户端程序，就可以看到效果