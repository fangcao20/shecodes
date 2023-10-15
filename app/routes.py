from datetime import datetime

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post, Hashtag


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data,
                    phone_number=form.phone_number.data, work_place=form.work_place.data, description=form.description.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username.data) | (User.email == form.username.data) | (User.phone_number == form.username.data)).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Đăng nhập', form=form)


@app.route('/')
def index():
    return render_template('index.html', title='Trang chủ')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    return render_template('user.html', user=user, posts=posts)


@app.route('/create_post', methods=['POST'])
def create_post():
    post_title = request.form['title']
    post_content = request.form['post_content']
    p = Post(content=post_content, user_id=current_user.id, title=post_title)
    hashtag = request.form['hashtag']
    hashtags = hashtag.split(' ')
    for h in hashtags:
        if not Hashtag.query.filter_by(content=h).first():
            ht = Hashtag(content=h)
            db.session.add(ht)
        else:
            ht = Hashtag.query.filter_by(content=h).first()
        p.hashtags.append(ht)
    db.session.add(p)
    db.session.commit()
    posts = []
    posts_db = Post.query.filter_by(username=current_user.username).order_by(Post.timestamp).desc()
    for p in posts_db:
        posts.append(p.to_dict())
    return jsonify(posts=posts)


@app.route('/sponsors')
def sponsors():
    sponsors = User.query.filter(User.role == "Nhà hảo tâm").all()
    return render_template('sponsors.html', sponsors=sponsors)


@app.route('/projects')
def projects():
    hashtags = Hashtag.query.all()
    posts = Post.query.all()
    return render_template('projects.html', hashtags=hashtags, posts=posts)


@app.route('/get_posts', methods=['POST'])
def get_posts():
    hashtag_id = request.form['hashtag_id']
    h = Hashtag.query.get(int(hashtag_id))
    posts = []
    for p in h.posts:
        posts.append(p.to_dict())
    return jsonify(posts=posts)
