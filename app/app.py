
from flask import Flask, request
import time
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger("app")


REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency', ['endpoint'])

app = Flask(__name__)


resource = Resource(attributes={"service.name": "flask-sample-app"})
provider = TracerProvider(resource=resource)
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(span_processor)
trace.set_tracer_provider(provider)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    start = time.time()
    logger.info("Handling hello endpoint", extra={"path": "/", "method": "GET"})
    time.sleep(0.05)  
    REQUESTS.labels(method="GET", endpoint="/", http_status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    return "Hello, Observability!\n"

@app.route("/sleep/<int:ms>")
def sleepy(ms):
    start = time.time()
    logger.info("Sleep endpoint called", extra={"path": "/sleep", "ms": ms})
    time.sleep(ms / 1000.0)
    REQUESTS.labels(method="GET", endpoint="/sleep", http_status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/sleep").observe(time.time() - start)
    return f"Slept {ms} ms\n"


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
