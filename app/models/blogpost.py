import uuid
from app.aws.dynamodb_utils import create_blog_post_metadata, get_blog_posts_by_user, get_all_blog_posts
from app.aws.s3_utils import upload_blog_posts_to_s3, get_blog_post_from_s3

class BlogPost:
    def __init__(self, post_id, username, title, content):
        self.post_id = post_id
        self.username = username
        self.title = title
        self.content = content
    
    def save_to_db(self):
        create_blog_post_metadata(self.post_id, self.username, self.title)
        upload_blog_posts_to_s3(self.username, self.post_id, self.to_json())

    def to_json(self):
        return {
            'post_id': self.post_id,
            'username': self.username,
            'title': self.title,
            'content': self.content
        }

    def from_json(json_data):
        return BlogPost(
            post_id=json_data['post_id'],
            username=json_data['username'],
            title=json_data['title'],
            content=json_data['content']
        )
    
    @staticmethod
    def get_posts_by_user(username):
        items = get_blog_posts_by_user(username)
        posts = [BlogPost.from_json(get_blog_post_from_s3(item['username'], item['post_id'])) for item in items]
        return posts
    
    @staticmethod
    def get_all_posts():
        items = get_all_blog_posts()
        posts = [BlogPost.from_json(get_blog_post_from_s3(item['username'], item['post_id'])) for item in items]
        return posts
    
    @staticmethod
    def get_post(username, post_id):
        return BlogPost.from_json(get_blog_post_from_s3(username, post_id))