from extensions import db
from datetime import datetime

class MyWittiSurvey(db.Model):
    __tablename__ = 'mywitti_survey'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation avec les questions
    questions = db.relationship('MyWittiSurveyQuestion', backref='survey', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Survey {self.id} - {self.title}>"

class MyWittiSurveyQuestion(db.Model):
    __tablename__ = 'mywitti_survey_question'
    id = db.Column(db.BigInteger, primary_key=True)
    survey_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_survey.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_order = db.Column(db.Integer, default=1)  # Ordre d'affichage
    is_required = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation avec les options
    options = db.relationship('MyWittiSurveyOption', backref='question', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<SurveyQuestion {self.id} - {self.question_text[:50]}...>"

class MyWittiSurveyOption(db.Model):
    __tablename__ = 'mywitti_survey_option'
    id = db.Column(db.BigInteger, primary_key=True)
    question_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_survey_question.id'), nullable=False)
    option_text = db.Column(db.String(255), nullable=False)
    option_value = db.Column(db.Integer, nullable=False)
    option_order = db.Column(db.Integer, default=1)  # Ordre d'affichage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SurveyOption {self.id} - {self.option_text}>"

class MyWittiSurveyResponse(db.Model):
    __tablename__ = 'mywitti_survey_response'
    id = db.Column(db.BigInteger, primary_key=True)
    survey_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_survey.id'), nullable=False)
    question_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_survey_question.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_users.id'), nullable=False)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_client.id'), nullable=False)
    option_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_survey_option.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    survey = db.relationship('MyWittiSurvey', backref='responses')
    question = db.relationship('MyWittiSurveyQuestion', backref='responses')
    option = db.relationship('MyWittiSurveyOption', backref='responses')
    user = db.relationship('MyWittiUser', backref='enhanced_survey_responses')
    customer = db.relationship('MyWittiClient', backref='enhanced_survey_responses')
    
    def __repr__(self):
        return f"<SurveyResponse {self.id} - Survey {self.survey_id} - Question {self.question_id}>"
