from extensions import db

class MyWittiClientPalierHistory(db.Model):
    __tablename__ = 'mywitti_client_palier_history'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_client.id'))
    palier = db.Column(db.String)
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    statut = db.Column(db.String)
    client = db.relationship('MyWittiClient', backref='palier_history') 