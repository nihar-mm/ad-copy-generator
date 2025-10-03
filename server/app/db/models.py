from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
import json

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(String, primary_key=True)
    image_key = Column(String, nullable=False)
    status = Column(String, default="queued")
    params = Column(JSON, default={})
    result = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "image_key": self.image_key,
            "status": self.status,
            "params": self.params,
            "result": self.result,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }
