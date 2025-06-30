from extensions import db

class MyWittiClient(db.Model):
    __tablename__ = 'mywitti_client'
    id = db.Column(db.BigInteger, primary_key=True)
    customer_code = db.Column(db.String)
    short_name = db.Column(db.String)
    first_name = db.Column(db.String)
    gender = db.Column(db.String)
    birth_date = db.Column(db.Date)
    phone_number = db.Column(db.String)
    street = db.Column(db.String)
    jetons = db.Column(db.BigInteger)
    date_ouverture = db.Column(db.String)
    nombre_jours = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('mywitti_category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('mywitti_users.id'))
    category = db.relationship('MyWittiCategory', backref='clients')
    user = db.relationship('MyWittiUser', backref='clients') 