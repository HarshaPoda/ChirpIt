import uuid
from app.aws.dynamodb_utils import (
    create_blog_post_metadata, get_blog_posts_by_user, get_all_blog_posts, 
    update_blog_post_likes, add_blog_post_comment, get_comments_for_post, get_blog_post_metadata,
    user_has_liked_post, add_user_like )
from app.aws.s3_utils import upload_blog_posts_to_s3, get_blog_post_from_s3

class BlogPost:
    def __init__(self, post_id, username, title, content,created_at, likes=0, comments=[]):
        self.post_id = post_id
        self.username = username
        self.title = title
        self.content = content
        self.created_at = created_at
        self.likes = likes
        self.comments = comments
    
    def save_to_db(self):
        create_blog_post_metadata(self.post_id, self.username, self.title, self.likes, self.comments)
        upload_blog_posts_to_s3(self.username, self.post_id, self.to_json())

    def to_json(self):
        return {
            'post_id': self.post_id,
            'username': self.username,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'likes': self.likes,
            'comments': self.comments
        }

    def from_json(json_data):
        return BlogPost(
            post_id=json_data['post_id'],
            username=json_data['username'],
            title=json_data['title'],
            content=json_data['content'],
            created_at=json_data.get('created_at', ''),
            likes=json_data.get('likes', 0),
            comments=json_data.get('comments', [])
        )
    
    @staticmethod
    def get_posts_by_user(username):
        items = get_blog_posts_by_user(username)
        posts = []
        for item in items:
            post = BlogPost.from_json(get_blog_post_from_s3(item['username'], item['post_id']))
            post.comments = Comment.get_comments_by_post(post.post_id)
            post.likes = post.likes
            posts.append(post)
        return posts
    
    @staticmethod
    def get_all_posts():
        items = get_all_blog_posts()
        posts = []
        for item in items:
            post = BlogPost.from_json(get_blog_post_from_s3(item['username'], item['post_id']))
            post.comments = Comment.get_comments_by_post(post.post_id)
            post.likes = post.likes
            posts.append(post)
        return posts
    
    @staticmethod
    def get_post_by_id(post_id):
        metadata = get_blog_post_metadata(post_id)
        if metadata:
            blog_post = BlogPost.from_json(get_blog_post_from_s3(metadata['username'], post_id))
            blog_post.comments = Comment.get_comments_by_post(post_id)
            blog_post.likes = metadata.get('likes', 0)
            return blog_post
        return None
    
    @staticmethod
    def get_post(username, post_id):
        #return BlogPost.from_json(get_blog_post_from_s3(username, post_id))
        metadata = get_blog_post_metadata(post_id)
        if metadata:
            blog_post = BlogPost.from_json(get_blog_post_from_s3(metadata['username'], post_id))
            blog_post.comments = Comment.get_comments_by_post(post_id)
            blog_post.likes = metadata.get('likes', 0)
            return blog_post
        return None
    
    
    @staticmethod
    def add_like(username, post_id):
        if not user_has_liked_post(username, post_id):
            add_user_like(username, post_id)
    
    @staticmethod
    def add_comment(post_id, comment):
        add_blog_post_comment(post_id, comment)


class Comment:
    def __init__(self, comment_id, post_id, username, content, created_at):
        self.comment_id = comment_id
        self.post_id = post_id
        self.username = username
        self.content = content
        self.created_at = created_at
    
    def to_json(self):
        return {
            'comment_id': self.comment_id,
            'post_id': self.post_id,
            'username': self.username,
            'content': self.content,
            'created_at': self.created_at
        }

    @staticmethod
    def from_json(json_data):
        return Comment(
            comment_id=json_data['comment_id'],
            post_id=json_data['post_id'],
            username=json_data['username'],
            content=json_data['content'],
            created_at=json_data['created_at']
        )
    
    @staticmethod
    def get_comments_by_post(post_id):
        items = get_comments_for_post(post_id)
        return [Comment.from_json(item) for item in items]

    def save_to_db(self):
        add_blog_post_comment(self.post_id, self)


