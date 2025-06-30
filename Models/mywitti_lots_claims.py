from extensions import db

class MyWittiLotsClaims(db.Model):
    __tablename__ = 'mywitti_lots_claims'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_client.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('mywitti_lots.id'))
    date_reclamation = db.Column(db.DateTime)
    statut = db.Column(db.String)
    client = db.relationship('MyWittiClient', backref='claims')
    lot = db.relationship('MyWittiLot', backref='claims') 