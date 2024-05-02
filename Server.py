import json
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
