from flask_login import UserMixin
import boto3
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
    
    @staticmethod
    def get_user_by_username(username):
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table('Users')
        response = table.query(
            KeyConditionExpression = Key('username').eq(username)
        )
        if response['Items']:
            item = response['Items'][0]
            return User(item['username'], item['email'], item['password_hash'])
        return None
    
class Follow:

    @staticmethod
    def add_follow(follower, followed):
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table('Follows')
        table.put_item(Item={
            'follower':follower,
            'followed':followed,
            'status': 'pending'
        })
    
    @staticmethod
    def get_followers(username):
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table('Follows')
        response = table.query(
            IndexName='followed-index',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('followed').eq(username)
        )
        return response.get('Items', [])
    
    @staticmethod
    def get_following(username):
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table('Follows')
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('follower').eq(username)
        )
        return response.get('Items', [])

    @staticmethod
    def accept_follow(follower, followed):
        print(f"Attempting to update follow request from {follower} to {followed}")  # Debug print
        try:
            dynamodb = get_dynamodb_client()
            table = dynamodb.Table('Follows')
            table.update_item(
                Key={
                    'follower': follower
                },
                UpdateExpression='SET #s = :s',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':s': 'accepted'}
            )
            print(f"Successfully updated follow request from {follower} to {followed}")
        except Exception as e:
            print(f"Error updating follow request: {e}")