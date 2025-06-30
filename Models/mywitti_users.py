from extensions import db
from datetime import datetime
from werkzeug.security import check_password_hash

class MyWittiUser(db.Model):
    __tablename__ = 'mywitti_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_type = db.Column(db.String)
    date_joined = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    must_change_password = db.Column(db.Boolean, default=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('mywitti_user_type.id'))
    email = db.Column(db.String)
    user_type_rel = db.relationship('MyWittiUserType', backref='users')
    
    def check_password(self, password):
        """Vérifie si le mot de passe fourni correspond au hash stocké"""
        return check_password_hash(self.password, password)
    
    @property
    def is_admin(self):
        """Retourne True si l'utilisateur est un admin"""
        return self.user_type in ['admin', 'superadmin'] or self.is_staff
    
    @property
    def is_superuser(self):
        """Retourne True si l'utilisateur est un super admin"""
        return self.user_type == 'superadmin' 