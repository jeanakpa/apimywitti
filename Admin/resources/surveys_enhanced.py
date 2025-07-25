# Admin/resources/surveys_enhanced.py
from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models.mywitti_users import MyWittiUser
from Models.mywitti_survey import MyWittiSurvey, MyWittiSurveyOption
from extensions import db
from Admin.views import api

# Modèles pour l'API améliorée
question_model = api.model('Question', {
    'question_text': fields.String(required=True, description='Texte de la question'),
    'options': fields.List(fields.Nested(api.model('QuestionOption', {
        'option_text': fields.String(required=True, description='Texte de l\'option'),
        'option_value': fields.Integer(required=True, description='Valeur de l\'option')
    })), required=True, description='Liste des options de réponse')
})

survey_enhanced_input_model = api.model('SurveyEnhancedInput', {
    'title': fields.String(required=True, description='Titre du sondage'),
    'description': fields.String(description='Description du sondage'),
    'questions': fields.List(fields.Nested(question_model), required=True, description='Liste des questions')
})

survey_enhanced_response_model = api.model('SurveyEnhancedResponse', {
    'id': fields.Integer(description='Survey ID'),
    'title': fields.String(description='Survey title'),
    'description': fields.String(description='Survey description'),
    'created_at': fields.String(description='Creation date'),
    'questions': fields.List(fields.Nested(api.model('QuestionResponse', {
        'id': fields.Integer(description='Question ID'),
        'question_text': fields.String(description='Question text'),
        'options': fields.List(fields.Nested(api.model('OptionResponse', {
            'id': fields.Integer(description='Option ID'),
            'option_text': fields.String(description='Option text'),
            'option_value': fields.Integer(description='Option value')
        })))
    })))
})

class AdminSurveysEnhanced(Resource):
    @jwt_required()
    @api.expect(survey_enhanced_input_model)
    @api.marshal_with(api.model('SurveyEnhancedCreateResponse', {
        'msg': fields.String(description='Success message'),
        'survey_id': fields.Integer(description='Survey ID')
    }), code=201)
    def post(self):
        """Créer un sondage avec plusieurs questions"""
        try:
            # Vérification des autorisations admin
            admin_identifiant = get_jwt_identity()
            admin = MyWittiUser.query.filter_by(user_id=admin_identifiant).first()
            if not admin or not admin.is_superuser:
                api.abort(403, "Seuls les super admins peuvent créer des sondages")
            
            data = request.get_json()
            
            # Validation des données
            if not data.get('title'):
                api.abort(400, "Le titre du sondage est requis")
            
            if not data.get('questions') or len(data['questions']) == 0:
                api.abort(400, "Au moins une question est requise")
            
            # Création du sondage
            survey = MyWittiSurvey(
                title=data['title'],
                description=data.get('description', ''),
                is_active=True
            )
            db.session.add(survey)
            db.session.flush()  # Pour obtenir l'ID du sondage
            
            # Création des questions et options
            for question_data in data['questions']:
                if not question_data.get('question_text'):
                    continue
                
                if not question_data.get('options') or len(question_data['options']) == 0:
                    continue
                
                # Création de la question
                question = MyWittiSurveyQuestion(
                    survey_id=survey.id,
                    question_text=question_data['question_text'],
                    question_order=len(survey.questions) + 1
                )
                db.session.add(question)
                db.session.flush()
                
                # Création des options pour cette question
                for option_data in question_data['options']:
                    if not option_data.get('option_text'):
                        continue
                    
                    option = MyWittiSurveyOption(
                        question_id=question.id,
                        option_text=option_data['option_text'],
                        option_value=option_data.get('option_value', 0),
                        option_order=len(question.options) + 1
                    )
                    db.session.add(option)
            
            db.session.commit()
            
            return {
                "msg": "Sondage multi-questions créé avec succès",
                "survey_id": survey.id
            }, 201
            
        except Exception as e:
            db.session.rollback()
            api.abort(500, f"Erreur lors de la création du sondage: {str(e)}")

    @jwt_required()
    @api.marshal_with(survey_enhanced_response_model, as_list=True)
    def get(self):
        """Récupérer tous les sondages avec leurs questions"""
        try:
            # Vérification des autorisations admin
            admin_identifiant = get_jwt_identity()
            admin = MyWittiUser.query.filter_by(user_id=admin_identifiant).first()
            if not admin or not (admin.is_admin or admin.is_superuser):
                api.abort(403, "Utilisateur non autorisé")
            
            surveys = MyWittiSurvey.query.all()
            surveys_data = []
            
            for survey in surveys:
                survey_data = {
                    'id': survey.id,
                    'title': survey.title,
                    'description': survey.description,
                    'created_at': str(survey.created_at),
                    'questions': []
                }
                
                # Récupération des questions triées par ordre
                questions = MyWittiSurveyQuestion.query.filter_by(survey_id=survey.id).order_by(MyWittiSurveyQuestion.question_order).all()
                
                for question in questions:
                    question_data = {
                        'id': question.id,
                        'question_text': question.question_text,
                        'options': []
                    }
                    
                    # Récupération des options triées par ordre
                    options = MyWittiSurveyOption.query.filter_by(question_id=question.id).order_by(MyWittiSurveyOption.option_order).all()
                    
                    for option in options:
                        question_data['options'].append({
                            'id': option.id,
                            'option_text': option.option_text,
                            'option_value': option.option_value
                        })
                    
                    survey_data['questions'].append(question_data)
                
                surveys_data.append(survey_data)
            
            return surveys_data
            
        except Exception as e:
            api.abort(500, f"Erreur lors de la récupération des sondages: {str(e)}")

# Enregistrement de la ressource
api.add_resource(AdminSurveysEnhanced, '/surveys-enhanced')
