import av
import threading
import av
import cv2
from av import VideoFrame


class BackgroundTasks(threading.Thread):
    def __init__(self):
        self.buffer = bytes()
        self.decoder = av.codec.CodecContext.create('h264', 'r')

    def decode_buffer(self):
        print("decode buffer")
        # Attempt to decode as much as possible from the buffer
        while True:
            try:
                print("decoding buffer")
                packets = self.decoder.parse(self.buffer)
                print("show packet")
                print(packets)
                if not packets:
                    break

                for packet in packets:
                    print("decoding packet")
                    frames = packet.decode()
                    for frame in frames:
                        self.display_frame(frame)
                self.buffer = bytes()
            except av.AVError as e:
                # Not enough data to decode; wait for more
                # Optionally, implement buffering strategies here
                # For now, break and wait for more data
                break

    def display_frame(self, frame: VideoFrame):
        # Convert AV Frame to OpenCV image
        img = frame.to_ndarray(format='bgr24')
        print(img)
        cv2.imshow('H264 Stream', img)
