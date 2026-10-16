# TaskBoard DevOps Capstone — Presentation Speaker Notes

This document provides the slide-by-slide speaker notes and demonstration walkthrough corresponding to `TaskBoard_DevOps_Capstone_Presentation.pptx`.

---

### Slide 1: Title Slide
- **Speaker Script**:  
  "Good morning/afternoon everyone. Today I am presenting my DevOps Final Capstone Project: **TaskBoard**, an end-to-end cloud-native enterprise application. Over the course of this project, I've implemented the full software delivery lifecycle—taking code from local development and automated testing through DevSecOps quality gates, container packaging, Terraform Infrastructure as Code, Kubernetes orchestration with Helm, and Prometheus observability."

---

### Slide 2: Executive Summary & Core Objectives
- **Speaker Script**:  
  "The goal of this capstone was not merely to run code, but to engineer an enterprise-grade delivery pipeline. Key verified outcomes include:
  1. A 100% Pytest pass rate executing in under 0.1 seconds.
  2. Zero HIGH or CRITICAL CVEs across all container images via Trivy scanning.
  3. A fully automated green CI/CD pipeline on GitHub Actions publishing SHA-tagged images to GHCR.
  4. A 5-pod Kubernetes deployment with Ingress routing and Horizontal Pod Autoscaling.
  5. A verified 56-resource Terraform plan for AWS VPC and EKS in ap-southeast-2."

---

### Slide 3: Full-Stack SaaS Application Architecture (Module M1)
- **Speaker Script**:  
  "At the application layer, TaskBoard is structured as a 3-tier SaaS platform:
  - **FastAPI Backend**: Uses Python 3.12 with asynchronous SQLAlchemy 2.0 and Alembic schema migrations. It exposes RESTful CRUD endpoints under `/api/tasks`, analytics at `/api/tasks/stats`, plus Kubernetes `/health`, `/ready`, and `/metrics` endpoints.
  - **React 18 Frontend**: A modern single-page dashboard styled with Tailwind CSS, displaying real-time KPI cards and task status tracking.
  - **PostgreSQL 16**: Managed through Alembic migrations to guarantee zero schema drift."

---

### Slide 4: Automated Testing & Code Quality Assurance (Module M2)
- **Speaker Script**:  
  "Testing is our first quality gate. Our Pytest suite consists of 10 comprehensive tests covering probe health, CRUD workflows, statistics aggregation, and error handling.
  Crucially, we follow the best practice of hermetic testing: we use an in-memory SQLite fixture with transactional rollbacks. This ensures tests never touch live databases, execute deterministically in 0.08 seconds, and eliminate any chance of CI build flakiness."

---

### Slide 5: Containerization & Non-Root Security Standards (Module M4)
- **Speaker Script**:  
  "In containerizing the stack, security and footprint optimization were primary concerns:
  - The backend runs on `python:3.12-slim` under a dedicated non-root user `appuser` (UID 10001).
  - The frontend uses a multi-stage build: Node 22 compiles static assets, which are copied into an unprivileged NGINX 1.27 runtime running strictly under UID 101 on port 8080.
  - Docker Compose orchestrates the entire multi-service stack with a PostgreSQL health check gate and host port isolation."

---

### Slide 6: Automated CI/CD Pipeline (Module M5)
- **Speaker Script**:  
  "Our CI/CD pipeline is implemented in GitHub Actions and runs on every push to `main`:
  - Job 1 runs backend Pytest tests and builds the frontend assets.
  - Job 2 builds the multi-stage Docker images and runs our security scanner.
  - Upon passing security gates, images are pushed to GitHub Container Registry (GHCR) tagged with the exact Git commit SHA—never the floating `latest` tag—ensuring strict auditability."

---

### Slide 7: DevSecOps & Vulnerability Remediation (Module M6)
- **Speaker Script**:  
  "Security scanning is a mandatory gate in modern engineering. We integrated Aqua Security Trivy into our pipeline with a strict `--severity HIGH,CRITICAL --exit-code 1` policy.
  When Trivy flagged 3 HIGH CVEs in Starlette and outdated Alpine OS packages, we did not bypass or suppress the check. Instead, we performed true root-cause remediation: upgrading Starlette and FastAPI to secure versions and applying Alpine security updates. Both images now pass with 0 vulnerabilities."

---

### Slide 8: AWS Infrastructure as Code with Terraform (Module M7)
- **Speaker Script**:  
  "For cloud infrastructure, we authored modular Terraform configurations parameterized for AWS Region `ap-southeast-2`:
  - It provisions a custom VPC with multi-AZ public and private subnets, an Internet Gateway, and NAT Gateway.
  - It defines a managed EKS 1.30 cluster with auto-scaling worker node groups and IAM policies.
  - We ran `terraform validate` and `terraform plan`, producing a verified plan of 56 resources to add, while consciously skipping `terraform apply` to avoid unnecessary cloud costs."

---

### Slide 9: Kubernetes Orchestration & Helm Packaging (Module M8)
- **Speaker Script**:  
  "To manage Kubernetes workloads, we built a modular Helm chart under `helm/taskboard`:
  - It deploys 2 backend replicas, 2 frontend replicas, and 1 PostgreSQL pod with PersistentVolume storage in the `taskboard` namespace.
  - An NGINX Ingress Controller routes `/` to the React frontend and `/api` to the FastAPI backend.
  - A Horizontal Pod Autoscaler (HPA) automatically scales backend pods from 2 to 6 based on CPU utilization."

---

### Slide 10: Observability, Telemetry & Load Testing (Module M9)
- **Speaker Script**:  
  "For production observability, the backend is instrumented with Prometheus FastApi Instrumentator, exposing standard RED metrics (Rate, Errors, Duration) at `/metrics`.
  Our Helm chart includes a ServiceMonitor resource for automated scraping by the Prometheus Operator, accompanied by Grafana dashboard configurations and a load testing script (`scripts/load-test.sh`) to validate real-time metrics under stress."

---

### Slide 11: Production Verification & Live Demo Runbook (Module M10)
- **Speaker Script**:  
  "During the live demo, we can verify three environments:
  1. Local Docker Compose running at `http://localhost:3000`.
  2. GitHub Actions workflow run `#38934949900` showing green quality gates and GHCR container publishing.
  3. Minikube cluster showing all 5 pods in `Running` state and Ingress successfully resolving API requests."

---

### Slide 12: Key Learnings & Conclusion
- **Speaker Script**:  
  "In conclusion, this project demonstrated key DevOps engineering tenets: Shift-Left security, defense-in-depth with non-root containers, hermetic testing, and immutable infrastructure delivery. The capstone satisfies all 10 evaluation rubrics, totaling 100/100 points. Thank you, and I am happy to take any questions."
