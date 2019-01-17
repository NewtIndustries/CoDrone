import socket
import re
import http.client
import pprint

# https://gist.github.com/jn0/8b98652f9fb8f8d7afbf4915f63f6726

pp = pprint.PrettyPrinter()

def printrec(recstr):
	""" Pretty-printing rtsp strings
	"""

	recs = recstr.split('\r\n')
	for rec in recs:
		print(rec)

def getPorts(searchString, st):
	pat = re.compile(searchString + "=\d*-\d*")
	pat2 = re.compile('\d+')
	mString = pat.findall(st)[0]
	nums = pat2.findall(mString)
	numas = []
	for num in nums:
		numas.append(int(num))

	return numas

def getSessionId(response):
	recs = response.split("\r\n")
	for rec in recs:
		ss = rec.split()
		if (ss[0].strip() == "Session:"):
			return int(ss[1].split(';')[0].strip())
	return -1

# ip = '184.72.239.149'
# rtspUrl = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov'
host = '184.72.239.149'
rtspUrl = 'rtsp://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov'

# conn = http.client.HTTPSConnection(rtspUrl)
print('Attempting to connect to ' + host + ' on port 554')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 554))

# options = (
# 	'OPTIONS ' + rtspUrl + 'RTSP/1.0' + '\r\n' +
# 	'CSeq: 1\r\n' + 
# 	'User-Agent: python\r\n\r\n'
# )

# print('Sending Options')
# print(options)

# http = 
# http.client.HTTPSConnection(host).send(options)

# s.send(options.encode('utf-8'))
# print('Sent Options\r\n\r\n')

# print('Receiving Option Response')
# response = s.recv(4096)
# print(response)

describe = (
	'DESCRIBE ' + rtspUrl + ' RTSP/1.0' + '\r\n' + 
	'CSeq: 2\r\n' +
	'User-Agent: python\r\n' +
	'Accept: application/sdp\r\n\r\n'
)
print('Sending Describe')
print(describe)
s.send(describe.encode('utf-8'))
print('Sent Describe')

print('Receiving Describe Response')
response = s.recv(4096)
print(response)


setup = (
	'SETUP ' + rtspUrl + '/trackID=1 RTSP/1.0\r\n' +
	'CSeq: 3\r\n' +
	'User-Agent: python\r\n' +
	'Transport: RTP/AVP;unicast;client_port=60784-60785\r\n\r\n'
)

print('Sending Setup')
print(setup)
s.send(setup.encode('utf-8'))
print('Sent Setup')

print('Receiving Setup Response')
response = s.recv(4096)
print(response)

stringResponse = response.decode('utf-8')
print(stringResponse)



sessionId = getSessionId(stringResponse)
serverPorts = getPorts('server_port', stringResponse)
clientPorts = getPorts('client_port', stringResponse)
print('Session Id')
pp.pprint(sessionId)
print('Server Ports')
pp.pprint(serverPorts)
print('Client Ports')
pp.pprint(clientPorts)
# pp.pprint('ServerPorts:' + dir(serverPorts))

streamingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
streamingSocket.bind(("127.0.0.1", 60784))
streamingSocket.settimeout(15)

play = (
	"PLAY " + rtspUrl + " RTSP/1.0\r\n" +
	"CSeq: 4\r\n" +
	"Session: " + str(sessionId) + "\r\n" +
	"Range: npt=0.000-\r\n\r\n"
)


print('Sending Play')
print(play)

s.send(play.encode('utf-8'))
print('Sent Play')
response = s.recv(4096)
print(response)

data = streamingSocket.recv(1)
print(data)
# while True:
# 	data, addr = streamingSocket.recvfrom(1024)
# 	# data = streamingSocket.recv(4096)
# 	# if not data:
# 	# 	break
# 	# print(data)