from extensions import db

class MyWittiLot(db.Model):
    __tablename__ = 'mywitti_lots'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String)
    slug = db.Column(db.String)
    recompense_image = db.Column(db.Text)
    jetons = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('mywitti_category.id'))
    category = db.relationship('MyWittiCategory', backref='lots') 