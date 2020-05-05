import cv2 as cv
from app.Stream import Stream

s = Stream()
qr = cv.QRCodeDetector()

while True:
    frame = s.get_frame()
    data, _, _ = qr.detectAndDecode(frame)

    print(data)
    cv.imshow('out', frame)
    cv.waitKey(1)
