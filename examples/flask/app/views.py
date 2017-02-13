#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging, sys, os, uuid
import gender_ratio
from os.path import split, abspath, dirname
from facebook import get_user_from_cookie, GraphAPI
from flask import g, render_template, redirect, request, session, url_for, current_app, send_from_directory
from werkzeug import secure_filename
from sqlalchemy import desc, asc, and_

from app import app, db
from models import User, uploadFile, Questionnaire, Answer

# Facebook app details
FB_APP_ID = '259026017824476'
FB_APP_NAME = 'Login'
FB_APP_SECRET = '41f1497704fff159e6f6a93f6ba5fb2a'


@app.route('/')
@app.route('/<text>')
def index(text=None):
    # If a user was set in the get_current_user function before the request,
    # the user is logged in.
    charts = True if db.session.query(uploadFile).filter(uploadFile.uid == g.user['uid']).first() else False
    if g.user:
        return render_template('index.html', app_id=FB_APP_ID,
                               app_name=FB_APP_NAME, user=g.user, charts=charts, text=text)
    
    # Otherwise, a user is not logged in.
    return render_template('login.html', app_id=FB_APP_ID, name=FB_APP_NAME)


@app.route('/logout')
def logout():
    """Log out the user from the application.

    Log out the user from the application by removing them from the
    session.  Note: this does not log the user out of Facebook - this is done
    by the JavaScript SDK.
    """
    session.pop('user', None)
    return redirect(url_for('index'))


@app.before_request
def get_current_user():
    """Set g.user to the currently logged in user.

    Called before each request, get_current_user sets the global g.user
    variable to the currently logged in user.  A currently logged in user is
    determined by seeing if it exists in Flask's session dictionary.

    If it is the first time the user is logging into this application it will
    create the user and insert it into the database.  If the user is not logged
    in, None will be set to g.user.
    """


    # Set the user in the session dictionary as a global g.user and bail out
    # of this function early.
    if session.get('user'):
        g.user = session.get('user')
        return

    # Attempt to get the short term access token for the current user.
    result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)
    
    # If there is no result, we assume the user is not logged in.
    if result:
        # Check to see if this user is already in our database.

        user = User.query.filter(User.uid == result['uid']).first()
        if not user:
            # Not an existing user so get info
            graph = GraphAPI(result['access_token'])
            profile = graph.get_object('me',fields='name,age_range,email,gender,link')

            # Create the user and insert it into the database
            user = User(uid=str(profile['id']), name=profile['name'],
                        age = profile['age_range']['min'],
                        gender = profile['gender'], email = profile['email'],
                        profile_url=profile['link'],
                        access_token=result['access_token'])
            db.session.add(user)
        elif user.access_token != result['access_token']:
            # If an existing user, update the access token
            user.access_token = result['access_token']

        # Add the user to the current session
        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               uid=user.uid, access_token=user.access_token,
                               age=user.age, gender=user.gender, email=user.email)

    # Commit changes to the database and set the user as a global g.user
    db.session.commit()
    g.user = session.get('user', None)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        apk = request.files['file']
        logo = request.files['logo']
        if apk and allowed_file(apk.filename):
            intro = request.form['intro']
            appname = request.form['app']
            asks = request.form.getlist('ask')
            
            filename = secure_filename(apk.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            apk.save(path)
            
            logo_name = secure_filename(logo.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], logo_name)
            logo.save(path)
            
            app_id = uuid.uuid4()
            get_apk_profile(appname, filename, intro, app_id, logo_name)
            for ask in asks:
                if ask != '':
                    question = Questionnaire(apk=filename, app_uid=app_id, name=appname,
                                            owner=g.user['name'], owner_uid=g.user['uid'],
                                            question=ask)
                    db.session.add(question)
            db.session.commit()
            return redirect(url_for('index', text=u'成功上傳囉～'))
            #return render_template('index.html', text=u'成功上傳囉～', user=g.user)
    return render_template('upload.html')


def get_apk_profile(appname, filename, intro, app_id, logo):
    upload_num = len(db.session.query(uploadFile).filter(uploadFile.owner == g.user['name']).all()) + 1
    upload_info = uploadFile(name=appname, apk=filename, uid=g.user['uid'], owner=g.user['name'],
                             app_uid=app_id, intro=intro, user_total_num=upload_num, logo=logo)
    db.session.add(upload_info)


@app.route('/download', methods=['GET', 'POST'])
def download():
    record = db.session.query(uploadFile).order_by(desc(uploadFile.time))
    return render_template('download.html', record=record)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_apk(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/<path:image>', methods=['GET', 'POST'])
def upload_image(image):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=image)


@app.route('/questionnaire/<path:app_uid>', methods = ['GET', 'POST'])
def answer_question(app_uid):
    record = db.session.query(uploadFile).all()
    for r in record:
        condition = and_(Questionnaire.app_uid == app_uid)
        question = db.session.query(Questionnaire).filter(condition).order_by(asc(Questionnaire.id)).all()
        if request.method == 'POST':
            for q in question: 
                answer = request.form[str(q.id)]
                answer = Answer(res_uid=g.user['uid'], age=g.user['age'], gender=g.user['gender'], app_uid=q.app_uid,
                                respondent=g.user['name'], question=q.question, answer=answer, name=q.name, owner_uid=r.uid)
                db.session.add(answer)
                db.session.commit()
                return redirect(url_for('index', text=u'謝謝你完成了問卷!'))
                #return render_template('index.html', text=u'謝謝你完成了問卷!', user=g.user)
        return render_template('questionnaire.html', question=question)


@app.route('/charts/<int:uid>', methods = ['GET', 'POST'])
def get_user_file_list(uid):
    record = db.session.query(uploadFile).filter(uploadFile.uid == uid).order_by(asc(uploadFile.time)).all()
    return render_template('charts.html', record=record)


@app.route('/charts/<int:uid>/<app_uid>', methods = ['GET', 'POST'])
def get_charts(uid, app_uid):
    page = ['gender_pie_chart', 'age_line_graph', 'questionnaire_result_line_graph']
    return render_template('diagrams.html',
                           page=page,
                           data=gender_ratio.Diagram(uid, app_uid).get_data())    
