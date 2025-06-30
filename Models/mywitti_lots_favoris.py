from extensions import db

class MyWittiLotsFavoris(db.Model):
    __tablename__ = 'mywitti_lots_favoris'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_client.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('mywitti_lots.id'))
    date_ajout = db.Column(db.DateTime)
    client = db.relationship('MyWittiClient', backref='favoris')
    lot = db.relationship('MyWittiLot', backref='favoris') 