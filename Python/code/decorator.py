# decorator.py
# 本质上，decorator就是一个返回函数的高阶函数

# 我们要定义一个能打印日志的decorator，可以定义如下:
def log(func):
	def wrapper(*args, **kw):
		print('call %s():' % func.__name__)
		return func(*args, **kw)
	return wrapper
# 观察上面的log，因为它是一个decorator，所以接受一个函数作为参数，并返回一个函数。
# 我们要借助Python的@语法，把decorator置于函数的定义处：
@log
def now():
	print('2015-3-25')

# 调用now(),不仅会执行now()本身，还会在运行now()函数前打印一行日志

# 把@log放到now()的定义处，相当于执行了语句：
now = log(now)

# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本：
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

# 这个3层嵌套的decorator用法如下：

@log('execute')
def now():
    print('2015-3-25')
