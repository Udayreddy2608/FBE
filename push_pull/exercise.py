from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"Active connections: {len(self.active_connections)}")

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)
        print(f"User {user_id} disconnected")

    async def broadcast(self, message: str):
        disconnected = []

        for user_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
            except:
                disconnected.append(user_id)

        for user_id in disconnected:
            self.disconnect(user_id)

    async def send_to_user(self, user_id: int, message: str, target_user: int):
        websocket = self.active_connections.get(target_user)
        if websocket:
            try:
                await websocket.send_text(f"Message from user: {user_id} -> {message}")
            except:
                self.disconnect(user_id)

messaging_manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user_id = int(websocket.query_params.get("user_id"))

    await messaging_manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            target_user = data["to"]
            message = data["message"]

            await messaging_manager.send_to_user(
                user_id=user_id,
                target_user=target_user,
                message=message
            )

    except WebSocketDisconnect:
        messaging_manager.disconnect(user_id)
