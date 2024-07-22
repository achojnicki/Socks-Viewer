from adisconfig import adisconfig

from socketio_conn import SocketIO_Conn
from api_conn import API_Conn

from socks_viewer.pages.connections_page import Connections_Page
from exceptions import SocketIOConnectionException
from sys import exit
import wx


class Socks_Viewer_Gui(wx.Frame):

	def __init__(self, root):
		self._on_load=[]

		self._root=root
		wx.Frame.__init__(self, None, title="Socks Viewer", size=(1680,950), style=wx.DEFAULT_FRAME_STYLE)


		self._notebook=wx.Notebook(self)
		self._connections_page=Connections_Page(self._root, self._notebook, self)
		self._notebook.AddPage(self._connections_page, "Connections")

		self.Bind(wx.EVT_CLOSE, self._on_close)

	def _do_on_load(self, event):
		for a in self._on_load:
			a()

	def _on_close(self, event):
		exit(0)

class Socks_Viewer:
	def __init__(self):
		self._app=wx.App()
		self._config=adisconfig('./configs/gui.yaml')
		try:
			self._socketio_conn=SocketIO_Conn(self)
		except SocketIOConnectionException:
			wx.MessageBox('Unable to connect to socketio_dispatcher', 'Error')
			self._app.Destroy()
			exit(1)

		self._api_conn=API_Conn(self)
		self._socks_viewer_gui=Socks_Viewer_Gui(self)


	def start(self):
		self._socks_viewer_gui.Show()
		self._app.MainLoop()
		
