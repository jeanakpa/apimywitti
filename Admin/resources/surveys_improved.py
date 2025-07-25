# Admin/resources/surveys_improved.py
from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models.mywitti_users import MyWittiUser
from Models.mywitti_survey import MyWittiSurvey, MyWittiSurveyOption, MyWittiSurveyResponse
from Models.mywitti_client import MyWittiClient
from extensions import db
from Admin.views import api

# Modèles améliorés
survey_improved_model = api.model('SurveyImproved', {
    'id': fields.Integer(description='Survey ID'),
    'title': fields.String(description='Survey title'),
    'description': fields.String(description='Survey description'),
    'created_at': fields.String(description='Creation date'),
    'options': fields.List(fields.Nested(api.model('SurveyOptionImproved', {
        'id': fields.Integer(description='Option ID'),
        'option_text': fields.String(description='Option text'),
        'option_value': fields.Integer(description='Option value')
    })))
})

survey_improved_input_model = api.model('SurveyImprovedInput', {
    'title': fields.String(required=True, description='Titre du sondage'),
    'description': fields.String(description='Description du sondage'),
    'is_active': fields.Boolean(description='Sondage actif?', default=True),
    'options': fields.List(fields.Nested(api.model('OptionInput', {
        'option_text': fields.String(required=True, description='Texte de l\'option'),
        'option_value': fields.Integer(required=True, description='Valeur de l\'option')
    })), required=True, description='Liste des options de réponse')
})

class AdminSurveysImproved(Resource):
    @jwt_required()
    @api.expect(survey_improved_input_model)
    @api.marshal_with(api.model('SurveyImprovedResponse', {
        'msg': fields.String(description='Message de succès'),
        'survey_id': fields.Integer(description='ID du sondage')
    }), code=201)
    def post(self):
        """Créer un sondage avec des options personnalisées"""
        try:
            admin_identifiant = get_jwt_identity()
            admin = MyWittiUser.query.filter_by(user_id=admin_identifiant).first()
            if not admin or not admin.is_superuser:
                api.abort(403, "Seuls les super admins peuvent créer des sondages")
            
            data = request.get_json()
            
            # Validation
            if not data.get('title'):
                api.abort(400, "Le titre du sondage est requis")
            
            if not data.get('options') or len(data['options']) < 2:
                api.abort(400, "Au moins 2 options de réponse sont requises")
            
            # Création du sondage
            survey = MyWittiSurvey(
                title=data['title'],
                description=data.get('description', ''),
                is_active=data.get('is_active', True)
            )
            db.session.add(survey)
            db.session.flush()
            
            # Création des options personnalisées
            options = []
            for opt_data in data['options']:
                option = MyWittiSurveyOption(
                    survey_id=survey.id,
                    option_text=opt_data['option_text'],
                    option_value=opt_data['option_value']
                )
                options.append(option)
            
            db.session.add_all(options)
            db.session.commit()
            
            return {
                "msg": "Sondage créé avec succès",
                "survey_id": survey.id
            }, 201
            
        except Exception as e:
            db.session.rollback()
            api.abort(500, f"Erreur lors de la création: {str(e)}")

    @jwt_required()
    @api.marshal_with(survey_improved_model, as_list=True)
    def get(self):
        """Récupérer tous les sondages avec leurs options"""
        try:
            admin_identifiant = get_jwt_identity()
            admin = MyWittiUser.query.filter_by(user_id=admin_identifiant).first()
            if not admin or not (admin.is_admin or admin.is_superuser):
                api.abort(403, "Utilisateur non autorisé")
            
            surveys = MyWittiSurvey.query.all()
            surveys_data = []
            
            for survey in surveys:
                options = MyWittiSurveyOption.query.filter_by(survey_id=survey.id).all()
                surveys_data.append({
                    'id': survey.id,
                    'title': survey.title,
                    'description': survey.description,
                    'created_at': str(survey.created_at),
                    'options': [
                        {
                            'id': opt.id, 
                            'option_text': opt.option_text, 
                            'option_value': opt.option_value
                        } for opt in options
                    ]
                })
            
            return surveys_data
            
        except Exception as e:
            api.abort(500, f"Erreur lors de la récupération: {str(e)}")

# Enregistrement de la ressource
api.add_resource(AdminSurveysImproved, '/surveys-improved')
