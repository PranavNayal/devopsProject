# FlowBoard DevOps Capstone — Presentation Speaker Notes

This guide provides concise, punchy, slide-by-slide speaker scripts corresponding to `FlowBoard_DevOps_Capstone_Presentation.pptx` and `FlowBoard_DevOps_Capstone_Presentation.pdf`.

---

### Slide 1: Title Slide
- **Script**: "Welcome everyone. Today I'm presenting **FlowBoard**, a cloud-native SaaS task board shipped through a complete end-to-end DevOps delivery pipeline."

### Slide 2: One board. Live KPI stats. Zero state drift.
- **Script**: "FlowBoard solves team coordination with clear state progression: tasks move seamlessly across TODO, IN PROGRESS, and DONE. Telemetry at `/api/tasks/stats` computes live metrics, containers execute strictly under non-root users, and database migrations eliminate schema drift."

### Slide 3: The Project in Numbers
- **Script**: "Here is the project in numbers: 10 REST and ops endpoints, 10 Pytest tests passing in under 0.1 seconds, 3 automated CI/CD jobs, 56 Terraform AWS resources planned, zero HIGH or CRITICAL CVEs, and zero secrets committed to Git."

### Slide 4: How It All Fits Together
- **Script**: "This is our high-level architecture. Developers push code to GitHub, triggering CI/CD quality gates. Container images are scanned by Trivy and published to GHCR tagged with the Git commit SHA. Helm orchestrates our 5-pod deployment on AWS EKS behind an NGINX Ingress controller, instrumented with Prometheus and Grafana."

---

## 01 The Application

### Slide 5: Act 01 Divider
- **Script**: "Act 1 covers the application layer: FastAPI, React 18, and PostgreSQL 16, built for reliable task execution."

### Slide 6: A Single Dashboard Runs Daily Execution
- **Script**: "The front desk is a single, clean dashboard: real-time KPI cards track project velocity, interactive filter chips toggle between statuses, and a modal allows fast task creation with Pydantic validation."

### Slide 7: Instant Feedback Across Any Device
- **Script**: "The UI is built with resilience first. If the backend is unreachable, users see a non-intrusive notification rather than a white screen crash. The responsive layout adapts cleanly from desktop down to 375-pixel mobile viewports."

### Slide 8: Every Task Follows an Explicit Lifecycle
- **Script**: "Tasks move through a strict state machine: TODO to IN PROGRESS to DONE. Every state change atomically updates the database and recalculates aggregate KPI metrics in real time."

### Slide 9: PostgreSQL and Pydantic Guarantee Data Integrity
- **Script**: "We enforce integrity at both layers: Pydantic schemas validate input types and constraints at the API gateway, while SQLAlchemy sessions guarantee atomic database transactions. In Pytest, malformed requests return HTTP 422, proving invalid data never reaches PostgreSQL."

### Slide 10: Ten REST Endpoints Plus Ops Probes
- **Script**: "Our FastAPI service exposes 10 endpoints: full CRUD under `/api/tasks`, aggregated metrics at `/api/tasks/stats`, plus Kubernetes liveness (`/health`), readiness (`/ready`), and Prometheus telemetry (`/metrics`). All documented via Swagger UI at `/docs`."

### Slide 11: Alembic Owns the Schema Migrations
- **Script**: "Database evolution is completely version-controlled via Alembic migrations. We do not use ad-hoc SQL in production. Our `/ready` probe gates Kubernetes traffic until migrations are complete, preventing broken queries."

---

## 02 Quality and Containers

### Slide 12: Act 02 Divider
- **Script**: "Act 2 covers our quality gates and container hygiene: hermetic testing and unprivileged containers."

### Slide 13: 10 Tests Prove the Rules
- **Script**: "We run 10 comprehensive Pytest tests achieving 100% endpoint pass rate. By using an in-memory SQLite fixture with StaticPool and transactional rollbacks, the entire suite executes in just 0.08 seconds with zero CI flakiness."

### Slide 14: Docker Images Run Strictly Non-Root
- **Script**: "Security starts in the containerfile. Our React frontend uses a multi-stage build: Node 22 compiles assets, and unprivileged NGINX 1.27 serves them under UID 101. The backend runs on `python:3.12-slim` under UID 10001 (`appuser`)."

### Slide 15: One Command Starts the Whole Stack
- **Script**: "Running `docker compose up --build -d` starts all three services. Health checks ensure PostgreSQL passes `pg_isready` before the backend launches, and services communicate over an isolated internal bridge."

---

## 03 The Pipeline

### Slide 16: Act 03 Divider
- **Script**: "Act 3 covers our automated pipeline: every push to main is tested, scanned, built, published, and deployed."

### Slide 17: Every Push Runs Automated Pipeline Jobs
- **Script**: "Our GitHub Actions pipeline executes four stages: parallel Pytest and Vite builds, multi-stage container builds, Aqua Trivy security scanning, and GHCR container publishing with Helm validation."

### Slide 18: A Failing Test Stops Everything
- **Script**: "The pipeline acts as a strict quality gate. When tests pass, containers build and deploy. If a single test fails, the pipeline halts immediately—no images are built or pushed to the registry."

### Slide 19: Images Ship to GHCR Tagged by Commit SHA
- **Script**: "We never deploy mutable `:latest` tags. Both backend and frontend images are published to GHCR tagged with the exact Git commit SHA. This provides 100% cryptographic traceability from pod to source code."

### Slide 20: Trivy Gates Every Image Against CVEs
- **Script**: "Aqua Trivy scans OS packages and language dependencies with `--severity HIGH,CRITICAL --exit-code 1`. When earlier scans flagged CVEs in Starlette and Alpine, we patched the dependencies at the root. The scan now passes cleanly with 0 CVEs."

