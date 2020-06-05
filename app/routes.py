import os
import secrets
from datetime import datetime, date
from flask import render_template, flash, url_for, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, bcrypt
from app.forms import LoginForm, UploadForm
from app.models import User, Video
import requests
import secrets
import re


@app.route('/')
def index():
    videos = Video.query.order_by(Video.modified_time.desc()).all()
    return render_template("index.html", title="Home Page", videos=videos)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    videos = Video.query.order_by(Video.modified_time.desc()).filter_by(
        user_id=current_user.id).all()
    form = UploadForm()

    if form.validate_on_submit():

        match = re.search(r"youtube\.com/.*v=([^&]*)", form.video_link.data)
        video_id_youtube = match.group(1)

        image_url = "https://img.youtube.com/vi/" + \
            video_id_youtube + "/mqdefault.jpg"
        img_data = requests.get(image_url).content
        random_hex = secrets.token_hex(16)
        thumb_filename = random_hex + ".jpg"

        with open(current_app.root_path + '/static/thumbs/' + thumb_filename, 'wb') as handler:
            handler.write(img_data)

        uploaded_video = Video(video_title=form.video_title.data, video_thumb=thumb_filename,
                               video_link=form.video_link.data, video_description=form.video_description.data, user_id=current_user.id)

        # saving to database
        db.session.add(uploaded_video)
        db.session.commit()
        flash('Video uploaded successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', title='Dashboard', videos=videos, form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if user already logged in, lets redirect them to their account page
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    # creating the login form object
    form = LoginForm()
    if form.validate_on_submit():
        # make sure the user exists in database
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # this will do the whole user session for us
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Username or Password Error!', 'danger')
    return render_template('login.html', title="User Login", form=form)


@app.route('/register')
def register():
    flash('This feature is not available right now!', 'danger')
    return redirect(url_for('index'))


# now let's logout the user
@app.route('/logout')
def logout():
    # redirect user who not logged in but try to logout
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    # if logged in then logout him
    logout_user()
    flash('You have been logged out!', 'warning')
    return redirect(url_for('index'))


@app.route('/video/view/<int:video_id>')
def view_video(video_id):
    video = Video.query.get_or_404(video_id)

    match = re.search(r"youtube\.com/.*v=([^&]*)", video.video_link)
    video_id = match.group(1)

    return render_template('video.html', title=video.video_title, video=video, video_id=video_id)


@app.route('/video/edit/<int:video_id>', methods=['GET', 'POST'])
def edit_video(video_id):
    video = Video.query.get_or_404(video_id)

    if not video.user_id == current_user.id:
        flash('You are not allowed to view this page!', 'danger')
        return redirect(url_for('dashboard'))

    form = UploadForm()

    if form.validate_on_submit():

        match = re.search(r"youtube\.com/.*v=([^&]*)", form.video_link.data)
        video_id_youtube = match.group(1)

        image_url = "https://img.youtube.com/vi/" + \
            video_id_youtube + "/mqdefault.jpg"
        img_data = requests.get(image_url).content
        random_hex = secrets.token_hex(16)
        thumb_filename = random_hex + ".jpg"

        with open(current_app.root_path + '/static/thumbs/' + thumb_filename, 'wb') as handler:
            handler.write(img_data)

        video.video_title = form.video_title.data
        video.video_thumb = thumb_filename
        video.video_link = form.video_link.data
        video.video_description = form.video_description.data
        video.modified_time = datetime.now()

        # saving to database
        db.session.commit()
        flash('Video updated successfully', 'success')
        return redirect(url_for('dashboard'))

    elif request.method == 'GET':
	    form.video_title.data = video.video_title
	    form.video_link.data = video.video_link
	    form.video_description.data = video.video_description

    return render_template('edit-video.html', title=video.video_title, form=form, video=video, video_id=video_id)
