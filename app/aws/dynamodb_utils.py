import boto3
from boto3.dynamodb.conditions import Key
import json
from flask import current_app

def get_dynamodb_client():
    return boto3.resource(
        'dynamodb',
        aws_access_key_id=current_app.config['DYNAMODB_USER_CRED_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['DYNAMODB_USER_CRED_SECRET_ACCESS_KEY'],
        region_name='us-east-1'
    )

def create_user(username, email, password_hash):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('Users')
    table.put_item(
        Item={
            'username' : username,
            'email':email,
            'password_hash':password_hash
        }
    )

def create_blog_post_metadata(post_id, username, title):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('BlogPosts')
    table.put_item(
        Item={
            'post_id':post_id,
            'username':username,
            'title':title
        }
    )

def get_blog_posts_by_user(username):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('BlogPosts')
    response = table.query(
        IndexName='username-index',
        KeyConditionExpression=Key('username').eq(username)
    )
    return response['Items']

def get_all_blog_posts():
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('BlogPosts')
    response = table.scan()
    return response['Items']
