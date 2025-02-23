# Performance Investigation of Various Microservice Architectures

## Project Overview

**Performance Investigation of Various Microservice Architectures** is a diploma thesis project that examines how different software architecture paradigms affect the performance of web services. It provides a comparative analysis of monolithic systems, Service-Oriented Architectures (SOA), and microservices, with a particular focus on the increasingly popular microservices approach. The project implements **five distinct microservice architectural variants** (spanning centralized orchestration and event-driven choreography patterns) and evaluates their performance under identical conditions. By stress-testing each architecture and measuring key metrics, the study highlights how design choices impact throughput, latency, scalability, and failure tolerance.

**Key findings** reveal that different architectures come with unique trade-offs. For example, an event-streaming **choreography** approach using **Redpanda** excelled at handling high-volume data, whereas a **RabbitMQ** message broker ensured stable performance under high load. Meanwhile, an **orchestrator-driven** microservices design simplified service coordination but introduced state management complexities. This research provides actionable insights for engineers selecting architecture styles based on real-world needs.

## Thesis Link

- **Full Thesis PDF:** [**Performance Investigation of Various Microservice Architectures**](documents/Performance_Investigation_of_various_Microservice_Architectures.pdf)
- **Presentation:** [**Performance Investigation of Various Microservice Architectures Presentation**](documents/Performance_Investigation_of_various_Microservice_Architectures.pptx)
- **Online Publication:** [artemis.cslab.ece.ntua.gr (NTUA Thesis Repository)](http://artemis.cslab.ece.ntua.gr:8080/jspui/handle/123456789/18763)

## Technologies & Infrastructure

This project leverages a broad set of technologies and infrastructure components:

- ![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python&logoColor=white) **Python** – Core language for implementing services and orchestrators.  
- ![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?style=flat&logo=fastapi&logoColor=white) **FastAPI** – Web framework for building RESTful API endpoints.  
- ![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=flat&logo=docker&logoColor=white) **Docker** – Containerization of all microservices for consistency and scalability.  
- ![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message_Broker-FF6600?style=flat&logo=rabbitmq&logoColor=white) **RabbitMQ** – AMQP message broker used for microservice communication.  
- ![Redpanda](https://img.shields.io/badge/Redpanda-Streaming_Platform-EE0000?style=flat&logo=red%20hat&logoColor=white) **Redpanda** – Kafka-compatible streaming platform for event-driven services.  
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=flat&logo=postgresql&logoColor=white) **PostgreSQL** – Database for storing performance test results.  
- ![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?style=flat&logo=prometheus&logoColor=white) **Prometheus** – Monitoring system for collecting performance metrics.  
- ![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?style=flat&logo=grafana&logoColor=white) **Grafana** – Dashboarding tool for real-time visualization of metrics.  
- ![Metabase](https://img.shields.io/badge/Metabase-Analytics-509EE3?style=flat&logo=metabase&logoColor=white) **Metabase** – Querying and analyzing collected test results.

## Methodology & Best Practices

- **Containerization**: Services run in isolated Docker containers for consistent deployments.
- **Monitoring**: Prometheus collects metrics, and Grafana visualizes performance in real time.
- **Performance Benchmarking**: Systematic tests ensure fair comparisons between architectures.
- **API Stress Testing**: Load tests simulate real-world traffic and measure scalability.

## Getting Started

### Prerequisites
Ensure you have **Docker** and **Docker Compose** installed before proceeding.

### Clone the Repository
```sh
git clone https://github.com/yourusername/your-repo.git  
cd your-repo
```

### Launch Infrastructure
```sh
docker compose -f deployment/docker-compose-front.yml -f deployment/docker-compose-workers.yml up -d
```

### Run a Test Scenario
To execute a performance test for a specific architecture, use:
```sh
make orchestrator
# or
make async_orchestrator
# or
make serialised_rmq
```

### Monitor Performance
- **Grafana Dashboard:** [http://localhost:3001](http://localhost:3001)  
- **Prometheus Metrics:** [http://localhost:9090](http://localhost:9090)  
- **Metabase Data Analysis:** [http://localhost:3000](http://localhost:3000)  

### Stop Services
```sh
docker compose down
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
