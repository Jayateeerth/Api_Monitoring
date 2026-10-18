
from repositories.log_repository import (
    save_request_log,
    get_recent_logs
)


def record_request(method, endpoint, status_code, duration_ms):
    """Save details of a completed API request."""
    return save_request_log(
        method=method,
        endpoint=endpoint,
        status_code=status_code,
        duration_ms=duration_ms,
    )


def fetch_logs(limit=20, status_code=None, method=None):
    """Validate filters and retrieve recent request logs."""

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100")

    if status_code is not None and not 100 <= status_code <= 599:
        raise ValueError("Status code must be between 100 and 599")

    if method:
        method = method.strip().upper()

        allowed_methods = {"GET", "POST", "PUT", "PATCH", "DELETE"}
        if method not in allowed_methods:
            raise ValueError("Unsupported HTTP method")

    logs = get_recent_logs(
        limit=limit,
        status_code=status_code,
        method=method,
    )

    return [log.to_dict() for log in logs]
