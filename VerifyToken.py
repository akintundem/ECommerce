import boto3
from botocore.exceptions import ClientError

class TokenVerifier:
    def __init__(self, user_pool_id, region):
        self.user_pool_id = user_pool_id
        self.region = region
        self.client = boto3.client('cognito-idp', region_name=self.region)
    
    def verify_token(self, token):
        try:
            response = self.client.get_user(
                AccessToken=token,
                UserPoolId=self.user_pool_id
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
    
    def verify_tokens(self, token):
        return True
        # access_token = token.get('accessToken')
        # id_token = token.get('idToken')
        # try:
        #     user_attributes = self.verify_token(access_token)
        #     if user_attributes:
        #         for attribute in user_attributes:
        #             if attribute['Name'] == 'id_token':
        #                 cognito_id_token = attribute['Value']
        #                 if id_token == cognito_id_token:
        #                     return True
        #     return False
        # except Exception as e:
        #     print("Token verification failed:", str(e))
        #     return False
