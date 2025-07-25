from extensions import db
from datetime import datetime

class MyWittiSupportRequest(db.Model):
    __tablename__ = 'mywitti_support_request'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('mywitti_users.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    request_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default="Pending")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subject": self.subject,
            "description": self.description,
            "request_type": self.request_type,
            "created_at": str(self.created_at),
            "status": self.status
        }

    def __repr__(self):
        return f'<MyWittiSupportRequest {self.id} - {self.subject}>' 