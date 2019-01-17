# import pycurl
# import pprint
# from io import StringIO

# class RtspClient:
# 	def __init__(self):
# 		self.url = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov'
# 		self.buffer = StringIO()
# 		self.curl = pycurl.Curl()
# 		self.curl.setopt(pycurl.VERBOSE, True)
# 		pp = pprint.PrettyPrinter(width=41, compact=False)
# 		pp.pprint(self.curl)
# 		pp.pprint(dir(pycurl))
# 	def options(self):
# 		self.curl.setopt(pycurl.URL, self.url)
# 		self.curl.setopt(pycurl.WRITEDATA, self.buffer)
# 		# self.curl.setopt(pycurl.CURLOPT_RTSP_STREAM_URI, self.url)
# 		# self.curl.setopt(pycurl.OPT_RTSP_REQUEST, pycurl.RTSPREQ_OPTIONS)
# 		return False
	
# 	def describe(self):
# 		return False

# 	def setup(self):
# 		return False

# 	def play(self):
# 		return False