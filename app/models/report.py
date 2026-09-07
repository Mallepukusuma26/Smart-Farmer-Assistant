from datetime import datetime
from app.extensions import db

class Report(db.Model):
    """Generated PDF / CSV reports registry entity."""
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False) # Soil Analysis, Crop Recommendation, Irrigation, Disease, Yield, Financial, Full Farm
    title = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_format = db.Column(db.String(10), default='pdf')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'report_type': self.report_type,
            'title': self.title,
            'file_path': self.file_path,
            'file_format': self.file_format,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self):
        return f"<Report id={self.id} title='{self.title}'>"
