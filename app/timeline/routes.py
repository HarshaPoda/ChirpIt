from flask import Blueprint, render_template, current_app
from app.models.blogpost import BlogPost

timeline_bp = Blueprint('timeline_bp', __name__)


@timeline_bp.route('/timeline')
def timeline():
    posts = BlogPost.get_all_posts()
    return render_template('timeline.html', title='Timeline', blogs=posts)
