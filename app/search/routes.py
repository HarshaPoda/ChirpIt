from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User, Follow
import boto3
from app.aws.dynamodb_utils import get_dynamodb_client, create_user


search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        dynamodb = get_dynamodb_client()
        table = dynamodb.Table('Users')
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('username').contains(search_term)
        )
        results = [User(item['username'], item['email'], item['password_hash']) for item in response['Items']]
        return render_template('search_results.html', results=results)
    return render_template('search.html')

@search_bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    followed = User.get_user_by_username(username)
    if not followed:
        flash('User not found. ', 'danger')
        return redirect(url_for('search_bp.search'))
    if followed.username == current_user.username:
        flash('You cannot follow yourself! :)', 'danger')
        return redirect(url_for('search_bp.search'))
    Follow.add_follow(current_user.username, followed.username)
    flash(f'You have requested to follow {followed.username}', 'success')
    return redirect(url_for('search_bp.profile'))

@search_bp.route('/accept_follow/<follower>', methods=['POST'])
@login_required
def accept_follow(follower):
    Follow.accept_follow(follower, current_user.username)
    flash(f"You have accepted the follow request from {follower}", 'success')
    return redirect(url_for('user_bp.profile', username=current_user.username))