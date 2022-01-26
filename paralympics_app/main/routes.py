import os
from pathlib import Path

import pandas as pd
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from paralympics_app import photos, db
from paralympics_app.main.forms import ProfileForm, CompetitionForm
from paralympics_app.models import Profile, Region, User, CompetitionEntry

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    images = get_logos()
    return render_template('index.html', title='Home page', images=images)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('main.update_profile'))
    else:
        return redirect(url_for('main.create_profile'))


@main_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    form.region_id.choices = [(r.id, r.region) for r in Region.query.order_by('region')]
    print(len(form.region_id.choices))
    if request.method == 'POST' and form.validate_on_submit():
        filename = None
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                filename = photos.save(request.files['photo'])
        p = Profile(region_id=form.region_id.data, username=form.username.data, photo=filename, bio=form.bio.data,
                    user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.display_profiles', username=p.username))
    return render_template('profile.html', form=form)


@main_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User, User.id == Profile.user_id).filter_by(id=current_user.id).first()
    form = ProfileForm(obj=profile)
    form.region_id.choices = [(r.id, r.region) for r in Region.query.order_by('region')]
    if request.method == 'POST' and form.validate_on_submit():
        # TODO: modify so that if the username is unchanged, ignore on validation and don't update
        if 'photo' in request.files:
            file = photos.save(request.files['photo'])
            profile.photo = file
        profile.region = form.region_id.data
        profile.bio = form.bio.data
        profile.username = form.username.data
        db.session.commit()
        return redirect(url_for('main.display_profiles', username=profile.username))
    return render_template('profile.html', form=form, photo_filename=profile.photo)


@main_bp.route('/display_profiles', methods=['POST', 'GET'], defaults={'username': None})
@main_bp.route('/display_profiles/<username>/', methods=['POST', 'GET'])
@login_required
def display_profiles(username):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("main.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("Username not found.")
        return redirect(url_for("main.index"))
    filenames = []
    for result in results:
        if result.photo:
            filename = result.photo
            filenames.append(filename)
    return render_template('display_profile.html', profiles=zip(results, filenames))


@main_bp.route('/competition', methods=['POST', 'GET'])
def competition():
    comp_form = CompetitionForm(request.form)
    if request.method == 'POST' and comp_form.validate_on_submit():
        if current_user:
            entry = CompetitionEntry(q1=comp_form.q1.data, q2=comp_form.q2.data, user_id=current_user.id)
        else:
            entry = CompetitionEntry(q1=comp_form.q1.data, q2=comp_form.q2.data)
        try:
            db.session.add(entry)
            db.session.commit()
            flash("Competition entry saved.")
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Error, competition entry not saved. Please try again.', 'error')
            return redirect(url_for('main.competition'))
    return render_template('competition.html', title='Competition', form=comp_form)


def get_logos():
    """
    Checks the logos directory and returns a list information about the logos for each paralympics
    :return: images: A list with the logo file name, year and event name for each paralympic event
    """
    img_list = []
    # TODO: Consider using context with url_for() instead of Path
    img_directory = Path(__file__).parent.parent.joinpath('static', 'images', 'logos')
    for filename in os.listdir(img_directory):
        img_list.append(filename)
    img_df = pd.DataFrame(img_list, columns=['filename'])
    img_df['year'] = img_df['filename'].str[:4]
    img_df['event'] = img_df['filename'].str[5:-4]
    img_df.sort_values(by=['year'], inplace=True)
    img_df.reset_index(inplace=True, drop=True)
    images = img_df.values.tolist()
    return images
