from threading import Thread
from exceptions import SocketIOConnectionException, SocketIOLostConnection
import socketio


class SocketIO_Conn:
	def __init__(self, root):
		self._root=root
		self._socketio=socketio.Client()

		self._socketio.on('connections_data', namespace="/", handler=self.response)


		self.connect()
		#self.wait()

	def connect(self):
		try:
			self._socketio.connect(f'http://{self._root._config.socketio.host}:{self._root._config.socketio.port}')
		except socketio.exceptions.ConnectionError:
			raise SocketIOConnectionException


	def wait(self):
		t=Thread(target=self._socketio.wait, args=())
		t.start()


	def build_message(self, chat_uuid, user_uuid, model, message):
		return {
			"chat_uuid":chat_uuid,
			"user_uuid":user_uuid,
			"model": model,
			"message": message}

	def send_message(self, chat_uuid, user_uuid, model,  message):
		try:
			self._socketio.emit(
				'message',
				self.build_message(model=model, message=message, chat_uuid=chat_uuid, user_uuid=user_uuid)
				)
		except socketio.exceptions.BadNamespaceError:
			raise SocketIOLostConnection


	def response(self, data):
		self._root._socks_viewer_gui._connections_page.add_connection(data)
