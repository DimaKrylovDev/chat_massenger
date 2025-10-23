from fastapi import FastAPI, WebSocket

app = FastAPI 

@app.websocket('/ws/chat')
2