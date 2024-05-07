
import json
import base64
import boto3
from botocore.exceptions import ClientError
from UserAuth.StubUser import StubUserRepository
from UserAuth.UserAuth import UserAuth
import configparser

import tornado.ioloop
import tornado.web
import tornado.websocket

config = configparser.ConfigParser()
config.read('cognito_cred.config')

user_storage = StubUserRepository()
user_auth = UserAuth()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        data = json.loads(message)
        token = data.get('Token')
        access_token = token.get('accessToken')
        id_token = token.get('idToken')
        if self.verify_tokens(access_token, id_token):
            # Tokens are valid, handle the action of the message
            action = data.get('action')
            if action == 'request_song':
                # Request a song
                song_name = data.get('songName')
                song_artist = data.get('songArtist')
                song_url = data.get('songURL')
                response = {
                    'status': 'success',
                    'message': 'Song requested'
                }
                self.write_message(json.dumps(response))
        else: 
            # Tokens are invalid, send an error response
            response = {
                'status': 'error',
                'message': 'Invalid tokens'
            }
            self.write_message(json.dumps(response))

    def on_close(self):
        print("WebSocket closed")

    def verify_tokens(self, access_token, id_token):
        # Replace these values with your AWS Cognito User Pool ID and AWS region
        user_pool_id = config.get('Cognito', 'user_pool_id')
        region = config.get('Cognito', 'region')
        
        try:
            user_attributes = self.verify_token(access_token, user_pool_id, region)
            if user_attributes:
                for attribute in user_attributes:
                    if attribute['Name'] == 'id_token':
                        cognito_id_token = attribute['Value']
                        if id_token == cognito_id_token:
                            return True
            return False
        except Exception as e:
            print("Token verification failed:", str(e))
            return False


    def verify_token(self, token, user_pool_id, region):
        client = boto3.client('cognito-idp', region_name=region)
        try:
            response = client.get_user(
                AccessToken=token,
                UserPoolId=user_pool_id
            )
            return response['UserAttributes']  # If token is valid, return the user attributes
        except ClientError as e:
            if e.response['Error']['Code'] == 'NotAuthorizedException':
                print("Token verification failed: Token is not valid.")
            else:
                print("Token verification failed:", e.response['Error']['Message'])
            return None
        except Exception as e:
            print("Token verification failed:", str(e))
            return None

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("WebSocket server started at port 8888")
    tornado.ioloop.IOLoop.current().start()
