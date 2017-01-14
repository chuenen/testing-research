from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True)
    uid = db.Column(db.String(256), index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, index=True,
                        onupdate=datetime.utcnow)
    name = db.Column(db.String(20), index=True)
    age = db.Column(db.String(20), index=True)
    gender = db.Column(db.String(20), index=True)
    email = db.Column(db.String(64), index=True)
    profile_url = db.Column(db.String(1024), index=True)
    access_token = db.Column(db.String(1024), index=True)


class uploadFile(db.Model):
    __tablename__ = 'upload file'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_total_num = db.Column(db.Integer, index=True)
    name = db.Column(db.String(30), index=True)
    app_uid = db.Column(db.String(100), index=True)
    apk = db.Column(db.String(255), index=True)
    uid = db.Column(db.String(256), index=True)
    owner = db.Column(db.String(20), index=True)
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    intro = db.Column(db.String(1024), index=True)
    count = db.Column(db.Integer, nullable=False, default=0, index=True)
    
class Questionnaire(db.Model):
    __tablename__= 'question'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), index=True)
    app_uid = db.Column(db.String(100), index=True)
    apk = db.Column(db.String(255), index=True)
    owner = db.Column(db.String(20), index=True)
    question = db.Column(db.String(255), index=True)

class Answer(db.Model):
    __tablename__= 'answer'

    id = db.Column(db.Integer, primary_key=True, index=True)
    res_uid = db.Column(db.String(256), index=True)
    app_uid = db.Column(db.String(100), index=True)
    question = db.Column(db.String(255), index=True)
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    respondent = db.Column(db.String(20), index=True)
    age = db.Column(db.String(20), index=True)
    gender = db.Column(db.String(20), index=True)
    answer = db.Column(db.String(6), index=True)
