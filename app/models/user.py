from flask_login import UserMixin
from boto3.dynamodb.conditions import Key, Attr
from app import bcrypt
from app.aws.dynamodb_utils import get_dynamodb_client, create_user

class User(UserMixin):
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def find_by_username(username):
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table('Users')
        response = table.query(
            KeyConditionExpression = Key('username').eq(username)
        )
        if response['Items']:
            item = response['Items'][0]
            return User(item['username'], item['email'], item['password_hash'])
        return None
    
    @staticmethod
    def find_by_email(email):
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table('Users')
        response = table.scan(
            FilterExpression=Attr('email').eq(email)
        )
        if response['Items']:
            item=response['Items'][0]
            return User(item['username'], item['email'], item['password_hash'])
        return None
    
    def save_to_db(self):
        create_user(self.username, self.email, self.password_hash)

    @staticmethod
    def verify_password(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)
    
    def get_id(self):
        return self.username
    