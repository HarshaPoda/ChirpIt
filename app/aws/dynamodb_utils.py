import datetime
import uuid
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import NoCredentialsError

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

def create_blog_post_metadata(post_id, username, title, likes, comments):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('BlogPosts')
    table.put_item(
        Item={
            'post_id':post_id,
            'username':username,
            'title':title,
            'likes': likes,
            'comments': comments
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

def get_blog_post_metadata(post_id):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('BlogPosts')
    response = table.get_item(Key={'post_id': post_id})
    return response.get('Item', None)

def update_blog_post_likes(post_id):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('BlogPosts')
    table.update_item(
        Key={'post_id': post_id},
        UpdateExpression='ADD likes :inc',
        ExpressionAttributeValues={':inc': 1}
    )

def add_blog_post_comment(post_id, comment):
    comment_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('Comments')
    table.put_item(Item={
        'comment_id': comment_id,
        'post_id': post_id,
        'username': comment.username,
        'content': comment.content,
        'created_at': created_at
    })
    blogposts_table = dynamodb.Table('BlogPosts')
    blogposts_table.update_item(
        Key={'post_id': post_id},
        UpdateExpression='SET comments = list_append(comments, :c)',
        ExpressionAttributeValues={':c': [comment_id]}
    )

def get_comments_for_post(post_id):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table('Comments')
    response = table.query(
        IndexName='post_id-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('post_id').eq(post_id)
    )
    return response.get('Items', [])