import cv2


c = cv2.VideoCapture("rtsp://184.72.239.149/vod/mp4:BigBuckBunny_115k.mov")
while(1):
	ret, frame = c.read()
	cv2.imshow('VIDEO', frame)
	cv2.waitKey(1)
