# py爬虫.py
# 你需要学习：
# 1.基本的爬虫工作原理
# 2.基本的HTTP抓取工具scrapy
# 3.bloom filter
# 4.如果需要大规模网页抓取，你需要学习分布式爬虫的概念。其实你只需要学会怎样维护一个所有集群机器能够有效分享的分布式队列。最简单的实现是python-rq

# 1）首先你要明白爬虫怎样工作。想象你是一只蜘蛛，现在你被放到了互联“网”上。那么，你需要把所有的网页都看一遍。怎么办呢？没问题呀，你就随便从某个地方开始，比如说人民日报的首页，这个叫initial pages，用$表示吧。在人民日报的首页，你看到那个页面引向的各种链接。于是你很开心地从爬到了“国内新闻”那个页面。太好了，这样你就已经爬完了俩页面（首页和国内新闻）！暂且不用管爬下来的页面怎么处理的，你就想象你把这个页面完完整整抄成了个html放到了你身上。突然你发现， 在国内新闻这个页面上，有一个链接链回“首页”。作为一只聪明的蜘蛛，你肯定知道你不用爬回去的吧，因为你已经看过了啊。所以，你需要用你的脑子，存下你已经看过的页面地址。这样，每次看到一个可能需要爬的新链接，你就先查查你脑子里是不是已经去过这个页面地址。如果去过，那就别去了。好的，理论上如果所有的页面可以从initial page达到的话，那么可以证明你一定可以爬完所有的网页。那么在python里怎么实现呢？很简单
import Queue

initial_page = "http://www.renminribao.com"

url_queue = Queue.Queue()
seen = set()

seen.insert(initial_page)
url_queue.put(initial_page)

while(True): #一直进行直到海枯石烂
    if url_queue.size()>0:
        current_url = url_queue.get()    #拿出队例中第一个的url
        store(current_url)               #把这个url代表的网页存储好
        for next_url in extract_urls(current_url): #提取把这个url里链向的url
            if next_url not in seen:      
                seen.put(next_url)
                url_queue.put(next_url)
    else:
        break

# 2）效率如果你直接加工一下上面的代码直接运行的话，你需要一整年才能爬下整个豆瓣的内容。更别说Google这样的搜索引擎需要爬下全网的内容了。
# 问题出在哪呢？需要爬的网页实在太多太多了，而上面的代码太慢太慢了。设想全网有N个网站，那么分析一下判重的复杂度就是N*log(N)，因为所有网页要遍历一次，而每次判重用set的话需要log(N)的复杂度。
# OK，OK，我知道python的set实现是hash——不过这样还是太慢了，至少内存使用效率不高。通常的判重做法是怎样呢？Bloom Filter. 简单讲它仍然是一种hash的方法，但是它的特点是，它可以使用固定的内存（不随url的数量而增长）以O(1)的效率判定url是否已经在set中。
# 可惜天下没有白吃的午餐，它的唯一问题在于，如果这个url不在set中，BF可以100%确定这个url没有看过。但是如果这个url在set中，它会告诉你：这个url应该已经出现过，不过我有2%的不确定性。注意这里的不确定性在你分配的内存足够大的时候，可以变得很小很少。

# 3)集群化抓取
# 假设你现在有100台机器可以用，怎么用python实现一个分布式的爬取算法呢？
# 我们把这100台中的99台运算能力较小的机器叫作slave，另外一台较大的机器叫作master，那么回顾上面代码中的url_queue，如果我们能把这个queue放到这台master机器上，所有的slave都可以通过网络跟master联通，每当一个slave完成下载一个网页，就向master请求一个新的网页来抓取。
# 而每次slave新抓到一个网页，就把这个网页上所有的链接送到master的queue里去。同样，bloom filter也放到master上，但是现在master只发送确定没有被访问过的url给slave。Bloom Filter放到master的内存里，而被访问过的url放到运行在master上的Redis里，这样保证所有操作都是O(1)。

# 考虑如何用python实现：
# 在各台slave上装好scrapy,那么各台机子就变成了有抓取能力的slave，在master上装好redis和rq用作分布式队列
# 代码于是写成

# slave.py
current_url = request_from_master()
to_send = []
for next_url in extract_urls(current_url):
	to_send.append(next_url)

store(current_url)
send_to_master(to_send)

# master.py
distributed_queue = DistributedQueue()
bf = BloomFilter()

initial_pages = "www.renminribao.com"

while(True):
	if request == 'GET'
		if distributed_queue.size() > 0:
			send(distributed_queue.get())
		else:
			break
	elif request == 'POST':
		bf.put(request.url)