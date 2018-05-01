from simpledu.app import create_app

# 使用开发环境配置
app = create_app('development')

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
