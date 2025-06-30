from extensions import db

class MyWittiClientJetonsDaily(db.Model):
    __tablename__ = 'mywitti_client_jetons_daily'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.BigInteger, db.ForeignKey('mywitti_client.id'))
    date_jour = db.Column(db.Date)
    solde_jetons = db.Column(db.BigInteger)
    client = db.relationship('MyWittiClient', backref='jetons_daily') 