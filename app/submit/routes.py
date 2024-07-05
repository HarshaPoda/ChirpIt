from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from app.aws.s3_utils import get_s3_client, upload_blog_posts_to_s3
from botocore.exceptions import ClientError
from app.models.blogpost import BlogPost
from flask_login import login_required, current_user
import json
import uuid

submit_bp = Blueprint('submit_bp', __name__)

@submit_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if not current_user.is_authenticated:
        return render_template('login_prompt.html', title="Login Required")
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        #blog_id = blog_title
        post_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        blog_post=BlogPost(post_id=post_id,username=current_user.username, title=blog_title, content=blog_content, created_at=created_at)
        blog_post.save_to_db()
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('home_bp.my_blogs'))
    return render_template('submit.html', title='Submit Blog')
