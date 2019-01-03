import rtsp

droneUri = 'rtsp://192.168.100.1/cam1/mpeg4'

class Camera:
	def __init__(self):
		self.rtspClient = rtsp.Client(rtsp_server_uri=droneUri)