# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.lock = asyncio.Lock()
        self.sps_pps: bytes = b''  # Store SPS and PPS

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections.append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")

        # Send SPS and PPS if available
        if self.sps_pps:
            try:
                await websocket.send_bytes(self.sps_pps)
                print("Sent SPS and PPS to new client")
            except Exception as e:
                print(f"Error sending SPS/PPS: {e}")

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
                print(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, data: bytes, is_sps_pps=False):
        async with self.lock:
            connections = self.active_connections.copy()
        if not connections:
            print("No active connections to broadcast to.")
            return
        send_tasks = []
        for connection in connections:
            try:
                send_tasks.append(connection.send_bytes(data))
            except Exception as e:
                print(f"Error preparing to send data: {e}")
                send_tasks.append(asyncio.create_task(self.disconnect(connection)))
        results = await asyncio.gather(*send_tasks, return_exceptions=True)
        for connection, result in zip(connections, results):
            if isinstance(result, Exception):
                print(f"Error sending data to a client: {result}")
                await self.disconnect(connection)

    def set_sps_pps(self, sps_pps: bytes):
        self.sps_pps = sps_pps
        print("SPS and PPS updated")


manager = ConnectionManager()
