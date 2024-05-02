import websocket
import json

def on_message(ws, message):
    print("Received message:", message)
    # Handle incoming messages from the server here

def on_error(ws, error):
    print("Error:", error)
    # Handle WebSocket errors here

def on_close(ws):
    print("WebSocket closed")
    # Handle WebSocket close event here

def on_open(ws):
    print("WebSocket opened")
    # Example registration message
    registration_data = {
        'action': 'register',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'password': 'password123'
    }
    ws.send(json.dumps(registration_data))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8888/websocket",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
