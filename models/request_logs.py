from datetime import datetime , timezone

from extensions import db


class request_logs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    method = db.Column(db.String(10), nullable= False)
    endpoint = db.Column(db.String(255), nullable = False)
    status_code =  db.Column(db.Integer, nullable = False)
    duration_ms = db.Column(db.Float , nullable = False)
    timestamp = db.Column(
        db.DateTime(timezone=True),
        default= lambda: datetime.now(timezone.utc),
        nullable = False,
    )

    def to_dict(self):
        return {
            "id":self.id,
            "method":self.method,
            "endpoint":self.endpoint,
            "status_code" : self.status_code,
            "duration_ms": self.duration_ms,
            "timestamp":self.timestamp.isoformat()
        }