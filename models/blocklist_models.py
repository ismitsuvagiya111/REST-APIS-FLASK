
from db import db


class BlocklistModel(db.Model):
    __tablename__ = "blocklist"
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
