from flask import render_template
from app.auth import bp

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/signup')
def signup():
    return 'Signup'

@bp.route('/logout')
def logout():
    return 'Logout'