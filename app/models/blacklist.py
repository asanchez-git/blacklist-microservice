from datetime import datetime, timezone
from app import db


class Blacklist(db.Model):
    __tablename__ = "blacklists"
    __table_args__ = (
        db.UniqueConstraint("email", "app_uuid", name="uq_blacklist_email_app"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))