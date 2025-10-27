# Complete Observability System (Metrics, Logs & Traces)

## Objective
An integrated monitoring system with:
- **Prometheus** for metrics
- **Loki** for logs
- **Jaeger** for tracing
- **Grafana** dashboards for visualization

##  Tools Used
- Docker & Docker Compose  
- Prometheus  
- Grafana  
- Loki  
- Jaeger  
- Flask (Python)

##  Setup
1. Clone this repository  
   ```bash
   git clone https://github.com/<your-username>/observability-project.git
   cd observability-project
2.Build and start all containers*
  ```bash
  docker-compose up --build

## Access UIs:
- App → http://localhost:5000
- Prometheus → http://localhost:9090
- Grafana → http://localhost:3000
- Jaeger → http://localhost:16686

