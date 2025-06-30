from extensions import db

class MyWittiCategory(db.Model):
    __tablename__ = 'mywitti_category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    slug = db.Column(db.String)
    description = db.Column(db.Text)
    categ_points = db.Column(db.Integer)
    recompense_point = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    level = db.Column(db.Integer)
    min_jetons = db.Column(db.BigInteger)
    nb_jours = db.Column(db.Integer) 