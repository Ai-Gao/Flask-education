from flask import Blueprint

ws = Blueprint('ws', __name__, url_prefix='/ws')




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
