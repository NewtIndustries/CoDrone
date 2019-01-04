import rtsp

droneUri = 'rtsp://192.168.100.1/cam1/mpeg4'

class Camera:
	@property
	def isCameraConnected(self):
		return self.rtspClient.isOpened()

	def __init__(self):
		self.rtspClient = rtsp.Client(rtsp_server_uri=droneUri)
		self.rtspClient.open()

	def readFrame(self):
		self.rtspClient.read().show()

	def preview(self):
		self.rtspClient.preview()
