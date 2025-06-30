from extensions import db

class MyWittiUserType(db.Model):
    __tablename__ = 'mywitti_user_type'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String)
    description = db.Column(db.Text)
    permissions = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime) 