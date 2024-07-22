from eventlet import wsgi, monkey_patch
from adisconfig import adisconfig
from json import loads, dumps
from threading import Thread
from redis import StrictRedis
from pprint import pprint

monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO

import functools

class socketio_dispatcher:
    active=True
    def __init__(self, application, socketio):

        self.application=application
        self.socketio=socketio

        self.config=adisconfig('./configs/socketio_dispatcher.yaml')

        self.redis_cli=StrictRedis(
            host=self.config.redis.host,
            port=self.config.redis.port,
            db=self.config.redis.db)

        self.bind_socketio_events()
        self.application.config['SECRET_KEY'] = self.config.socketio.secret

    def response_process(self, channel, method, properties, body):
        data=loads(body.decode('utf8'))
        self.socketio.emit(
            "response",
            data,
            to=data['socketio_session_id']
        )

    def start(self):
        try:
            print(f'Starting socketio_dispatcher at {self.config.socketio.host}:{self.config.socketio.port}...')
            self.socketio.start_background_task(target=self.loop)
            self.socketio.run(self.application, host=self.config.socketio.host, port=self.config.socketio.port)
        except:
            print(f'Stopping socketio_dispatcher...')
            self.stop()

    def stop(self):
        self.active=False

    def loop(self):
        pubsub=self.redis_cli.pubsub()
        pubsub.subscribe('socks_viewer-connections')
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                self.socketio.emit('connections_data',loads(message['data'].decode('utf-8')))
                print(message['data'].decode('utf-8'))


    def bind_socketio_events(self):
        pass

if __name__=="__main__":
    app = Flask(__name__)
    socketio = SocketIO(
        app,
        cors_allowed_origins="*")

    socketio_dispatcher=socketio_dispatcher(app, socketio)
    socketio_dispatcher.start()
