from extensions import db
from models import request_logs

def save_request_log(method:str, endpoint:str, status_code:int, duration_ms: str):
    log = request_logs(
        method = method,
        endpoint= endpoint,
        status_code=status_code,
        duration_ms = duration_ms
    )

    try:
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise

    return log

def get_recent_logs(limit=20, status_code=None, method=None):
    query = db.select(request_logs)

    if status_code is not None:
        query = query.where(request_logs.status_code == status_code)

    if method:
        query = query.where(request_logs.method == method.upper())

    query = query.order_by(request_logs.id.desc()).limit(limit)

    return db.session.execute(query).scalars().all()