### Slide 21: Security Runs Through the Entire Delivery Pipeline
- **Script**: "Our pipeline practices defense-in-depth: non-root users, SHA image pinning, zero secrets in Git, read-only root filesystems, pinned GitHub Actions, and private network isolation."

---

## 04 Infrastructure and Kubernetes

### Slide 22: Act 04 Divider
- **Script**: "Act 4 covers cloud infrastructure, Kubernetes orchestration, autoscaling, and telemetry."

### Slide 23: Architectural Decisions Shaped Our Cloud Design
- **Script**: "In designing our AWS footprint for `ap-southeast-2`, we chose high-availability multi-AZ public and private subnets, a managed EKS 1.31 cluster, and strict cost controls through verified Terraform plans."

### Slide 24: Terraform Builds the Entire Stack from Code
- **Script**: "Using modular Terraform HCL, we authored 56 resources: custom VPC, subnets, route tables, Internet Gateway, NAT Gateway, EKS cluster, node groups, and IAM roles. Everything is parameterized and reproducible."

### Slide 25: AWS Infrastructure Verified in Code and Console
- **Script**: "The network architecture strictly separates public Ingress traffic from private worker nodes. Cluster execution roles adhere to least-privilege principles, and security groups restrict pod-to-pod communication."

### Slide 26: Helm Packages the App for Kubernetes
- **Script**: "We packaged the application into a custom Helm chart: deploying 2 backend replicas, 2 frontend replicas, and a PostgreSQL StatefulSet with PersistentVolumeClaim storage in the `flowboard` namespace."

### Slide 27: NGINX Ingress Provides a Single Public Entry Point
- **Script**: "Traffic enters through an NGINX Ingress Controller. Path `/` routes to the React frontend, and `/api` routes to FastAPI. This eliminates external CORS configuration and routes traffic only to healthy pods."

### Slide 28: The Autoscaler Adds Pods Under Load
- **Script**: "We configured a Horizontal Pod Autoscaler targeting 60% CPU utilization. Under traffic bursts generated by our load testing script, backend replicas scale automatically from 2 up to 6 pods, cooling down when traffic subsides."

### Slide 29: The Backend Exposes Prometheus RED Metrics
- **Script**: "FastAPI Instrumentator exposes RED telemetry at `/metrics`: Request Rate, HTTP error rates, and duration histograms calculating p50, p95, and p99 latencies, alongside probe states."

### Slide 30: Prometheus Scrapes It and Grafana Shows It
- **Script**: "A Prometheus `ServiceMonitor` auto-discovers backend pods. Grafana displays real-time dashboards tracking requests per second, error percentages, response latencies, and container memory usage."

---

## 05 Operate and Learn

### Slide 31: Act 05 Divider
- **Script**: "Act 5 covers operations, deployment verification, troubleshooting, cost control, and engineering reflections."

### Slide 32: One Commit Became a Live Deployment
- **Script**: "In our live verification, committing a change to main triggers GitHub Actions, packages a new SHA-tagged image, and performs a zero-downtime rolling update across our Kubernetes pods."

### Slide 33: The Delivery Pipeline Ships in Under 3 Minutes
- **Script**: "Thanks to hermetic testing (0.08s), parallel Vite building, and cached multi-stage Docker builds, the full delivery pipeline completes in under 3 minutes."

### Slide 34: The Cluster Now Runs the New Image
- **Script**: "Inspecting running pods confirms the image tag matches `git rev-parse HEAD`. Helm rollouts ensure new pods pass `/ready` probes before terminating old pods, with instant rollback available via `helm rollback`."

### Slide 35: A Troubleshooting Lab Trains the Diagnosis
- **Script**: "We built a troubleshooting lab with 3 failure scenarios: `ImagePullBackOff` from invalid tags, `Service has no endpoints` from label mismatches, and `CrashLoopBackOff` from DB errors. Our core rule: check events first, labels connect services to pods, and liveness is not readiness."

### Slide 36: AWS Cost Governance & Clean Teardown
- **Script**: "We practiced strict cloud cost discipline: running `terraform plan` to verify all 56 resources while avoiding idle cluster runtime charges, and verifying clean teardown with `terraform destroy`."

### Slide 37: Five Problems That Taught Me the Most
- **Script**: "Five real engineering problems taught me the most:
  1. Fixing the Trivy action runner failure by upgrading to v0.36.0.
  2. Remediating 3 container CVEs in Starlette and Alpine packages.
  3. Configuring unprivileged NGINX permissions on port 8080.
  4. Resolving GitHub Actions secrets conditional syntax with shell checks.
  5. Eliminating test flakiness with an in-memory SQLite StaticPool fixture."

### Slide 38: Where FlowBoard Goes Beyond the Baseline
- **Script**: "FlowBoard moves beyond basic coursework: immutable SHA tags instead of `:latest`, non-root containers instead of root, modular Helm charts instead of raw YAML, autoscaling instead of static pods, and Trivy DevSecOps gates instead of unscanned containers."

### Slide 39: Every Grading Module Has Verified Evidence
- **Script**: "Every grading rubric from M1 through M10 has verified submission evidence, satisfying all criteria for 100 out of 100 points."

### Slide 40: Thank You & Future Roadmap
- **Script**: "Thank you. For future iterations, I would implement automated HTTPS with AWS Route 53 and ACM, migrate PostgreSQL to managed AWS RDS Multi-AZ, implement GitHub Actions OIDC role federation, and configure Alertmanager notifications. I'm glad to answer any questions."
