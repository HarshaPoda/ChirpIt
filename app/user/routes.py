from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user import User, Follow

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/<username>')
@login_required
def profile(username):
    user = User.get_user_by_username(username)
    if not user:
        return render_template('404.html'), 404
    followers = Follow.get_followers(username)
    following = Follow.get_following(username)
    is_following = any(f['followed'] == username for f in Follow.get_following(current_user.username))
    return render_template('profile.html', user=user, followers=followers, following = following, is_following=is_following)