from extensions import db

class MyWittiCompte(db.Model):
    __tablename__ = 'mywitti_comptes'
    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String)
    agence = db.Column(db.String)
    numero_compte = db.Column(db.String)
    libelle = db.Column(db.String)
    date_ouverture_compte = db.Column(db.Date)
    working_balance = db.Column(db.BigInteger) 