from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.models.blogpost import BlogPost, Comment 
import uuid

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html')

@home_bp.route('/my_blogs')
@login_required
def my_blogs():
    posts = BlogPost.get_posts_by_user(current_user.username)
    return render_template('my_blogs.html', title='My Blogs', posts=posts)

########################################################################

@home_bp.route('/user_blogs/<username>')
@login_required
def user_blogs(username):
    posts = BlogPost.get_posts_by_user(username)
    return render_template('user_blogs.html', title=f'{username}\'s Blogs', posts=posts)

# @home_bp.route('/blog/<post_id>')
# def view_blog(post_id):
#     # Fetch the blog post without relying on current_user
#     blog = BlogPost.get_post_by_id(post_id)
#     if not blog:
#         return render_template('404.html'), 404
#     comments = Comment.get_comments_by_post(post_id)
#     return render_template('view_blog.html', blog=blog, comments=comments)

@home_bp.route('/blog/<post_id>', methods=['GET', 'POST'])
def view_blog(post_id):
    blog = BlogPost.get_post_by_id(post_id)
    if not blog:
        return render_template('404.html'), 404
    comments = Comment.get_comments_by_post(post_id)
    if request.method == 'POST':
        content = request.form['content']
        comment_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        comment = Comment(comment_id=comment_id, post_id=post_id, username=current_user.username, content=content, created_at=created_at)
        comment.save_to_db()
        BlogPost.add_comment(post_id, comment)
        return redirect(url_for('home_bp.view_blog', post_id=post_id))
    return render_template('view_blog.html', blog=blog, comments=comments)

@home_bp.route('/blog/<post_id>/like', methods=['POST'])
@login_required
def like_blog(post_id):
    BlogPost.add_like(current_user.username, post_id)
    #BlogPost.add_like(post_id)
    blog = BlogPost.get_post_by_id(post_id)
    return jsonify(likes=blog.likes)
    #return redirect(url_for('home_bp.view_blog', post_id=post_id))

# @home_bp.route('/blog/<post_id>/comment', methods=['POST'])
# @login_required
# def comment_blog(post_id):
#     content = request.form['content']
#     comment_id = str(uuid.uuid4())
#     created_at = datetime.utcnow().isoformat()
#     comment = Comment(comment_id=comment_id, post_id=post_id, username=current_user.username, content=content, created_at=created_at)
#     comment.save_to_db()
#     BlogPost.add_comment(post_id, comment)
#     return redirect(url_for('home_bp.view_blog', post_id=post_id))