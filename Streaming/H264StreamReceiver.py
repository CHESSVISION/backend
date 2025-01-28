import asyncio
import websockets
import av
import cv2
from av import VideoFrame


class H264StreamReceiver:
    def __init__(self, uri):
        self.uri = uri
        self.decoder = av.codec.CodecContext.create('h264', 'r')
        self.buffer = bytearray()

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            print(f"Connected to {self.uri}")
            await self.receive_stream(websocket)

    async def receive_stream(self, websocket):
        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    self.buffer.extend(message)
                    self.decode_buffer()
                else:
                    print("Received non-bytes message; ignoring.")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")

    def decode_buffer(self):
        # Attempt to decode as much as possible from the buffer
        while True:
            try:
                packets = self.decoder.parse(self.buffer)
                if not packets:
                    break

                for packet in packets:
                    frames = self.decoder.decode(packet)
                    for frame in frames:
                        self.display_frame(frame)

                # Clear the buffer after decoding
                self.buffer.clear()
            except av.AVError as e:
                # Not enough data to decode; wait for more
                # Optionally, implement buffering strategies here
                # For now, break and wait for more data
                break

    def display_frame(self, frame: VideoFrame):
        # Convert AV Frame to OpenCV image
        img = frame.to_ndarray(format='bgr24')
        cv2.imshow('H264 Stream', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            asyncio.get_event_loop().stop()
