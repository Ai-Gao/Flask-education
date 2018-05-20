from flask import Blueprint
import redis
import gevent


ws = Blueprint('ws', __name__, url_prefix='/ws')

# 创建 redis 连接

redis = redis.from_url('redis://127.0.0.1:6379')

class Chatroom(object):
    def __init__(self):

        self.clients = []
        # 初始化 pubsub系统
        self.pubsub = redis.pubsub()
        # 订阅频道
        self.pubsub.subscribe('chat')

    # ws对象注册
    def register(self, client):
        self.clients.append(client)

    # 给每一个客户端 client 发送data
    def send(self, client, data):
        try:
            # python3 接收到的消息为二进制
            client.send(data.decode('utf-8'))
        except:
            self.clients.remove(client)

    def run(self):
        # 将接收到的消息发给所有客户端
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message.get('data')
                for client in self.clients:
                    # gevent 异步发送
                    gevent.spawn(self.send, client, data)

    def start(self):
        # 异步执行 run 函数
        gevent.spawn(self.run)

# 实例化对象
chat = Chatroom()
# 异步启动聊天室
chat.start()

# 服务器端

# 定义send发送信息路由
@ws.route('/send')
def index(ws):
    # flask-sockets,ws对象将被自动注入到路由处理函数
    while not ws.closed:
        message = ws.receive()

        if message:
            redis.publish('chat', message)

# 定义recv收取信息路由
@ws.route('/recv')
def outbox(ws):
    chat.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)


"""
from flask import Blueprint, render_template
import redis
import gevent

ws = Blueprint('ws', __name__, url_prefix='/ws' )

redis = redis.from_url('redis://127.0.0.1:6379')

class Chatroom(object):
    def __init__(self):
        self.clients = []
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe('chat')

    def register(self, client):
        self.clients.append(client)

    def send(self, client, data):
        try:
            client.send(data.decode('utf-8'))
        except:
            self.clients.remove(client)

    def run(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message.get('data')
                for client in self.clients:
                    gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)

chat = Chatroom()
chat.start()

@ws.route('/send')
def inbox(ws):
    while not ws.closed:
        message = ws.receive()

        if message:
            redis.publish('chat', message)

@ws.route('/recv')
def outbox(ws):
    chat.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)

@ws.route('/live')
def index():
    return render_template('live/index.html')
"""
