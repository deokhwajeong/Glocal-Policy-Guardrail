"""
Monitoring and observability with Prometheus metrics
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response
import time
import functools


# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Number of active HTTP requests',
    ['method', 'endpoint']
)

COMPLIANCE_SCANS = Counter(
    'compliance_scans_total',
    'Total compliance scans performed',
    ['country', 'result']
)

REGULATORY_UPDATES = Counter(
    'regulatory_updates_total',
    'Total regulatory updates detected',
    ['country', 'source']
)

SYSTEM_ERRORS = Counter(
    'system_errors_total',
    'Total system errors',
    ['component', 'error_type']
)

UPDATE_CHECK_DURATION = Histogram(
    'update_check_duration_seconds',
    'Time taken to check regulatory updates',
    ['country']
)


def track_request_metrics(f):
    """Decorator to track request metrics"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        endpoint = f.__name__
        method = 'GET'  # Default, can be enhanced
        
        ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).inc()
        
        start_time = time.time()
        try:
            response = f(*args, **kwargs)
            status = 200 if hasattr(response, 'status_code') else 200
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            return response
        except Exception as e:
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=500).inc()
            SYSTEM_ERRORS.labels(component=endpoint, error_type=type(e).__name__).inc()
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
            ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).dec()
    
    return decorated_function


def track_compliance_scan(country, compliant):
    """Track compliance scan metrics"""
    result = 'pass' if compliant else 'fail'
    COMPLIANCE_SCANS.labels(country=country, result=result).inc()


def track_regulatory_update(country, source):
    """Track regulatory update detection"""
    REGULATORY_UPDATES.labels(country=country, source=source).inc()


def track_error(component, error):
    """Track system errors"""
    error_type = type(error).__name__
    SYSTEM_ERRORS.labels(component=component, error_type=error_type).inc()


def metrics_endpoint():
    """Endpoint to expose Prometheus metrics"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# Health check
HEALTH_STATUS = Gauge('system_health', 'System health status (1=healthy, 0=unhealthy)')
HEALTH_STATUS.set(1)  # Initially healthy


def set_health_status(healthy: bool):
    """Update system health status"""
    HEALTH_STATUS.set(1 if healthy else 0)
