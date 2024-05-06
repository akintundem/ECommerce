import json
import base64

from UserAuth.StubUser import StubUserRepository
from UserAuth.UserAuth import UserAuth

import tornado.ioloop
import tornado.web
import tornado.websocket


user_storage = StubUserRepository()
user_auth = UserAuth()

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print("Received message:", message)
        data = json.loads(message)
        action = data.get('action')

        if action == 'register':
            # Handle registration logic here
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
            # Perform registration processs
            success, message = user_auth.register_user(first_name, last_name, email, password, phone,user_storage)
            if success:
                response = {
                    'status': 'success',
                    'message': message
                }
            else:
                response = {
                    'status': 'error',
                    'message': message
                }
            self.write_message(json.dumps(response))

        elif action == 'request_song':
            # Handle song request logic here
            message = data.get('message')
            song_name = message.get('song_name')
            artist_name = message.get('artist_name')
            request_id = message.get('request_id')
            song_path = 'Lojay-Ft-Sarz-Monalisa-1-(TrendyBeatz.com).mp3'
            with open(song_path, 'rb') as file:
                song_data = file.read()
            
            song_data_base64 = base64.b64encode(song_data).decode('utf-8')

            response = {
                'status': 'success',
                'message': {
                    'song_name': song_name,
                    'artist_name': artist_name,
                    'request_id': request_id,
                    'songdata': song_data_base64,
                }
            }
            try:
                self.write_message(json.dumps(response))
            except tornado.websocket.WebSocketClosedError:
                print("WebSocket connection closed before sending message")

        elif action == 'login':
            # Handle login logic here
            username = data.get('username')
            password = data.get('password')
            success, message = user_auth.login_user(username, password, user_storage)
            response = {
                'status': 'success',
                'message': 'Login successful'
            }
            self.write_message(json.dumps(response))

        elif action == 'reset':
            # Handle password reset logic here
            username = data.get('username')
            success, message = user_auth.reset_password(username, user_storage)
            response = {
                'status': 'success',
                'message': 'Password reset successful'
            }
            self.write_message(json.dumps(response))

        else:
            response = {
                'status': 'error',
                'message': 'Invalid action'
            }
            self.write_message(json.dumps(response))

def on_close(self):
    print("WebSocket closed")

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("WebSocket server started at port 8888")
    tornado.ioloop.IOLoop.current().start()
