from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.blogpost import BlogPost 
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