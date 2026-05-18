# Online Cosmetics Store SRE Project

## Project Overview

This project is an end-term Site Reliability Engineering implementation for an online cosmetics store. The system is built as a distributed microservices application and demonstrates containerization, monitoring, orchestration, infrastructure provisioning, automation, incident response, and capacity planning.

The project includes a React frontend served by Nginx, six backend microservices, PostgreSQL, Redis, Prometheus, Grafana, cAdvisor, Docker Compose, Docker Swarm, Kubernetes, Terraform, and Ansible.

## Architecture

```text
User
|
React Frontend served by Nginx
|
Nginx API Gateway
|
+------------------------------------------------+
|                 Microservices                  |
|------------------------------------------------|
| Auth | Product | Order | Payment               |
| Notification | Review                          |
+------------------------------------------------+
|
PostgreSQL / Redis

Monitoring:
Prometheus → Grafana
cAdvisor → Prometheus → Grafana

Infrastructure:
Terraform → VM provisioning simulation

Configuration:
Ansible → Setup & deployment validation

Orchestration:
Docker Compose → Local deployment
Docker Swarm → Stack deployment and service replication
Kubernetes → Pods, Deployments, Services, ConfigMaps, and HPA