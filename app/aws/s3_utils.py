import boto3
import json
from flask import current_app

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=current_app.config['S3_AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['S3_AWS_SECRET_ACCESS_KEY']
    )

def list_blog_posts(s3, bucket_name):
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)

    blogs = []
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'].endswith('.json'):
                    try:
                        file_obj = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
                        file_content = file_obj['Body'].read().decode('utf-8')
                        if file_content.strip():  # Check if the content is not empty
                            blog_post = json.loads(file_content)
                            blogs.append(blog_post)
                        else:
                            print(f"Empty file: {obj['Key']}")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {obj['Key']}: {e}")
                    except Exception as e:
                        print(f"Error reading file {obj['Key']}: {e}")

    return blogs

# def list_blog_posts(s3, bucket_name):
#     response = s3.list_objects_v2(Bucket=bucket_name, Prefix='blogs/')
#     blogs = []
#     if 'Contents' in response:
#         for obj in response['Contents']:
#             if obj['Key'][-1] != '/':
#                 file_obj = s3.get_object(Bucket=bucket_name, Key=obj['Key'])
#                 blogs.append(json.loads(file_obj['Body'].read().decode('utf-8')))
#     return blogs


def upload_blog_posts_to_s3(username, post_id, blog_post):
    s3 = get_s3_client()
    s3.put_object(
        Bucket=current_app.config['BUCKET_NAME'],
        Key=f'blogs/{username}/{post_id}.json',
        Body=json.dumps(blog_post)
    )

def get_blog_post_from_s3(username, post_id):
    s3 = get_s3_client()
    response = s3.get_object(
        Bucket=current_app.config['BUCKET_NAME'],
        Key=f'blogs/{username}/{post_id}.json'
    )
    return json.loads(response['Body'].read())