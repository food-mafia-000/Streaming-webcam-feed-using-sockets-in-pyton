import socket
#import cv2
import numpy as np
import imutils
import pickle
import struct

s=socket.socket()
s.bind(('localhost', 6969))
s.listen(5)
data = b""
payload_size = struct.calcsize("Q")

while True:
    c, add = s.accept()
    print("Successfully connected with ", add)

    while True:
        while (len(data)) < payload_size:
            packet = c.recv(4 * 1024)
            if packet:
                data += packet
            else:
                break

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += c.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2.imshow("receiving...", frame)
    if cv2.waitKey(1) == 27:
        s.close()