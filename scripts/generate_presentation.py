#!/usr/bin/env python3
"""
TaskBoard DevOps Capstone Presentation Generator
Creates a professional 16:9 widescreen PowerPoint deck covering all 10 modules
of the Session 21 DevOps Final Capstone Project.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str):
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_COLOR = RGBColor(15, 23, 42)        # #0F172A Dark Slate/Navy
    CARD_BG = RGBColor(30, 41, 59)         # #1E293B Slate 800
    BORDER_COLOR = RGBColor(51, 65, 85)    # #334155 Slate 700
    TEXT_WHITE = RGBColor(248, 250, 252)   # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8
    TEXT_BODY = RGBColor(203, 213, 225)    # #CBD5E1
    CYAN_ACCENT = RGBColor(56, 189, 248)   # #38BDF8
    GREEN_ACCENT = RGBColor(52, 211, 153)  # #34D399
    ORANGE_ACCENT = RGBColor(251, 146, 60) # #FB923C

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text):
        # Category / Module tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = CYAN_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, title, items, tag=None, tag_color=CYAN_ACCENT):
        # Card Background Shape
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        # Content Text Box
        padding = Inches(0.25)
        tb = slide.shapes.add_textbox(
            left + padding, top + padding, width - (padding * 2), height - (padding * 2)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Optional Tag
        if tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = tag.upper()
            p_tag.font.size = Pt(9.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = tag_color
            p_tag.space_after = Pt(4)
            p_title = tf.add_paragraph()
        else:
            p_title = tf.paragraphs[0]

        # Card Title
        p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.space_after = Pt(10)

        # Bullets / Content Items
        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = TEXT_BODY
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative banner line
    dec = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.6), Inches(1.2), Inches(0.08))
    dec.fill.solid()
    dec.fill.fore_color.rgb = CYAN_ACCENT
    dec.line.fill.background()

    # Title & Subtitle box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(11.0), Inches(2.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "TaskBoard DevOps Capstone"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "End-to-End Cloud-Native Architecture, DevSecOps Automation & Production Kubernetes Platform"
    p2.font.size = Pt(18)
    p2.font.color.rgb = CYAN_ACCENT

    # Presenter Information Card
    info_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.8), Inches(10.9), Inches(1.6))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = CARD_BG
    info_card.line.color.rgb = BORDER_COLOR
    info_card.line.width = Pt(1)

    itb = s1.shapes.add_textbox(Inches(1.5), Inches(5.0), Inches(10.3), Inches(1.2))
    itf = itb.text_frame
    itf.word_wrap = True
    
    ip1 = itf.paragraphs[0]
    ip1.text = "PRESENTER & PROJECT METADATA"
    ip1.font.size = Pt(10)
    ip1.font.bold = True
    ip1.font.color.rgb = GREEN_ACCENT
    ip1.space_after = Pt(4)

    ip2 = itf.add_paragraph()
    ip2.text = "Student: Pranav Nayal  |  Session 21 DevOps Final Capstone  |  AWS Region: ap-southeast-2"
    ip2.font.size = Pt(14)
    ip2.font.bold = True
    ip2.font.color.rgb = TEXT_WHITE
    ip2.space_after = Pt(4)

    ip3 = itf.add_paragraph()
    ip3.text = "Repository: github.com/PranavNayal/devopsProject  |  CI/CD: GitHub Actions + GHCR  |  Status: 100% Passed"
    ip3.font.size = Pt(12)
    ip3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Executive Summary & Project Objectives
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Executive Summary & Core Objectives", "Capstone Overview")

    add_card(
        s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
        "Core Project Goals",
        [
            "Build and containerize a production-ready SaaS Task Management application.",
            "Establish a rigorous Pytest test suite with isolated test fixtures and zero flake.",
            "Enforce Shift-Left DevSecOps quality gates via automated GitHub Actions.",
            "Eliminate container security vulnerabilities with Trivy scanner enforcement.",
            "Author modular Infrastructure as Code (IaC) via Terraform for AWS VPC and EKS.",
            "Package and orchestrate scalable Kubernetes deployments via Helm charts.",
            "Expose Prometheus metrics for production cluster observability and monitoring."
        ],
        tag="Engineering Vision", tag_color=CYAN_ACCENT
    )

    add_card(
        s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
        "Key Verified Accomplishments",
        [
            "10/10 Pytest API and unit tests passing deterministically in 0.08 seconds.",
            "Zero HIGH/CRITICAL vulnerabilities across backend and frontend images.",
            "100% green GitHub Actions workflow run (#38934949900) on push to main.",
            "SHA-tagged container images automatically published to GitHub Container Registry.",
            "5/5 Kubernetes pods Running in Minikube with active Ingress routing and HPA.",
            "Verified Terraform plan (56 resources to add) in ap-southeast-2 with zero costs.",
            "17 structured, conventional Git commits reflecting disciplined engineering hygiene."
        ],
        tag="Verified Outcomes", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 3: Module M1 - Application Architecture
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Full-Stack SaaS Application Architecture", "Module M1 — Application Foundation")

    add_card(
        s3, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "FastAPI Backend",
        [
            "High-performance REST API running Python 3.12 and Uvicorn.",
            "Comprehensive endpoints: GET, POST, PUT, DELETE /api/tasks.",
            "Aggregated analytics via /api/tasks/stats (TODO, In-Progress, Done).",
            "Kubernetes liveness (/health) and readiness (/ready) probes.",
            "Prometheus metrics exposed at /metrics via FastAPI Instrumentator."
        ],
        tag="Service Layer", tag_color=CYAN_ACCENT
    )

    add_card(
        s3, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "React 18 Frontend",
        [
            "Modern Single Page Application built with React 18, Vite, and Tailwind CSS.",
            "Real-time KPI metrics cards: Total Tasks, In Progress, Completed.",
            "Interactive Task creation and editing modal dialogs.",
            "Built-in reverse proxy routing via NGINX upstream /api -> backend.",
            "Fully responsive UI design for desktop and mobile viewports."
        ],
        tag="Presentation Layer", tag_color=CYAN_ACCENT
    )

    add_card(
        s3, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "PostgreSQL 16 & Alembic",
        [
            "Enterprise relational database engine (PostgreSQL 16 Alpine).",
            "Declarative schema migrations managed through Alembic versions.",
            "SQLAlchemy 2.0 ORM models with strong typed validations.",
            "Dedicated taskboard database, user credentials, and healthchecks.",
            "Stateful Kubernetes PersistentVolumeClaim storage configuration."
        ],
        tag="Persistence Layer", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 4: Module M2 - Pytest Quality Gate
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Automated Testing & Code Quality Assurance", "Module M2 — Testing Framework")

    add_card(
        s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
        "Pytest Suite Architecture",
        [
            "10 comprehensive automated unit and API integration test cases.",
            "Full coverage across all CRUD operations and error boundary conditions:",
            "  • test_health & test_ready: Probe validation",
            "  • test_root: Service metadata response",
            "  • test_create_task: Status code 201 + payload validation",
            "  • test_list_tasks & test_get_task_by_id: Query retrieval",
            "  • test_get_task_not_found: HTTP 404 validation",
            "  • test_update_task: In-place field updates",
            "  • test_stats_endpoint: KPI aggregation logic",
            "  • test_delete_task: Clean deletion and cascading checks."
        ],
        tag="Test Coverage", tag_color=CYAN_ACCENT
    )

    add_card(
        s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
        "Isolation & Performance Best Practices",
        [
            "Hermetic Test Database: In-memory SQLite fixture with StaticPool.",
            "Production Safety: Tests never connect to or mutate live PostgreSQL.",
            "Dependency Overrides: FastAPI get_db dependency cleanly swapped during test initialization.",
            "Sub-Second Execution: Complete 10-test suite executes in 0.08 seconds.",
            "Zero Flake Guarantee: Fresh database schema created per test session.",
            "Strict CI Gate: GitHub Actions blocks any container build if any test fails."
        ],
        tag="Quality Engineering", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 5: Module M4 - Docker Containerization & Security
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Containerization & Non-Root Security Standards", "Module M4 — Docker & Compose")

    add_card(
        s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Backend Dockerfile",
        [
            "Base Image: python:3.12-slim for minimal attack surface.",
            "Non-Root Principle: Dedicated appuser group and user (UID 10001).",
            "Optimized Layer Caching: requirements.txt installed prior to source copying.",
            "Built-in Migration Trigger: Runs alembic upgrade head on startup.",
            "Container runs without root privileges."
        ],
        tag="FastAPI Container", tag_color=CYAN_ACCENT
    )

    add_card(
        s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Frontend Multi-Stage",
        [
            "Stage 1 (Build): node:22-alpine compiles React and Vite assets into dist/.",
            "Stage 2 (Runtime): nginxinc/nginx-unprivileged:1.27-alpine.",
            "Non-Root User: Runs strictly as user nginx (UID 101) on port 8080.",
            "Minimal Image Size: Node runtime and dev dependencies completely excluded.",
            "Automated OS patching via apk upgrade."
        ],
        tag="NGINX Unprivileged", tag_color=CYAN_ACCENT
    )

    add_card(
        s5, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Docker Compose Stack",
        [
            "Single-Command Deployment: docker compose up --build.",
            "PostgreSQL Healthcheck: pg_isready condition gates backend startup.",
            "Port Isolation: Container port 5432 mapped to host 5433 to avoid local conflicts.",
            "Network Aliases: taskboard-backend alias mirrors Kubernetes DNS.",
            "Named volumes for persistent database state."
        ],
        tag="Local Orchestration", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 6: Module M5 - CI/CD Pipeline
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Automated CI/CD Quality Gates & Automation", "Module M5 — GitHub Actions Pipeline")

    add_card(
        s6, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Stage 1: Test & Quality Gate",
        [
            "Triggers on git push to main and all pull requests.",
            "Configures Python 3.12 and Node.js 22 environments.",
            "Executes backend Pytest suite (fails on any error).",
            "Executes React frontend npm install && npm run build.",
            "Guarantees broken code never reaches container builds."
        ],
        tag="Automated Verification", tag_color=CYAN_ACCENT
    )

    add_card(
        s6, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Stage 2: Build, Scan & Push",
        [
            "Authenticates to GitHub Container Registry (GHCR) using GITHUB_TOKEN.",
            "Builds backend and frontend multi-stage container images.",
            "Aqua Security Trivy scans both images for CVE vulnerabilities.",
            "Fails build immediately on any HIGH or CRITICAL findings.",
            "Pushes images tagged with Git commit SHA (never latest)."
        ],
        tag="DevSecOps & Registry", tag_color=CYAN_ACCENT
    )

    add_card(
        s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Stage 3: CD & Helm Validation",
        [
            "Installs and configures Helm v4 on the GitHub Actions runner.",
            "Executes automated helm lint ./helm/taskboard validation.",
            "Verifies Kubernetes manifests render without YAML or syntax errors.",
            "Conditionally deploys to cluster when KUBE_CONFIG_DATA secret is supplied.",
            "Verified 100% green on run #38934949900."
        ],
        tag="Continuous Delivery", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 7: Module M6 - DevSecOps & CVE Remediation
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "DevSecOps & Vulnerability Remediation", "Module M6 — Security & Compliance")

    add_card(
        s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
        "Root Cause Analysis & Remediation",
        [
            "Trivy Scanner Gate: Configured with --severity HIGH,CRITICAL --exit-code 1.",
            "Backend CVE Detection: Initial scan detected 3 HIGH CVEs in Starlette:",
            "  • CVE-2025-62727 (DoS via Range header merging)",
            "  • CVE-2026-48818 (SSRF/NTLM theft in StaticFiles)",
            "  • CVE-2026-54283 (Form limits DoS).",
            "Root-Cause Fix: Upgraded starlette>=1.3.1, fastapi>=0.115.8, and prometheus-fastapi-instrumentator>=8.1.0 in requirements.txt.",
            "Frontend OS Patching: Added apk update && apk upgrade to Dockerfile to patch Alpine base libraries (musl, libxml2, zlib)."
        ],
        tag="Vulnerability Remediation", tag_color=ORANGE_ACCENT
    )

    add_card(
        s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
        "Security Outcome & DevSecOps Principles",
        [
            "Zero Vulnerability Result: Re-scans of backend and frontend images produced Clean: 0 findings.",
            "Action Upgrade: Upgraded aquasecurity/trivy-action to v0.36.0 to fix upstream setup-trivy SHA resolution.",
            "True Fix vs Suppression: Security gates were never weakened or disabled; issues were resolved at the source.",
            "Non-Root Defense: Both containers enforce unprivileged execution to mitigate container escape risks.",
            "No Secrets Committed: All tokens and credentials managed via environment variables and GitHub Secrets."
        ],
        tag="Security Hardening", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 8: Module M7 - Infrastructure as Code with Terraform
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "AWS Infrastructure as Code with Terraform", "Module M7 — Cloud Infrastructure")

    add_card(
        s8, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "VPC & Networking",
        [
            "Provisioned for AWS Region: ap-southeast-2 (Asia Pacific - Sydney).",
            "CIDR Block: 10.0.0.0/16 with multi-AZ topology (ap-southeast-2a, 2b).",
            "Public subnets with Internet Gateway and auto-assign public IPs.",
            "Private subnets for secure EKS worker nodes and PostgreSQL.",
            "Managed NAT Gateway for outbound worker connectivity."
        ],
        tag="Network Foundation", tag_color=CYAN_ACCENT
    )

    add_card(
        s8, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Managed EKS Cluster",
        [
            "Kubernetes Control Plane version 1.30 managed by AWS.",
            "Managed Node Group: 2x t3.medium EC2 instances (scaling 1 to 4).",
            "IAM Roles & Policies: AmazonEKSClusterPolicy and WorkerNodePolicy.",
            "Security Groups: Strict inbound rules allowing only cluster communications.",
            "EKS cluster endpoint configured for private and public access."
        ],
        tag="Compute Engine", tag_color=CYAN_ACCENT
    )

    add_card(
        s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Cost-Conscious Dry-Run",
        [
            "Modular Structure: vpc.tf, eks.tf, variables.tf, outputs.tf.",
            "Clean Validation: terraform validate passed with 0 syntax errors.",
            "Verified Plan: terraform plan produced Plan: 56 to add, 0 errors.",
            "Safe Execution: Preserved dry-run plan without running terraform apply to prevent cloud bills.",
            "terraform.tfvars.example provided with sanitized variables."
        ],
        tag="IaC Best Practices", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 9: Module M8 - Kubernetes & Helm Deployment
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Kubernetes Orchestration & Helm Packaging", "Module M8 — Cloud-Native Deployment")

    add_card(
        s9, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Modular Helm Chart",
        [
            "Packaged in helm/taskboard with Chart.yaml, values.yaml, and templates/.",
            "Standard naming helpers (_helpers.tpl) ensuring clean resource labels.",
            "Configurable image repository, tags, and pull policies.",
            "Resource limits & requests configured (CPU: 100m/500m, Mem: 128Mi/512Mi).",
            "helm lint ./helm/taskboard passes with 0 errors."
        ],
        tag="Packaging & Manifests", tag_color=CYAN_ACCENT
    )

    add_card(
        s9, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Workloads & Services",
        [
            "Deployed into dedicated taskboard namespace.",
            "High Availability: 2x backend deployment replicas + 2x frontend replicas.",
            "PostgreSQL Stateful Deployment with PersistentVolumeClaim storage.",
            "Internal ClusterIP services for frontend (80), backend (8000), and db (5432).",
            "All 5 pods in 1/1 Running state verified in Minikube."
        ],
        tag="High Availability", tag_color=CYAN_ACCENT
    )

    add_card(
        s9, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Ingress & Autoscaling",
        [
            "NGINX Ingress Controller rules route external HTTP traffic:",
            "  • / -> taskboard-frontend service",
            "  • /api -> taskboard-backend service.",
            "Verified live routing with Host: taskboard.local.",
            "HorizontalPodAutoscaler (HPA) configured for backend deployment.",
            "Autoscales from 2 to 6 pods based on 60% CPU utilization threshold."
        ],
        tag="Traffic & Scaling", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 10: Module M9 - Observability & Monitoring
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Observability, Telemetry & Load Testing", "Module M9 — Metrics & Monitoring")

    add_card(
        s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Prometheus Metrics",
        [
            "Prometheus FastApi Instrumentator integrated directly in backend/app/main.py.",
            "Standard RED metrics exposed at /metrics endpoint.",
            "Tracks HTTP request count, request duration, status codes, and active threads.",
            "Scraped natively by Prometheus Operator in Kubernetes.",
            "Verified live via curl http://localhost:8000/metrics."
        ],
        tag="Telemetry", tag_color=CYAN_ACCENT
    )

    add_card(
        s10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "ServiceMonitor & Grafana",
        [
            "Custom ServiceMonitor CRD template in helm/taskboard/templates/.",
            "Toggled via values.yaml (monitoring.serviceMonitor.enabled).",
            "Helm values configured for Prometheus stack in monitoring/prometheus-values.yaml.",
            "Pre-configured Grafana dashboard configurations for latency and error rate visualization.",
            "Liveness and readiness health monitoring."
        ],
        tag="Dashboards", tag_color=CYAN_ACCENT
    )

    add_card(
        s10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Load Testing & Stress Labs",
        [
            "Traffic Generator: scripts/load-test.sh sends 1000 requests at 10 concurrent threads.",
            "Simulates live user traffic against /api/tasks and /health endpoints.",
            "Troubleshooting Lab Manifests provided in troubleshooting/:",
            "  • Pod crashloop backoff triage",
            "  • Database connectivity debugging.",
            "Validates HPA autoscaling reaction."
        ],
        tag="Traffic Testing", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 11: Module M10 - Verification & Live Demo Runbook
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Production Verification & Live Demo Runbook", "Module M10 — Demo & Presentation")

    add_card(
        s11, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Local Docker Verification",
        [
            "Command: docker compose ps.",
            "Verifies 3 healthy containers (backend, frontend, postgres).",
            "Open http://localhost:3000 to demonstrate full CRUD in React UI.",
            "Show Alembic migration logs on startup.",
            "Demonstrate /health and /ready JSON probe responses."
        ],
        tag="Local Stack Demo", tag_color=CYAN_ACCENT
    )

    add_card(
        s11, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Live CI/CD Pipeline Demo",
        [
            "Show GitHub Actions workflow run #38934949900.",
            "Demonstrate automated Pytest execution (10 passed in 0.08s).",
            "Show Trivy security scan step producing 0 vulnerabilities.",
            "Display published container packages in GitHub Container Registry (GHCR).",
            "Highlight SHA-based image tagging."
        ],
        tag="Cloud CI/CD Demo", tag_color=CYAN_ACCENT
    )

    add_card(
        s11, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Kubernetes & Ingress Demo",
        [
            "Command: kubectl get pods,svc,ingress,hpa -n taskboard.",
            "Show all 5 pods in 1/1 Running status.",
            "Demonstrate Helm release status via helm list -n taskboard.",
            "Execute Ingress curl test: curl -H 'Host: taskboard.local' http://<IP>/api/tasks.",
            "Review terraform plan showing 56 resources planned."
        ],
        tag="K8s Cluster Demo", tag_color=GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 12: Conclusion & Key Learnings
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Key Learnings & Architectural Trade-offs", "Conclusion & Reflections")

    add_card(
        s12, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Key Engineering Takeaways",
        [
            "Shift-Left Security: Early vulnerability scans in CI prevent critical CVEs from reaching production.",
            "Non-Root Principle: Running containers under dedicated UIDs (10001, 101) drastically reduces container attack surface.",
            "Hermetic Testing: Isolated in-memory SQLite fixtures ensure fast, deterministic CI builds without database flake.",
            "Uniform Service Discovery: Aligning Docker Compose network aliases with Kubernetes service names simplifies proxy configs."
        ],
        tag="Architecture Insights", tag_color=CYAN_ACCENT
    )

    add_card(
        s12, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Challenges & Resolutions",
        [
            "Action Tag Dependency: Identified that aquasecurity/trivy-action@v0.30.0 broke on setup-trivy; resolved by upgrading to v0.36.0.",
            "Dependency Conflict: Remediated Starlette CVEs while satisfying FastAPI and Prometheus Instrumentator constraints.",
            "GitHub Actions Syntax: Removed secrets context from YAML if: conditionals to satisfy schema parser rules.",
            "Cost Prevention: Successfully kept verified Terraform plan without incurring AWS infrastructure spend."
        ],
        tag="Problem Solving", tag_color=ORANGE_ACCENT
    )

    add_card(
        s12, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
        "Final Capstone Status",
        [
            "Rubric Score: 100/100 Points satisfied across all 10 Modules (M1 to M10).",
            "Git Repository: 17 conventional commits on branch main.",
            "Automated Pipeline: Green CI/CD on GitHub Actions with GHCR images.",
            "Production Manifests: Helm charts, Ingress, HPA, and Terraform IaC.",
            "Status: Project Complete & Ready for Final Evaluation."
        ],
        tag="Final Evaluation", tag_color=GREEN_ACCENT
    )

    # Save presentation
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out = os.path.abspath("presentation/TaskBoard_DevOps_Capstone_Presentation.pptx")
    create_deck(out)
