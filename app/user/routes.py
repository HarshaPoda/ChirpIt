from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user import User, Follow

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.find_by_username(username)
    if not user:
        return render_template('404.html'), 404

    followers = user.get_followers()
    following = user.get_following()
    analytics = {
        'views' : 'To-Do',
        'posts' : 'To-DO'
        #'views': user.get_view_count(),
        #'posts': len(user.get_posts())
        # Add more analytics data as needed
    }
    return render_template('profile.html', user=user, followers=followers, following=following, analytics=analytics)
