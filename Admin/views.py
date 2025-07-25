# Admin/views.py
from datetime import datetime
from flask import Blueprint, current_app, jsonify, request
from flask_restx import Api, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db
from Models.token_blacklist import TokenBlacklist
from Admin.resources.referral import ReferralManagementResource, referral_model, update_status_model
from Account.views import AdminLogin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
api = Api(admin_bp, version='1.0', title='Admin API', description='API for admin operations')

# Importer les ressources (déferer les importations problématiques)
from .resources.faq import FAQList, FAQDetail
from .resources.logout import AdminLogout
from .resources.admin import AdminList
from .resources.customer import CustomerList
from .resources.stock import StockList, StockDetail
from .resources.profile import AdminProfile
from .resources.stats import Stats, RewardsChart, StockChart, stats_ns, stats_model, rewards_chart_model, stock_chart_model
from .resources.support import SupportRequestList
from .resources.orders import AdminOrders, AdminOrderDetail, ValidateOrder, CancelOrder
from .resources.surveys import AdminSurveys, AdminSurvey, SurveyResults, SurveyResponses

# Définir les modèles pour ReferralManagementResource
referral_ns = Namespace('referrals', description='Opérations de gestion des parrainages')
referral_model_def = referral_ns.model('Referral', referral_model)
update_status_model_def = referral_ns.model('UpdateStatus', update_status_model)

# Décorer ReferralManagementResource avec les modèles
ReferralManagementResource.get = referral_ns.marshal_list_with(referral_model_def)(ReferralManagementResource.get)
ReferralManagementResource.put = referral_ns.expect(update_status_model_def)(ReferralManagementResource.put)

# Importation différée de AdminNotifications et AdminNotificationDetail
def import_notifications():
    from .resources.notifications import AdminNotifications, AdminNotificationDetail
    return AdminNotifications, AdminNotificationDetail

# Enregistrer les ressources
api.add_resource(AdminLogin, '/login')
api.add_resource(FAQList, '/faqs')
api.add_resource(AdminLogout, '/logout')
api.add_resource(FAQDetail, '/faqs/<int:faq_id>')
api.add_resource(AdminList, '/admins')
api.add_resource(CustomerList, '/customers')
api.add_resource(StockList, '/stock')
api.add_resource(StockDetail, '/stock/<int:stock_id>')
api.add_resource(AdminProfile, '/profile')
api.add_resource(Stats, '/stats')
api.add_resource(RewardsChart, '/stats/rewards-chart')
api.add_resource(StockChart, '/stats/stock-chart')
api.add_resource(SupportRequestList, '/support-requests')
api.add_resource(AdminOrders, '/orders')
api.add_resource(AdminOrderDetail, '/orders/<int:order_id>')
api.add_resource(ValidateOrder, '/orders/<int:order_id>/validate')
api.add_resource(CancelOrder, '/orders/<int:order_id>/cancel')

# Utiliser la fonction pour l'importation différée
AdminNotifications, AdminNotificationDetail = import_notifications()
api.add_resource(AdminNotifications, '/notifications')
api.add_resource(AdminNotificationDetail, '/notifications/<int:notification_id>')  # Supporte maintenant DELETE et PATCH

api.add_resource(AdminSurveys, '/surveys')
api.add_resource(AdminSurvey, '/surveys/<int:survey_id>')
api.add_resource(SurveyResults, '/surveys/<int:survey_id>/results')
api.add_resource(SurveyResponses, '/surveys/<int:survey_id>/responses')
api.add_resource(ReferralManagementResource, '/referrals', '/referrals/<int:referral_id>')