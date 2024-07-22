from requests import get

class API_Conn:
	def __init__(self, parent):
		self._parent=parent

	def get_geoip_data(self, remote_addr):
		r=get(f"http://ip-api.com/json/{remote_addr}")

		return r.json()