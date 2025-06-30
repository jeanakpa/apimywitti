from extensions import db

class MyWittiJetonsTransactions(db.Model):
    __tablename__ = 'mywitti_jetons_transactions'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_client.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('mywitti_lots.id'))
    montant = db.Column(db.Integer)
    motif = db.Column(db.Text)
    date_transaction = db.Column(db.DateTime)
    client = db.relationship('MyWittiClient', backref='transactions')
    lot = db.relationship('MyWittiLot', backref='transactions') 