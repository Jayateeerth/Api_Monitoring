
from flask import Blueprint, jsonify, request

from services.log_service import fetch_logs

api_bp = Blueprint("api", __name__)


@api_bp.get("/")
def home():
    return jsonify({
        "message": "API Monitoring & Log Viewer is running"
    })


@api_bp.get("/api/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@api_bp.get("/api/orders")
def get_orders():
    # Sample endpoint for testing request monitoring.
    return jsonify({
        "orders": [
            {"id": 1, "item": "Laptop"},
            {"id": 2, "item": "Keyboard"},
        ]
    })


@api_bp.get("/api/fail")
def fail():
    # Intentionally returns an error for monitoring tests.
    return jsonify({
        "error": "This is an intentional test error"
    }), 500


@api_bp.get("/api/logs")
def logs():
    try:
        limit = request.args.get("limit", default=20, type=int)

        status_code_raw = request.args.get("status_code")
        status_code = (
            int(status_code_raw)
            if status_code_raw is not None
            else None
        )

        method = request.args.get("method")

        result = fetch_logs(
            limit=limit,
            status_code=status_code,
            method=method,
        )

        return jsonify({
            "count": len(result),
            "logs": result,
        })

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
