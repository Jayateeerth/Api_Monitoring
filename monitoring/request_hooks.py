
import time

from flask import g, request

from services.log_service import record_request


def register_request_hooks(app):

    @app.before_request
    def start_request_timer():
        # Record when the request starts.
        g.start_time = time.perf_counter()

    @app.after_request
    def log_request(response):
        # Calculate request duration in milliseconds.
        start_time = getattr(g, "start_time", None)

        if start_time is not None:
            duration_ms = (time.perf_counter() - start_time) * 1000

            try:
                record_request(
                    method=request.method,
                    endpoint=request.path,
                    status_code=response.status_code,
                    duration_ms=round(duration_ms, 2),
                )
            except Exception:
                # Logging failure should not break the API response.
                app.logger.exception("Failed to save request log")

            app.logger.info(
                "%s %s %s %.2fms",
                request.method,
                request.path,
                response.status_code,
                duration_ms,
            )

        return response
