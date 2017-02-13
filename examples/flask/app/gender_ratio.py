from app import app, db
from sqlalchemy import asc
from .models import Answer, Questionnaire
import logging

class Diagram():
    def __init__(self, uid, app_uid):
        answer_batch = db.session.query(Answer).filter(Answer.owner_uid==uid, Answer.app_uid==app_uid).all()
        question_batch = db.session.query(Questionnaire).filter(Questionnaire.owner_uid==uid, Questionnaire.app_uid==app_uid) \
                                                        .order_by(asc(Questionnaire.id)).all()
        female, male = 0, 0
        length = float(len(answer_batch))
        self.data = {'w_age': {'14 -': 0, '15-24': 0,'25-34': 0, '35-44': 0, '45-54': 0, '55-64': 0, '65 +': 0},
                     'm_age': {'14 -': 0, '15-24': 0,'25-34': 0, '35-44': 0, '45-54': 0, '55-64': 0, '65 +': 0}}
       
        result = {'great': {}, 'smile': {}, 'meh': {}, 'frown': {}, 'worse': {}}
        question = [row.question for row in question_batch]

        self.data['satisfaction'] = {}
        self.data['question'] = sorted(question) 
        for r in result:
            for q in self.data['question']:
                if q not in result[r]:
                    result[r][q] = 0

        for row in answer_batch:
            for q in self.data['question']:
                if q == row.question:
                    result[row.answer][q] += 1
            if row.gender == 'female':
                female += 1
                self.get_woman_age_num(int(row.age))
            else:
                male += 1
                self.get_man_age_num(int(row.age))
        self.data['female'] = (female / length) * 100
        self.data['male'] = (male / length) * 100
         
        for r in result: 
            self.data['satisfaction'][r] = [[key, value] for key, value in sorted(result[r].items())]
        

    def get_woman_age_num(self, age):
        logging.info(type(age))
        if age <= 14:
            self.data['w_age']['14 -'] += 1
        elif 15 <= age < 25:
            self.data['w_age']['15-24'] += 1
        elif 25 <= age < 35:
            self.data['w_age']['25-34'] += 1
        elif 35 <= age < 45:
            self.data['w_age']['35-44'] += 1
        elif 45 <= age < 55:
            self.data['w_age']['45-54'] += 1
        elif 55 <= age < 65:
            self.data['w_age']['55-64'] += 1
        else:
            self.data['w_age']['65 +'] += 1

    def get_man_age_num(self, age):
        if age <= 14:
            self.data['m_age']['14 -'] += 1
        elif 15 <= age < 25:
            self.data['m_age']['15-24'] += 1
        elif 25 <= age < 35:
            self.data['m_age']['25-34'] += 1
        elif 35 <= age < 45:
            self.data['m_age']['35-44'] += 1
        elif 45 <= age < 55:
            self.data['m_age']['45-54'] += 1
        elif 55 <= age < 65:
            self.data['m_age']['55-64'] += 1
        else:
            self.data['m_age']['65 +'] += 1


    def get_data(self):
        return self.data
