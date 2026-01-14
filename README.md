🗳️ Voting Platform – Microservices with Observability

A production-style microservices project built using Docker, Prometheus, and Grafana, demonstrating end-to-end observability with real application metrics, latency tracking, and dashboards.

This project simulates a real-world voting application and focuses heavily on DevOps best practices, especially monitoring and metrics.

📌 Project Highlights

Microservices-based architecture

Dockerized services with Docker Compose

Prometheus metrics instrumentation

Grafana dashboards for real-time observability

RED metrics (Rate, Errors, Duration)

p95 latency monitoring using histograms

Resume / interview ready DevOps project
                ┌──────────┐
                │  Client  │
                └────┬─────┘
                     │
              ┌──────▼──────┐
              │ Vote Service │  (Flask)
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │    Redis    │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │   Worker    │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │ PostgreSQL  │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │ Result Svc  │  (Flask)
              └─────────────┘

Prometheus scrapes metrics from Vote & Result services  
Grafana visualizes metrics from Prometheus

🧩 Services Breakdown
Service	Description
vote	Accepts votes (cats / dogs)
redis	Temporary vote storage
worker	Processes votes from Redis → DB
postgres	Persistent storage
result	Displays aggregated results
prometheus	Metrics collection
grafana	Visualization & dashboards

🛠️ Tech Stack
Application

Python (Flask)

Redis

PostgreSQL

DevOps / Observability

Docker

Docker Compose

Prometheus

Grafana

📂 Repository Structure
voting-platform/
├── services/
│   ├── vote/
│   ├── result/
│   └── worker/
├── monitoring/
│   └── prometheus.yml
├── compose/
│   └── docker-compose.yml
├── db-init/
│   └── init.sql
└── README.md


🚀 Getting Started
1️⃣ Clone Repository
git clone https://github.com/<your-username>/voting-platform.git
cd voting-platform/compose

2️⃣ Start the Stack
docker-compose up -d


Verify:

docker ps

🌐 Application URLs
Component	URL
Vote Service	http://localhost:5000

Result Service	http://localhost:5001

Prometheus	http://localhost:9090

Grafana	http://localhost:3000
🔐 Grafana Login
Username: admin
Password: admin

📊 Observability Setup
Prometheus Targets

Prometheus scrapes:

vote-service → /metrics

result-service → /metrics

Check:

http://localhost:9090/targets

📈 Grafana Dashboard

Dashboard Name:

Voting Platform – Observability

Panels Included
✅ Service Health

Vote Service Status (UP / DOWN)

Result Service Status (UP / DOWN)

📊 Traffic

Requests Per Second (RPS)

⏱️ Latency

p95 latency using Prometheus histogram

🗳️ Business Metrics

Votes received (Cats vs Dogs)

🔍 Key PromQL Queries Used
Service Health
up{job="vote-service"}

Requests Per Second
sum(rate(vote_service_requests_total[1m]))

p95 Latency
histogram_quantile(
  0.95,
  sum by (le) (
    rate(vote_request_latency_seconds_bucket[5m])
  )
)

Votes Received
votes_received_total

🧪 Testing the System
Send Votes (PowerShell)
iwr http://localhost:5000/vote `
-Method POST `
-Headers @{ "Content-Type"="application/json" } `
-Body '{"vote":"cats"}'

Stop Service to Test Alerts / Status
docker stop compose-vote-1


Dashboard will show DOWN automatically.

🎯 What This Project Demonstrates

Real microservices communication

Metrics instrumentation at code level

Prometheus histogram usage

Production-grade Grafana dashboards

Docker networking & service discovery

Observability-first DevOps mindset

📌 Resume Bullet Points (You can copy)

Designed and deployed a Dockerized microservices voting platform with Redis, PostgreSQL, and background workers

Implemented Prometheus-based metrics collection including custom business and latency metrics

Built Grafana dashboards visualizing service health, RPS, and p95 latency using histogram quantiles

Implemented RED metrics and real-time observability for troubleshooting and performance analysis

Used Docker Compose for local orchestration and service discovery

🔮 Future Enhancements

Grafana alerts (Slack / Email)

Kubernetes deployment (EKS / Minikube)

GitOps with ArgoCD

Terraform-based infrastructure

Service Mesh (Istio / Linkerd)

Chaos testing & SRE practices

👤 Author

Rajaneesh
DevOps / Cloud / Platform Engineer
(Project built as part of hands-on DevOps learning)
