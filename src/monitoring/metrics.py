from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Prometheus System & ML Metrics
REQUEST_COUNT = Counter('recommendation_requests_total', 'Total recommendation requests', ['model_type'])
REQUEST_LATENCY = Histogram('recommendation_request_latency_seconds', 'Latency of recommendation request in seconds')
ERROR_COUNT = Counter('recommendation_errors_total', 'Total recommendation errors', ['error_type'])
MODEL_LOAD_TIME = Gauge('model_load_duration_seconds', 'Time taken to load ML model checkpoints')
ACTIVE_USERS = Gauge('recommendation_active_users', 'Number of unique users served in current session')

def get_latest_metrics():
    return generate_latest(), CONTENT_TYPE_LATEST
