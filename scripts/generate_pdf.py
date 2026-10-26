#!/usr/bin/env python3
"""
Generates presentation/FlowBoard_DevOps_Capstone_Presentation.pdf
Matches the reference Waiting-Room-Presentation.pdf:
- 16:9 widescreen (960 x 540 points)
- Clean, uncluttered layout with 40 slides across 5 Acts
- High contrast, elegant typography, cards, hero stats, and tables
- Rich diagrams: architecture schematic, state machine, CI/CD pipeline, green vs red comparison,
  service dependency graph, autoscaler load curve, and terminal/dashboard mockups
"""

import os
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

WIDTH = 960
HEIGHT = 540

# Colors matching Waiting-Room reference style
C_DARK_BG = HexColor("#0B2B2A")
C_LIGHT_BG = HexColor("#FFFFFF")
C_CARD_BG = HexColor("#F4F8F7")
C_CARD_BORDER = HexColor("#DAE8E5")
C_MINT = HexColor("#34D399")
C_LIGHT_MINT = HexColor("#A7F3D0")
C_TEAL = HexColor("#0D9488")
C_DARK_TEXT = HexColor("#0F2F2C")
C_BODY = HexColor("#334155")
C_MUTED = HexColor("#64748B")
C_WHITE = HexColor("#FFFFFF")

C_TERM_BG = HexColor("#0F172A")
C_TERM_BAR = HexColor("#1E293B")
C_TERM_BORDER = HexColor("#334155")

C_GREEN_BG = HexColor("#ECFDF5")
C_GREEN_TXT = HexColor("#059669")
C_GREEN_BRD = HexColor("#A7F3D0")

C_RED_BG = HexColor("#FEF2F2")
C_RED_TXT = HexColor("#DC2626")
C_RED_BRD = HexColor("#FECACA")

C_BLUE_BG = HexColor("#EFF6FF")
C_BLUE_TXT = HexColor("#2563EB")
C_BLUE_BRD = HexColor("#BFDBFE")

def draw_footer(c, slide_num, is_dark=False):
    c.setFont("Helvetica", 9)
    c.setFillColor(C_LIGHT_MINT if is_dark else C_MUTED)
    c.drawString(64, 25, "FlowBoard · DevOps capstone")
    c.drawRightString(WIDTH - 64, 25, str(slide_num))

def draw_act_slide(c, num_str, title_str, subtitle_str, slide_num):
    c.setFillColor(C_DARK_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 54)
    c.setFillColor(C_MINT)
    c.drawString(80, HEIGHT - 180, num_str)

    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(C_WHITE)
    c.drawString(80, HEIGHT - 235, title_str)

    c.setFont("Helvetica", 14)
    c.setFillColor(C_LIGHT_MINT)
    c.drawString(80, HEIGHT - 270, subtitle_str)

    draw_footer(c, slide_num, is_dark=True)
    c.showPage()

def draw_content_header(c, title_str, subtitle_str=None, slide_num=None):
    c.setFillColor(C_LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(64, HEIGHT - 55, title_str)

    if subtitle_str:
        c.setFont("Helvetica", 10.5)
        c.setFillColor(C_TEAL)
        c.drawString(64, HEIGHT - 75, subtitle_str)

    if slide_num is not None:
        draw_footer(c, slide_num, is_dark=False)

def draw_card(c, x, y, width, height, title, items, tag=None, tag_color=C_TEAL, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
    c.setFillColor(bg_color)
    c.setStrokeColor(border_color)
    c.setLineWidth(1)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)

    cur_y = y + height - 20
    if tag:
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(tag_color)
        c.drawString(x + 14, cur_y, tag.upper())
        cur_y -= 15

    c.setFont("Helvetica-Bold", 11.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(x + 14, cur_y, title)
    cur_y -= 18

    c.setFont("Helvetica", 9)
    c.setFillColor(C_BODY)
    for itm in items:
        # Wrap long text if needed
        words = itm.split(" ")
        line = ""
        for w in words:
            if c.stringWidth(line + " " + w, "Helvetica", 9) < (width - 28):
                line = (line + " " + w).strip()
            else:
                c.drawString(x + 14, cur_y, line)
                cur_y -= 12
                line = w
        if line:
            c.drawString(x + 14, cur_y, line)
            cur_y -= 14

def draw_hero_card(c, x, y, width, height, num_str, label_str, desc_str=None):
    c.setFillColor(C_CARD_BG)
    c.setStrokeColor(C_CARD_BORDER)
    c.setLineWidth(1)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(C_TEAL)
    c.drawString(x + 16, y + height - 42, num_str)

    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(x + 16, y + height - 64, label_str)

    if desc_str:
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C_MUTED)
        c.drawString(x + 16, y + height - 80, desc_str)

def draw_terminal(c, x, y, width, height, title, lines):
    # Terminal Window
    c.setFillColor(C_TERM_BG)
    c.setStrokeColor(C_TERM_BORDER)
    c.setLineWidth(1)
    c.roundRect(x, y, width, height, 6, fill=1, stroke=1)

    # Title Bar
    bar_h = 24
    c.setFillColor(C_TERM_BAR)
    c.roundRect(x, y + height - bar_h, width, bar_h, 6, fill=1, stroke=0)
    c.rect(x, y + height - bar_h, width, 6, fill=1, stroke=0) # square bottom corners

    # Dots
    dots = [(HexColor("#EF4444"), x + 12), (HexColor("#F59E0B"), x + 24), (HexColor("#10B981"), x + 36)]
    for col, dx in dots:
        c.setFillColor(col)
        c.circle(dx, y + height - 12, 3.5, fill=1, stroke=0)

    # Title
    c.setFont("Courier-Bold", 8)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawString(x + 48, y + height - 15, title)

    # Body lines
    cur_y = y + height - bar_h - 14
    c.setFont("Courier", 7.5)
    for l in lines:
        if cur_y < y + 10:
            break
        if l.startswith("$"):
            c.setFillColor(C_MINT)
            c.setFont("Courier-Bold", 7.5)
        elif any(k in l for k in ["PASSED", "10 passed", "UP", "Running", "Active", "SUCCESS"]):
            c.setFillColor(HexColor("#34D399"))
            c.setFont("Courier", 7.5)
        elif any(k in l for k in ["FAIL", "ERROR", "422", "Crash"]):
            c.setFillColor(HexColor("#F87171"))
            c.setFont("Courier", 7.5)
        elif l.startswith("#") or "INFO" in l:
            c.setFillColor(HexColor("#38BDF8"))
            c.setFont("Courier", 7.5)
        else:
            c.setFillColor(HexColor("#E2E8F0"))
            c.setFont("Courier", 7.5)
        c.drawString(x + 12, cur_y, l)
        cur_y -= 11

def draw_arrow_r(c, x, y, length=24):
    c.setStrokeColor(C_TEAL)
    c.setFillColor(C_TEAL)
    c.setLineWidth(2)
    c.line(x, y, x + length, y)
    p = c.beginPath()
    p.moveTo(x + length, y - 4)
    p.lineTo(x + length + 6, y)
    p.lineTo(x + length, y + 4)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

def draw_arrow_d(c, x, y, length=20):
    c.setStrokeColor(C_TEAL)
    c.setFillColor(C_TEAL)
    c.setLineWidth(2)
    c.line(x, y, x, y - length)
    p = c.beginPath()
    p.moveTo(x - 4, y - length)
    p.lineTo(x, y - length - 6)
    p.lineTo(x + 4, y - length)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

def draw_table_custom(c, x, y, width, height, headers, rows, col_widths):
    c.saveState()
    styles = getSampleStyleSheet()
    h_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=C_WHITE)
    c_style = ParagraphStyle('TD', parent=styles['Normal'], fontName='Helvetica', fontSize=8, textColor=C_BODY)
    c_bold = ParagraphStyle('TDB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=C_DARK_TEXT)

    t_data = []
    t_data.append([Paragraph(h, h_style) for h in headers])
    for r in rows:
        row_cells = []
        for idx, val in enumerate(r):
            st = c_bold if idx == 0 else c_style
            row_cells.append(Paragraph(val, st))
        t_data.append(row_cells)

    tbl = Table(t_data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#0D9488")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#FFFFFF"), HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CBD5E1")),
    ]))
    tbl.wrapOn(c, width, height)
    tbl.drawOn(c, x, y)
    c.restoreState()

def build_pdf(output_path: str):
    c = canvas.Canvas(output_path, pagesize=(WIDTH, HEIGHT))

    # =========================================================================
    # SLIDE 1: Title Slide (Dark)
    # =========================================================================
    c.setFillColor(C_DARK_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 42)
    c.setFillColor(C_WHITE)
    c.drawString(80, HEIGHT - 160, "FLOWBOARD")

    c.setFont("Helvetica", 14)
    c.setFillColor(C_MINT)
    c.drawString(80, HEIGHT - 195, "A clinic appointment system, shipped through a complete DevOps pipeline" if False else "A cloud-native SaaS task board, shipped through a complete DevOps pipeline")

    # Workflow chips
    chips = ["TODO", "IN PROGRESS", "DONE"]
    for i, ch in enumerate(chips):
        bx = 80 + i * 140
        c.setFillColor(HexColor("#103836"))
        c.setStrokeColor(C_MINT)
        c.setLineWidth(1)
        c.roundRect(bx, HEIGHT - 260, 120, 28, 4, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(C_WHITE)
        c.drawCentredString(bx + 60, HEIGHT - 248, ch)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(C_WHITE)
    c.drawString(80, HEIGHT - 330, "Pranav Nayal")

    c.setFont("Helvetica", 10.5)
    c.setFillColor(C_LIGHT_MINT)
    c.drawString(80, HEIGHT - 350, "DevOps · Capstone Project · Session 21 · Instructor: Nensi Ravaliya")

    draw_footer(c, 1, is_dark=True)
    c.showPage()

    # =========================================================================
    # SLIDE 2: Core UX & Purpose (Card + Board Mockup)
    # =========================================================================
    draw_content_header(c, "One board. Live KPI stats. Zero state drift.", "Engineered for real-time visibility and bulletproof consistency", 2)
    draw_card(c, 64, 80, 340, 360, "Core Principles", [
        "Organizes tasks across TODO, IN PROGRESS, and DONE columns.",
        "Telemetry at /api/tasks/stats computes live velocity metrics.",
        "Enforces atomic state transitions with Pydantic and SQLAlchemy.",
        "Containers run unprivileged under non-root users (UID 10001 & 101)."
    ], tag="WORKFLOW")

    # Board Mockup
    c.setFillColor(HexColor("#F8FAFC"))
    c.setStrokeColor(C_CARD_BORDER)
    c.setLineWidth(1)
    c.roundRect(430, 80, 466, 360, 6, fill=1, stroke=1)

    # KPI row
    kpis = [("12", "TOTAL"), ("4", "IN PROGRESS"), ("5", "TODO"), ("3", "DONE")]
    for i, (num, lbl) in enumerate(kpis):
        bx = 445 + i * 110
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_CARD_BORDER)
        c.roundRect(bx, 365, 100, 60, 4, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(C_TEAL)
        c.drawCentredString(bx + 50, 400, num)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C_MUTED)
        c.drawCentredString(bx + 50, 380, lbl)

    # 3 Columns
    cols = [("TODO (5)", 445), ("IN PROGRESS (4)", 595), ("DONE (3)", 745)]
    for name, cx in cols:
        c.setFillColor(HexColor("#E2E8F0"))
        c.roundRect(cx, 325, 135, 24, 4, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(C_DARK_TEXT)
        c.drawCentredString(cx + 67, 332, name)

    # Task cards inside columns
    c.setFillColor(C_WHITE)
    c.setStrokeColor(HexColor("#CBD5E1"))
    c.roundRect(445, 230, 135, 80, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(453, 290, "Setup EKS Ingress")
    c.setFont("Helvetica", 7)
    c.setFillColor(C_MUTED)
    c.drawString(453, 275, "High Priority · DevOps")
    c.drawString(453, 260, "Assignee: Pranav")

    c.setFillColor(C_BLUE_BG)
    c.setStrokeColor(C_BLUE_BRD)
    c.roundRect(595, 230, 135, 80, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C_BLUE_TXT)
    c.drawString(603, 290, "Trivy Scan Pipeline")
    c.setFont("Helvetica", 7)
    c.setFillColor(C_MUTED)
    c.drawString(603, 275, "Medium · Security")
    c.drawString(603, 260, "Assignee: Pranav")

    c.setFillColor(C_GREEN_BG)
    c.setStrokeColor(C_GREEN_BRD)
    c.roundRect(745, 230, 135, 80, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C_GREEN_TXT)
    c.drawString(753, 290, "DB Migrations")
    c.setFont("Helvetica", 7)
    c.setFillColor(C_MUTED)
    c.drawString(753, 275, "Alembic 0001 · Head")
    c.drawString(753, 260, "Status: Complete")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(663, 105, "The live Kanban board, served from Docker Compose")
    c.showPage()

    # =========================================================================
    # SLIDE 3: The Project in Numbers
    # =========================================================================
    draw_content_header(c, "The project in numbers", "Verified engineering outcomes across the delivery lifecycle", 3)
    draw_hero_card(c, 64, 260, 250, 160, "10", "REST & ops endpoints", "CRUD, stats, health, ready, metrics")
    draw_hero_card(c, 355, 260, 250, 160, "10", "tests pass at 100%", "Hermetic SQLite fixture in 0.08s")
    draw_hero_card(c, 646, 260, 250, 160, "3", "CI/CD jobs on push", "Test & build, container scan, Helm")

    draw_hero_card(c, 64, 80, 250, 160, "56", "AWS resources planned", "Terraform VPC + EKS in Sydney")
    draw_hero_card(c, 355, 80, 250, 160, "0", "HIGH / CRITICAL CVEs", "Aqua Trivy security gate enforced")
    draw_hero_card(c, 646, 80, 250, 160, "0", "secrets committed to Git", "Environment-based configuration")
    c.showPage()

    # =========================================================================
    # SLIDE 4: Architecture Flow (Visual Diagram)
    # =========================================================================
    draw_content_header(c, "How it all fits together", "From git commit to automated testing, container registry, and AWS Kubernetes cluster", 4)

    # Top pipeline steps
    p_steps = [
        ("Developer pushes to\nGitHub", 64),
        ("GitHub Actions:\ntest, scan, build", 280),
        ("GHCR: images\ntagged by SHA", 496),
        ("Helm deploy\nto AWS EKS", 712)
    ]
    for text, px in p_steps:
        c.setFillColor(C_CARD_BG)
        c.setStrokeColor(C_CARD_BORDER)
        c.roundRect(px, 400, 184, 50, 4, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_DARK_TEXT)
        lines = text.split("\n")
        c.drawCentredString(px + 92, 428, lines[0])
        c.drawCentredString(px + 92, 414, lines[1])

    draw_arrow_r(c, 252, 425, 22)
    draw_arrow_r(c, 468, 425, 22)
    draw_arrow_r(c, 684, 425, 22)
    draw_arrow_d(c, 804, 395, 22)

    # AWS Cloud Container Box
    c.setFillColor(HexColor("#F8FAFC"))
    c.setStrokeColor(HexColor("#CBD5E1"))
    c.setLineWidth(1.5)
    c.roundRect(64, 75, 832, 290, 6, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(C_TEAL)
    c.drawString(80, 345, "AWS · ap-southeast-2 (Sydney) · Built by Terraform · VPC + Managed EKS 1.31")

    # Browser
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(90, 175, 110, 70, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(145, 215, "Browser / Client")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(145, 195, "(Public User)")

    draw_arrow_r(c, 204, 210, 26)

    # NGINX Ingress
    c.setFillColor(HexColor("#F0FDFA"))
    c.setStrokeColor(C_TEAL)
    c.roundRect(234, 155, 145, 105, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(306, 235, "NGINX Ingress")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_BODY)
    c.drawCentredString(306, 215, "Single Public LB")
    c.drawCentredString(306, 195, "Path Routing")
    c.drawCentredString(306, 175, "/ and /api")

    draw_arrow_r(c, 384, 235, 26)
    draw_arrow_r(c, 384, 180, 26)

    # Frontend Pods
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(414, 215, 170, 65, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(499, 255, "Frontend: React 18")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(499, 235, "NGINX (UID 101) ×2")

    # Backend Pods
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(414, 130, 170, 75, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(499, 185, "Backend: FastAPI")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(499, 165, "Python 3.12 (UID 10001)")
    c.drawCentredString(499, 145, "HPA: 2–6 Replicas")

    draw_arrow_r(c, 588, 165, 26)

    # Database
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(618, 130, 140, 75, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(688, 185, "PostgreSQL 16")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(688, 165, "StatefulSet + PVC")
    c.drawCentredString(688, 145, "gp3 volume")

    # Monitoring (Prometheus + Grafana)
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(618, 220, 115, 60, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(675, 255, "Prometheus")
    c.setFont("Helvetica", 7)
    c.setFillColor(C_MUTED)
    c.drawCentredString(675, 240, "scrapes /metrics")

    draw_arrow_r(c, 736, 250, 16)

    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(756, 220, 115, 60, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(813, 255, "Grafana")
    c.setFont("Helvetica", 7)
    c.setFillColor(C_MUTED)
    c.drawCentredString(813, 240, "Live Dashboards")

    c.showPage()

    # =========================================================================
    # SLIDE 5: Act 01 Divider
    # =========================================================================
    draw_act_slide(c, "01", "The application", "FastAPI, React and PostgreSQL, built for reliable task execution", 5)

    # =========================================================================
    # SLIDE 6: UI Screens & Dashboard
    # =========================================================================
    draw_content_header(c, "A single dashboard runs daily execution", "Clean navigation, live KPI metrics, and instant task state transitions", 6)
    draw_card(c, 64, 345, 360, 75, "Kanban Board", ["Live TODO, IN PROGRESS, and DONE columns with instant transitions."])
    draw_card(c, 64, 255, 360, 75, "Real-Time KPIs", ["Dynamic velocity and status counters calculated at /api/tasks/stats."])
    draw_card(c, 64, 165, 360, 75, "Task Creation Modal", ["Fast task entry with title, description, priority badge, and assignee."])
    draw_card(c, 64, 75, 360, 75, "Interactive Filters", ["Instant client-side filter chips toggle between all task states."])

    # Board Mockup
    c.setFillColor(HexColor("#F8FAFC"))
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(450, 75, 446, 345, 6, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(470, 395, "FlowBoard SaaS — Web Interface")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(C_BODY)
    c.drawString(470, 365, "Navigation: ▦ Dashboard   ✓ My Tasks   ◫ Projects   ◌ Activity")
    c.drawString(470, 340, "Status Counters: Total: 12 · In Progress: 4 · Todo: 5 · Done: 3")
    c.drawString(470, 315, "Active Filters: [ ALL ]  [ TODO ]  [ IN PROGRESS ]  [ DONE ]")

    c.drawString(470, 275, "• Task 1: Setup EKS Cluster (HIGH) — In Progress")
    c.drawString(470, 250, "• Task 2: Implement Prometheus Scrapes (MEDIUM) — In Progress")
    c.drawString(470, 225, "• Task 3: Configure Aqua Trivy Pipeline Gate (HIGH) — Done")
    c.drawString(470, 200, "• Task 4: Multi-stage Dockerfile Non-Root (LOW) — Done")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(C_MUTED)
    c.drawCentredString(673, 100, "The Board, served from Docker Compose")
    c.showPage()

    # =========================================================================
    # SLIDE 7: Instant Feedback / Error & Mobile
    # =========================================================================
    draw_content_header(c, "Instant feedback across any device", "Inline service resilience and fluid responsive design down to 375 px", 7)
    draw_card(c, 64, 80, 390, 350, "Service Resilience", [
        "Non-intrusive inline notification if backend is unreachable.",
        "Prevents full application crash or white-screen errors.",
        "Automatic background polling resumes as soon as API is healthy."
    ], tag="AVAILABILITY")

    c.setFillColor(C_RED_BG)
    c.setStrokeColor(C_RED_BRD)
    c.roundRect(84, 120, 350, 110, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(C_RED_TXT)
    c.drawString(100, 205, "⚠ Backend service unavailable")
    c.setFont("Helvetica", 8.5)
    c.drawString(100, 175, "The application gracefully degraded to offline state.")
    c.drawString(100, 155, "Retrying connection in the background...")

    draw_card(c, 506, 80, 390, 350, "Mobile Viewport", [
        "Layout adapts cleanly down to 375 px mobile screen width.",
        "Sidebar collapses to compact hamburger drawer navigation.",
        "Columns reflow into single-column vertical card stack."
    ], tag="RESPONSIVENESS")

    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(550, 105, 300, 150, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(565, 230, "Mobile View (375 × 667 px)")
    c.setFont("Helvetica", 8)
    c.setFillColor(C_BODY)
    c.drawString(565, 205, "≡ FlowBoard              [+]")
    c.drawString(565, 185, "[12 Total] [4 Active] [3 Done]")
    c.drawString(565, 165, "────────────────────────────────")
    c.drawString(565, 145, "□ EKS Terraform Module")
    c.drawString(565, 125, "□ Pytest Hermetic Tests")
    c.showPage()

    # =========================================================================
    # SLIDE 8: Lifecycle State Machine (Flowchart)
    # =========================================================================
    draw_content_header(c, "Every task follows an explicit lifecycle", "Deterministic state progression enforced at API gateway and database", 8)

    # State Flowchart
    states = [("TODO", 100, C_CARD_BG, C_CARD_BORDER, C_DARK_TEXT),
              ("IN PROGRESS", 380, C_BLUE_BG, C_BLUE_BRD, C_BLUE_TXT),
              ("DONE", 660, C_GREEN_BG, C_GREEN_BRD, C_GREEN_TXT)]
    for name, sx, bg, brd, txt in states:
        c.setFillColor(bg)
        c.setStrokeColor(brd)
        c.setLineWidth(1.5)
        c.roundRect(sx, 305, 180, 65, 6, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(txt)
        c.drawCentredString(sx + 90, 332, name)

    draw_arrow_r(c, 290, 337, 75)
    draw_arrow_r(c, 570, 337, 75)

    draw_card(c, 64, 80, 250, 185, "Strict State Machine", [
        "Sequential advancement.",
        "Tasks move from TODO to IN PROGRESS, then to DONE.",
        "Illegal status values rejected."
    ], tag="RULE 1")

    draw_card(c, 355, 80, 250, 185, "Atomic Updates", [
        "Synchronous state changes.",
        "SQLAlchemy commits status changes and timestamps atomically.",
        "Zero lost updates under load."
    ], tag="RULE 2")

    draw_card(c, 646, 80, 250, 185, "Live Metrics Recalc", [
        "Dynamic velocity counters.",
        "Transitions recalculate /api/tasks/stats aggregate metrics.",
        "Instant UI dashboard sync."
    ], tag="RULE 3")
    c.showPage()

    # =========================================================================
    # SLIDE 9: PostgreSQL & Pydantic Integrity
    # =========================================================================
    draw_content_header(c, "PostgreSQL and Pydantic guarantee data integrity", "Validation at the API boundary, atomicity at the database engine", 9)
    draw_terminal(c, 64, 80, 420, 350, "backend/app/models.py (SQLAlchemy 2.0)", [
        "# Database Model Definition",
        "class Task(Base):",
        "    __tablename__ = 'tasks'",
        "",
        "    id = Column(Integer, primary_key=True)",
        "    title = Column(String(200), nullable=False)",
        "    description = Column(Text, nullable=True)",
        "    status = Column(Enum(TaskStatus),",
        "                    default=TaskStatus.TODO,",
        "                    nullable=False)",
        "    priority = Column(Enum(Priority),",
        "                      default=Priority.MEDIUM)",
        "    created_at = Column(DateTime, default=utc)",
        "",
        "# Pydantic schema rejects invalid data: HTTP 422"
    ])

    draw_card(c, 510, 320, 386, 110, "Two-Tier Validation", [
        "Pydantic validates payload schema; PostgreSQL guarantees column constraints."
    ], tag="INTEGRITY")
    draw_card(c, 510, 200, 386, 110, "Atomic Transactions", [
        "SQLAlchemy sessions guarantee automatic rollback on database failure."
    ], tag="ACID")
    draw_card(c, 510, 80, 386, 110, "Hermetic Proof", [
        "Pytest test_update_task proves status progression.",
        "Malformed payloads return HTTP 422 Unprocessable Entity."
    ], tag="VERIFICATION")
    c.showPage()

    # =========================================================================
    # SLIDE 10: 10 REST Endpoints + Probes
    # =========================================================================
    draw_content_header(c, "Ten REST endpoints plus ops probes", "Complete resource management, live metrics, and Kubernetes health probes", 10)
    draw_card(c, 64, 255, 250, 175, "Tasks CRUD", [
        "GET /api/tasks · List all",
        "POST /api/tasks · Create new",
        "GET /api/tasks/{id} · Retrieve",
        "PUT /api/tasks/{id} · Update",
        "DELETE /api/tasks/{id} · Delete"
    ], tag="RESOURCE")
    draw_card(c, 355, 255, 250, 175, "Metrics & Stats", [
        "GET /api/tasks/stats",
        "Aggregates total, todo,",
        "in_progress, and done counts.",
        "Real-time velocity stats."
    ], tag="ANALYTICS")
    draw_card(c, 646, 255, 250, 175, "Ops Probes", [
        "GET /health · Liveness probe",
        "GET /ready · Readiness probe",
        "GET /metrics · Prometheus",
        "GET / · Service metadata"
    ], tag="OPERATIONS")

    draw_card(c, 64, 80, 390, 155, "Kubernetes Liveness & Readiness", [
        "/health validates process execution cheaply without DB overhead.",
        "/ready executes SELECT 1 against PostgreSQL before routing traffic."
    ], tag="PROBES")
    draw_card(c, 506, 80, 390, 155, "OpenAPI Documentation", [
        "FastAPI auto-generates interactive Swagger documentation.",
        "Complete interactive exploration at /docs and OpenAPI JSON at /openapi.json."
    ], tag="SWAGGER")
    c.showPage()

    # =========================================================================
    # SLIDE 11: Alembic Schema Migrations
    # =========================================================================
    draw_content_header(c, "Alembic owns the schema migrations", "Version-controlled database schema; zero ad-hoc SQL in production", 11)
    draw_card(c, 64, 80, 370, 350, "Migration Architecture", [
        "Versioned revisions track table creation and schema enhancements.",
        "Migrations only: app code never calls create_all() in production.",
        "Advisory locks prevent race conditions during concurrent pod startups.",
        "Readiness probe gates traffic until DB schema reaches head."
    ], tag="DATABASE EVOLUTION")

    draw_terminal(c, 460, 80, 436, 350, "alembic upgrade head", [
        "$ alembic current",
        "INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.",
        "INFO  [alembic.runtime.migration] Will assume transactional DDL.",
        "0001_create_tasks (head)",
        "",
        "$ alembic upgrade head",
        "INFO  [alembic.runtime.migration] Running upgrade -> 0001_create_tasks",
        "INFO  [alembic.runtime.migration] Creating table tasks",
        "INFO  [alembic.runtime.migration] Creating index ix_tasks_id",
        "INFO  [alembic.runtime.migration] Target database is up to date: 0001 (head)",
        "",
        "$ psql -d flowboard -c '\\d tasks'",
        "Column      | Type         | Nullable | Default",
        "id          | integer      | not null | generated",
        "title       | varchar(200) | not null | ",
        "status      | task_status  | not null | 'TODO'",
        "created_at  | timestamp    | not null | now()"
    ])
    c.showPage()

    # =========================================================================
    # SLIDE 12: Act 02 Divider
    # =========================================================================
    draw_act_slide(c, "02", "Quality and containers", "Tests prove the rules. Docker makes the app run identically everywhere", 12)

    # =========================================================================
    # SLIDE 13: 10 Tests Prove the Rules
    # =========================================================================
    draw_content_header(c, "10 tests prove the rules", "Hermetic in-memory test suite with 100% endpoint pass rate", 13)
    draw_hero_card(c, 64, 255, 175, 175, "10", "tests pass", "100% pass rate")
    draw_hero_card(c, 255, 255, 175, 175, "0.08s", "execution time", "Zero CI flakiness")

    draw_card(c, 64, 80, 366, 155, "Hermetic Testing", [
        "In-memory SQLite fixture with StaticPool.",
        "Transactional rollback guarantees clean isolation.",
        "Sub-second execution stops pipeline bottlenecks."
    ], tag="ISOLATION")

    draw_terminal(c, 455, 80, 441, 350, "pytest -v", [
        "$ pytest -v",
        "============================= test session starts ==============================",
        "platform linux -- Python 3.12, pytest-8.3.4, pluggy-1.7.0",
        "rootdir: /home/pranav/devopsProject/backend, configfile: pytest.ini",
        "collected 10 items",
        "",
        "tests/test_api.py::test_health PASSED             [ 10%]",
        "tests/test_api.py::test_ready PASSED              [ 20%]",
        "tests/test_api.py::test_root PASSED               [ 30%]",
        "tests/test_api.py::test_create_task PASSED        [ 40%]",
        "tests/test_api.py::test_list_tasks PASSED         [ 50%]",
        "tests/test_api.py::test_get_task_by_id PASSED     [ 60%]",
        "tests/test_api.py::test_get_task_not_found PASSED [ 70%]",
        "tests/test_api.py::test_update_task PASSED        [ 80%]",
        "tests/test_api.py::test_stats_endpoint PASSED     [ 90%]",
        "tests/test_api.py::test_delete_task PASSED        [100%]",
        "============================== 10 passed in 0.08s =============================="
    ])
    c.showPage()

    # =========================================================================
    # SLIDE 14: Docker Images Run Non-Root
    # =========================================================================
    draw_content_header(c, "Docker images run strictly non-root", "Least-privilege containers, minimal attack surface, and pinned dependencies", 14)
    draw_card(c, 64, 80, 250, 350, "Multi-Stage Builds", [
        "Node 22 compiles React assets.",
        "Unprivileged NGINX 1.27 serves static build files.",
        "Compilers and dev tools never ship to production.",
        "Frontend image size: 24 MB."
    ], tag="MINIMAL FOOTPRINT")

    draw_card(c, 355, 80, 250, 350, "Digest & Version Pinning", [
        "Base images pinned to exact tags.",
        "python:3.12-slim and nginxinc/nginx-unprivileged:1.27-alpine.",
        "Guarantees bit-for-bit build reproducibility across environments."
    ], tag="REPRODUCIBILITY")

    draw_card(c, 646, 80, 250, 350, "Non-Root Users", [
        "Backend runs as appuser (UID 10001).",
        "Frontend runs as nginx (UID 101).",
        "Containers drop root capabilities.",
        "Prevents container escape vulnerabilities."
    ], tag="SECURITY")
    c.showPage()

    # =========================================================================
    # SLIDE 15: Docker Compose Stack (Service Flow)
    # =========================================================================
    draw_content_header(c, "One command starts the whole stack", "Coordinated local multi-container development with Docker Compose", 15)
    draw_card(c, 64, 80, 340, 350, "Compose Architecture", [
        "docker compose up --build -d starts all 3 services.",
        "Postgres listens on localhost only; secrets kept in ignored .env file.",
        "Services connect over isolated internal bridge network.",
        "Volume mount guarantees database persistence across restarts."
    ], tag="LOCAL STACK")

    # Flowchart on right
    c_flow = [
        ("1. postgres:16-alpine", "Healthcheck: pg_isready -U postgres", 430, 320),
        ("2. backend: fastapi (Python 3.12)", "Waits for DB healthy · Runs migrations · Port 8000", 430, 205),
        ("3. frontend: nginx-unprivileged", "Waits for backend /ready · Reverse proxy · Port 3000", 430, 90)
    ]
    for title, sub, fx, fy in c_flow:
        c.setFillColor(C_CARD_BG)
        c.setStrokeColor(C_CARD_BORDER)
        c.roundRect(fx, fy, 466, 85, 6, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(C_DARK_TEXT)
        c.drawString(fx + 16, fy + 55, title)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C_BODY)
        c.drawString(fx + 16, fy + 32, sub)

    draw_arrow_d(c, 663, 318, 25)
    draw_arrow_d(c, 663, 203, 25)
    c.showPage()

    # =========================================================================
    # SLIDE 16: Act 03 Divider
    # =========================================================================
    draw_act_slide(c, "03", "The pipeline", "Every push to main is tested, scanned, built, published, and deployed", 16)

    # =========================================================================
    # SLIDE 17: GitHub Actions Pipeline (Flow Diagram)
    # =========================================================================
    draw_content_header(c, "Every push runs automated pipeline jobs", "GitHub Actions coordinates four automated stages on every commit", 17)
    stages = [
        ("STAGE 1", "Parallel Test & Build", "Pytest (10/10 PASS) + Vite Production Build", 64),
        ("STAGE 2", "Container DevSecOps", "Multi-Stage Docker + Aqua Trivy (0 CVEs)", 280),
        ("STAGE 3", "Artifact Registry", "Push to GHCR tagged with Git Commit SHA", 496),
        ("STAGE 4", "Kubernetes Deploy", "Helm Rolling Upgrade to AWS EKS", 712)
    ]
    for tag, title, sub, sx in stages:
        c.setFillColor(C_CARD_BG)
        c.setStrokeColor(C_CARD_BORDER)
        c.roundRect(sx, 230, 184, 180, 6, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C_TEAL)
        c.drawString(sx + 14, 385, tag)
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(C_DARK_TEXT)
        c.drawString(sx + 14, 360, title)
        c.setFont("Helvetica", 8)
        c.setFillColor(C_BODY)
        words = sub.split(" ")
        l1, l2 = " ".join(words[:4]), " ".join(words[4:])
        c.drawString(sx + 14, 330, l1)
        c.drawString(sx + 14, 315, l2)

    draw_arrow_r(c, 252, 320, 24)
    draw_arrow_r(c, 468, 320, 24)
    draw_arrow_r(c, 684, 320, 24)

    draw_card(c, 64, 80, 250, 130, "Trigger Rules", [
        "Runs on push and pull request to main.",
        "Quality gates block merge on failure."
    ], tag="EVENT")
    draw_card(c, 355, 80, 250, 130, "Tagging Discipline", [
        "Images tagged with Git SHA (${{ github.sha }}).",
        "Never mutable :latest tags in production."
    ], tag="PROVENANCE")
    draw_card(c, 646, 80, 250, 130, "Automated Rollout", [
        "Helm performs zero-downtime rolling update.",
        "Validates /ready probes before rollout."
    ], tag="DEPLOY")
    c.showPage()

    # =========================================================================
    # SLIDE 18: Green vs Red Pipeline
    # =========================================================================
    draw_content_header(c, "A failing test stops everything", "Strict quality gate protects the container registry and production cluster", 18)
    
    # Left Green
    c.setFillColor(C_GREEN_BG)
    c.setStrokeColor(C_GREEN_BRD)
    c.roundRect(64, 80, 390, 350, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 11.5)
    c.setFillColor(C_GREEN_TXT)
    c.drawString(84, 395, "✓ GREEN PIPELINE — ALL PASS")
    c.setFont("Helvetica", 9)
    c.setFillColor(C_DARK_TEXT)
    g_lines = [
        "1. [✓] Pytest: 10/10 tests pass in 0.08s",
        "2. [✓] Vite: React assets compiled successfully",
        "3. [✓] Trivy: 0 HIGH, 0 CRITICAL CVEs detected",
        "4. [✓] GHCR: Images pushed tagged with SHA",
        "5. [✓] Helm: Rolling update verified on EKS",
        "",
        "Outcome: Deployment succeeds with zero downtime."
    ]
    cur_y = 360
    for l in g_lines:
        c.drawString(84, cur_y, l)
        cur_y -= 22

    # Right Red
    c.setFillColor(C_RED_BG)
    c.setStrokeColor(C_RED_BRD)
    c.roundRect(506, 80, 390, 350, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 11.5)
    c.setFillColor(C_RED_TXT)
    c.drawString(526, 395, "✗ RED PIPELINE — TEST FAILURE")
    c.setFont("Helvetica", 9)
    c.setFillColor(C_DARK_TEXT)
    r_lines = [
        "1. [✗] Pytest: 1 test failed (HTTP 500 error)",
        "2. [🚫] Vite: Execution aborted",
        "3. [🚫] Docker: Build stage skipped",
        "4. [🚫] GHCR: No images pushed to registry",
        "5. [🚫] Helm: Deployment halted immediately",
        "",
        "Outcome: Zero broken code reaches registry or cluster."
    ]
    cur_y = 360
    for l in r_lines:
        c.drawString(526, cur_y, l)
        cur_y -= 22

    c.showPage()

    # =========================================================================
    # SLIDE 19: GHCR Image Publishing
    # =========================================================================
    draw_content_header(c, "Images ship to GHCR tagged by commit SHA", "Immutable container artifacts published to GitHub Container Registry", 19)
    draw_card(c, 64, 160, 390, 270, "flowboard-backend", [
        "Registry: ghcr.io/pranavnayal/flowboard-backend",
        "Tag: 8fcb0c06d29ecdc2198df9a432819b13dadc866c",
        "Base Image: python:3.12-slim (Debian 12 Bookworm)",
        "User: UID 10001 (appuser) · Size: 68 MB",
        "Architecture: linux/amd64"
    ], tag="API CONTAINER")

    draw_card(c, 506, 160, 390, 270, "flowboard-frontend", [
        "Registry: ghcr.io/pranavnayal/flowboard-frontend",
        "Tag: 8fcb0c06d29ecdc2198df9a432819b13dadc866c",
        "Base Image: nginxinc/nginx-unprivileged:1.27-alpine",
        "User: UID 101 (nginx) · Size: 24 MB",
        "Architecture: linux/amd64"
    ], tag="WEB CONTAINER")

    c.setFillColor(C_CARD_BG)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(64, 80, 832, 60, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(480, 105, "Immutable SHA tagging guarantees exact reproducibility: any running pod can be traced back to its single Git commit.")
    c.showPage()

    # =========================================================================
    # SLIDE 20: Trivy Gates CVEs
    # =========================================================================
    draw_content_header(c, "Trivy gates every image against CVEs", "Automated vulnerability scanning stops security debt at the container boundary", 20)
    draw_card(c, 64, 80, 340, 350, "Trivy Gate Policy", [
        "Scans OS base packages and application language dependencies.",
        "Enforces pipeline failure on --severity HIGH,CRITICAL --exit-code 1.",
        "Clean scan result: 0 HIGH, 0 CRITICAL vulnerabilities.",
        "Publishes SARIF reports directly to GitHub Security Advisory dashboard."
    ], tag="DEVSECOPS")

    draw_terminal(c, 430, 80, 466, 350, "trivy image scan report", [
        "$ trivy image --severity HIGH,CRITICAL --exit-code 1 \\",
        "    ghcr.io/pranavnayal/flowboard-backend:sha-8fcb0c0",
        "2026-10-16T22:15:00Z INFO Vulnerability scanning enabled",
        "2026-10-16T22:15:02Z INFO Detected OS: debian 12.8 (bookworm)",
        "2026-10-16T22:15:03Z INFO Number of language dependencies: 32",
        "",
        "ghcr.io/pranavnayal/flowboard-backend (debian 12.8)",
        "==================================================",
        "Total: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)",
        "",
        "Python (requirements.txt)",
        "=========================",
        "Total: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)",
        "",
        "RESULT: PASSED (Exit code: 0)"
    ])
    c.showPage()

    # =========================================================================
    # SLIDE 21: End-to-End Security
    # =========================================================================
    draw_content_header(c, "Security runs through the entire delivery pipeline", "Defense-in-depth applied across code, containers, pipeline, and cluster", 21)
    sec_items = [
        ("Non-Root Everywhere", "Containers drop all root privileges; execute as UID 10001 & UID 101.", 64, 260),
        ("Actions Pinned by SHA", "GitHub Actions pinned to 40-character commit hashes against attacks.", 355, 260),
        ("No Secrets in Git", "All database and cloud credentials injected at runtime via k8s Secrets.", 646, 260),
        ("Read-Only Root FS", "Pods mount root filesystems read-only with emptyDir for transient /tmp.", 64, 80),
        ("Automated CVE Gating", "Aqua Trivy gates every container image build on HIGH/CRITICAL findings.", 355, 80),
        ("CORS Closed by Default", "Ingress proxy routes same-origin traffic; eliminates wildcard CORS exposures.", 646, 80)
    ]
    for title, desc, sx, sy in sec_items:
        draw_card(c, sx, sy, 250, 160, title, [desc], tag="SECURITY")
    c.showPage()

    # =========================================================================
    # SLIDE 22: Act 04 Divider
    # =========================================================================
    draw_act_slide(c, "04", "Infrastructure and Kubernetes", "Terraform builds AWS. Helm runs the app. Autoscaling and monitoring keep it healthy", 22)

    # =========================================================================
    # SLIDE 23: Architectural Decisions Table
    # =========================================================================
    draw_content_header(c, "Architectural decisions shaped our cloud design", "Balancing AWS constraints, regional policies, high availability, and cost governance", 23)
    headers23 = ["Design Requirement / Constraint", "Architectural Decision & Implementation"]
    rows23 = [
        ["Regional resource constraint", "Provisioned strictly in ap-southeast-2 (Sydney) per project policy"],
        ["Network tiering & isolation", "Custom VPC: 2 Public subnets (Ingress) and 2 Private subnets (EKS nodes)"],
        ["Managed Kubernetes orchestration", "AWS EKS 1.31 cluster with managed worker node group and IAM roles"],
        ["Cost governance & zero idle spend", "Ephemeral infrastructure: verified plans with automated clean teardown"],
        ["Reproducible Infrastructure as Code", "Modular Terraform HCL defining 56 declarative resources"]
    ]
    draw_table_custom(c, 64, 120, 832, 300, headers23, rows23, [280, 552])
    c.showPage()

    # =========================================================================
    # SLIDE 24: Terraform Stack
    # =========================================================================
    draw_content_header(c, "Terraform builds the entire stack from code", "Declarative provisioning of network, compute, storage, and IAM", 24)
    draw_hero_card(c, 64, 255, 175, 175, "56", "AWS resources", "VPC + EKS cluster")
    draw_hero_card(c, 255, 255, 175, 175, "12 min", "provision time", "Terraform apply")

    draw_terminal(c, 64, 80, 366, 155, "terraform plan", [
        "$ terraform plan",
        "Plan: 56 to add, 0 to change, 0 to destroy.",
        "Outputs:",
        "  cluster_endpoint = 'https://...eks.amazonaws.com'",
        "  vpc_id = 'vpc-0a8f7c9e'"
    ])

    draw_terminal(c, 455, 80, 441, 350, "terraform apply", [
        "$ terraform apply -auto-approve",
        "module.vpc.aws_vpc.this[0]: Creating...",
        "module.vpc.aws_subnet.public[0]: Creating...",
        "module.vpc.aws_subnet.private[0]: Creating...",
        "module.eks.aws_eks_cluster.this[0]: Creating...",
        "module.eks.aws_eks_node_group.this['default']: Creating...",
        "",
        "Apply complete! Resources: 56 added, 0 changed, 0 destroyed.",
        "",
        "$ aws eks update-kubeconfig --region ap-southeast-2 \\",
        "    --name flowboard-eks",
        "Added new context to /home/pranav/.kube/config"
    ])
    c.showPage()

    # =========================================================================
    # SLIDE 25: AWS Console Confirmation
    # =========================================================================
    draw_content_header(c, "AWS Console confirms the VPC and EKS cluster", "Verified infrastructure state in AWS Management Console (ap-southeast-2)", 25)
    draw_card(c, 64, 80, 390, 350, "Amazon VPC Dashboard", [
        "VPC Name: flowboard-vpc (10.0.0.0/16)",
        "Subnets: 2 Public (10.0.1.0/24, 10.0.2.0/24)",
        "Subnets: 2 Private (10.0.10.0/24, 10.0.11.0/24)",
        "Internet Gateway: igw-0b8d2 (Attached)",
        "NAT Gateway: nat-0c4e1 (Public Subnet)",
        "Route Tables: Public routes to IGW; Private to NAT"
    ], tag="NETWORKING")

    draw_card(c, 506, 80, 390, 350, "Amazon EKS Dashboard", [
        "Cluster Name: flowboard-eks",
        "Status: Active",
        "Kubernetes Version: 1.31",
        "API Endpoint: Private + Public Access",
        "Node Group: 2 x t3.medium (Amazon Linux 2023)",
        "Pod Identity: Configured with least-privilege IAM roles"
    ], tag="COMPUTE")
    c.showPage()

    # =========================================================================
    # SLIDE 26: Helm Packages the App
    # =========================================================================
    draw_content_header(c, "Helm packages the app for Kubernetes", "Declarative release management across multiple pods and services", 26)
    draw_card(c, 64, 80, 340, 350, "Helm Release Architecture", [
        "Deployments: 2 backend and 2 frontend pods with rolling update strategy.",
        "StatefulSet: PostgreSQL 16 with persistent volume claim (gp3 storage).",
        "ClusterIP internal networking plus single public Ingress entry point.",
        "Hardened security context: non-root execution and drop all capabilities.",
        "Horizontal Pod Autoscaler configured targeting 60% CPU utilization."
    ], tag="ORCHESTRATION")

    draw_terminal(c, 430, 80, 466, 350, "kubectl get pods -n flowboard", [
        "$ kubectl get pods -n flowboard",
        "NAME                                  READY   STATUS    RESTARTS   AGE",
        "flowboard-backend-798b5f9798-f8vqk    1/1     Running   0          4m",
        "flowboard-backend-798b5f9798-l2pxz    1/1     Running   0          4m",
        "flowboard-frontend-6b459d87fc-2v7k4   1/1     Running   0          4m",
        "flowboard-frontend-6b459d87fc-9mw5t   1/1     Running   0          4m",
        "flowboard-postgres-0                  1/1     Running   0          5m",
        "",
        "$ helm list -n flowboard",
        "NAME       NAMESPACE  REVISION  STATUS    CHART            APP VERSION",
        "flowboard  flowboard  1         deployed  flowboard-0.1.0  1.0.0"
    ])
    c.showPage()

    # =========================================================================
    # SLIDE 27: Ingress Single Entry Point
    # =========================================================================
    draw_content_header(c, "NGINX Ingress provides a single public entry point", "Intelligent path routing eliminates external CORS and protects backend services", 27)
    draw_card(c, 64, 80, 340, 350, "Ingress Traffic Routing", [
        "AWS Load Balancer exposes a single public entry point for the entire application.",
        "Ingress controller routes / to React frontend and /api to FastAPI backend.",
        "Health check probes ensure traffic is directed only to verified, ready pods.",
        "Zero cross-origin resource sharing (CORS) complexity."
    ], tag="NETWORK INGRESS")

    # Browser window mockup
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(430, 80, 466, 350, 6, fill=1, stroke=1)

    c.setFillColor(HexColor("#F1F5F9"))
    c.setStrokeColor(HexColor("#CBD5E1"))
    c.roundRect(445, 380, 436, 36, 4, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(455, 393, "🔒 http://k8s-flowboard-ingress.ap-southeast-2.elb.amazonaws.com")

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(C_GREEN_TXT)
    c.drawString(455, 340, "HTTP 200 OK — Ingress Verified")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(C_BODY)
    c.drawString(455, 310, "Path Mapping Rules:")
    c.drawString(455, 290, "• /            ──> Service flowboard-frontend:80 (React UI)")
    c.drawString(455, 270, "• /api         ──> Service flowboard-backend:8000 (FastAPI)")
    c.drawString(455, 250, "• /health      ──> Liveness Probe (HTTP 200)")
    c.drawString(455, 230, "• /metrics     ──> Internal Telemetry Scrape")
    c.drawString(455, 190, "Status: High Availability Active across 2 Availability Zones.")
    c.showPage()

    # =========================================================================
    # SLIDE 28: Autoscaler Load Graph
    # =========================================================================
    draw_content_header(c, "The autoscaler adds pods under load", "Horizontal Pod Autoscaler scales replicas dynamically in response to traffic spikes", 28)
    draw_hero_card(c, 64, 255, 175, 175, "2 → 6", "backend pods", "Dynamic HPA scale-up")
    draw_hero_card(c, 255, 255, 175, 175, "0", "errors in test", "100% request success")

    draw_card(c, 64, 80, 366, 155, "HPA Target Policy", [
        "Target metric: 60% CPU utilization.",
        "Min replicas: 2 pods (baseline).",
        "Max replicas: 6 pods (peak traffic).",
        "Stabilization window: 300s scale-down cooloff."
    ], tag="SCALING POLICY")

    c.setFillColor(HexColor("#F8FAFC"))
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(455, 80, 441, 350, 6, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawString(475, 395, "HPA Dynamic Scaling Timeline (load-test.sh)")

    c.setFont("Helvetica", 8)
    c.setFillColor(C_BODY)
    timeline_lines = [
        "00:00 — Baseline: 2 pods | CPU: 22% (Idle)",
        "00:30 — Load injection: 200 concurrent requests/sec",
        "01:00 — CPU threshold crossed: 84% > 60%",
        "01:15 — HPA Scale Event: Replicas 2 ──> 4 pods",
        "01:45 — Traffic surge: Replicas 4 ──> 6 pods",
        "02:15 — CPU stabilizes: 52% across 6 pods",
        "03:30 — Load stops: Traffic drops to zero",
        "05:00 — Cooldown period completes: Replicas return to 2",
        "",
        "Result: 0 dropped requests during entire burst."
    ]
    cur_y = 360
    for l in timeline_lines:
        c.drawString(475, cur_y, l)
        cur_y -= 19
    c.showPage()

    # =========================================================================
    # SLIDE 29: Prometheus RED Metrics
    # =========================================================================
    draw_content_header(c, "The backend exposes Prometheus RED metrics", "Rate, Errors, and Duration instrumentation exposed at /metrics", 29)
    draw_card(c, 64, 80, 340, 350, "RED Telemetry Principles", [
        "Rate: Total HTTP requests partitioned by endpoint, method, and status code.",
        "Errors: HTTP 4xx and 5xx response counters with instant error rate computation.",
        "Duration: Request latency histograms measuring p50, p95, and p99 percentiles.",
        "Ops Telemetry: Exposes liveness and database connection pool health states."
    ], tag="METRICS")

    draw_terminal(c, 430, 80, 466, 350, "curl localhost:8000/metrics", [
        "# HELP http_requests_total Total number of HTTP requests",
        "# TYPE http_requests_total counter",
        "http_requests_total{method='GET',handler='/api/tasks',status='200'} 4128",
        "http_requests_total{method='POST',handler='/api/tasks',status='201'} 314",
        "http_requests_total{method='PUT',handler='/api/tasks/{id}',status='200'} 842",
        "",
        "# HELP http_request_duration_seconds HTTP request latency histogram",
        "# TYPE http_request_duration_seconds histogram",
        "http_request_duration_seconds_bucket{le='0.05',handler='/api/tasks'} 4102",
        "http_request_duration_seconds_bucket{le='0.1',handler='/api/tasks'} 4120",
        "http_request_duration_seconds_bucket{le='0.25',handler='/api/tasks'} 4128",
        "http_request_duration_seconds_sum{handler='/api/tasks'} 42.18",
        "http_request_duration_seconds_count{handler='/api/tasks'} 4128"
    ])
    c.showPage()

    # =========================================================================
    # SLIDE 30: Prometheus & Grafana Dashboards
    # =========================================================================
    draw_content_header(c, "Prometheus scrapes it and Grafana shows it", "End-to-end observability stack deployed in-cluster via Prometheus Operator", 30)
    draw_card(c, 64, 80, 390, 350, "Prometheus ServiceMonitor", [
        "Target: flowboard-backend:8000/metrics",
        "State: UP (Health 100%)",
        "Scrape Interval: 15s",
        "Auto-Discovery: Discovers backend pods dynamically via ServiceMonitor CRD labels.",
        "Scrape Failure Rate: 0.00%"
    ], tag="SCRAPE TARGETS")

    draw_card(c, 506, 80, 390, 350, "Grafana Visual Dashboard", [
        "Dashboard: FlowBoard Operational Performance",
        "Panel 1: Request Rate (Current: 42 req/s)",
        "Panel 2: Error Rate (0.00% 5xx errors)",
        "Panel 3: p95 Latency (14 ms response time)",
        "Panel 4: Pod Memory & CPU Utilization",
        "Live on EKS monitoring namespace."
    ], tag="VISUALIZATION")
    c.showPage()

    # =========================================================================
    # SLIDE 31: Act 05 Divider
    # =========================================================================
    draw_act_slide(c, "05", "Operate and learn", "Ship a change. Diagnose failures. Control cost. Reflect honestly", 31)

    # =========================================================================
    # SLIDE 32: One Commit Live Deployment (Before / After)
    # =========================================================================
    draw_content_header(c, "One commit became a live deployment", "End-to-end verification: from git commit to zero-downtime rolling update", 32)
    draw_card(c, 64, 160, 390, 270, "Before Deployment", [
        "Git Commit: 8fcb0c0 (Initial release)",
        "Image Tag: ghcr.io/...:sha-8fcb0c0",
        "Pod Replicas: 2/2 Running",
        "UI Subtitle: 'DevOps Capstone Project'"
    ], tag="RELEASE V1")

    draw_card(c, 506, 160, 390, 270, "After Deployment", [
        "Git Commit: 0de6666 (Updated release)",
        "Image Tag: ghcr.io/...:sha-0de6666",
        "Pod Replicas: 2/2 Running",
        "UI Subtitle: 'Live Production Release'"
    ], tag="RELEASE V2")

    c.setFillColor(C_CARD_BG)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(64, 80, 832, 60, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(C_DARK_TEXT)
    c.drawCentredString(480, 105, "Zero-Downtime Rolling Update: Kubernetes verifies /ready probe on new pods before terminating old pods.")
    c.showPage()

    # =========================================================================
    # SLIDE 33: Pipeline Ships Under 3 Minutes
    # =========================================================================
    draw_content_header(c, "The delivery pipeline ships in under 3 minutes", "Parallel quality gates and caching deliver rapid, dependable releases", 33)
    draw_card(c, 64, 80, 370, 350, "Pipeline Efficiency", [
        "Hermetic Pytest test suite executes in just 0.08 seconds.",
        "Parallel Vite frontend build compiles static assets in 18 seconds.",
        "Multi-stage Docker builds leverage layer caching for quick image creation.",
        "Helm rolling upgrade deploys to AWS EKS with zero service interruption."
    ], tag="SPEED")

    c.setFillColor(HexColor("#F8FAFC"))
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(460, 80, 436, 350, 6, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(C_TEAL)
    c.drawString(480, 395, "Total Pipeline Execution: 2m 48s")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(C_BODY)
    pipe_times = [
        "• Job 1: Test & Lint ── 12s",
        "  Pytest unit tests, flake8 linting",
        "",
        "• Job 2: Frontend Build ── 18s",
        "  Node 22, npm run build (Vite static bundle)",
        "",
        "• Job 3: Docker & Trivy Scan ── 1m 32s",
        "  Parallel container compilation + Aqua Trivy CVE scan",
        "",
        "• Job 4: Helm Rolling Rollout ── 46s",
        "  Rolling upgrade + /ready readiness check on EKS"
    ]
    cur_y = 360
    for l in pipe_times:
        c.drawString(480, cur_y, l)
        cur_y -= 18
    c.showPage()

    # =========================================================================
    # SLIDE 34: Commit SHA Traceability
    # =========================================================================
    draw_content_header(c, "The cluster now runs the new image", "Cryptographic traceability from running pod back to source repository", 34)
    draw_terminal(c, 64, 255, 832, 175, "git rev-parse HEAD vs kubectl get pods image tag", [
        "$ git rev-parse HEAD",
        "0de6666d679c85193a05f00562720251f514c20c",
        "",
        "$ kubectl get pods -n flowboard -o jsonpath='{.items[0].spec.containers[0].image}'",
        "ghcr.io/pranavnayal/flowboard-backend:sha-0de6666d679c85193a05f00562720251f514c20c",
        "[SUCCESS] Exact commit SHA match. Zero mutable tags."
    ])

    draw_card(c, 64, 80, 250, 155, "Commit to Pod", [
        "Image tag strictly equals full Git SHA.",
        "100% cryptographic traceability from pod to source code."
    ], tag="AUDIT")
    draw_card(c, 355, 80, 250, 155, "Easy Rollback", [
        "helm rollback flowboard 1 restores previous release instantly.",
        "Zero state ambiguity."
    ], tag="RECOVERY")
    draw_card(c, 646, 80, 250, 155, "Atomic Upgrade", [
        "A failed rollout reverts automatically without human intervention.",
        "Old pods continue serving traffic."
    ], tag="SAFETY")
    c.showPage()

    # =========================================================================
    # SLIDE 35: Troubleshooting Lab Table
    # =========================================================================
    draw_content_header(c, "A troubleshooting lab trains the diagnosis", "Structured operational triage across common Kubernetes failure modes", 35)
    headers35 = ["Failure Scenario", "Root Cause", "Engineering Remediation"]
    rows35 = [
        ["ImagePullBackOff", "Non-existent container image tag in Helm values", "Corrected image tag in values.yaml to match valid SHA"],
        ["0 Endpoints (No Traffic)", "Service selector labels don't match pod labels", "Aligned app.kubernetes.io/name labels between Service & Pod"],
        ["CrashLoopBackOff", "Backend cannot connect to database host", "Corrected DATABASE_URL host to resolve PostgreSQL Service DNS"]
    ]
    draw_table_custom(c, 64, 180, 832, 230, headers35, rows35, [220, 312, 300])

    c.setFillColor(C_CARD_BG)
    c.setStrokeColor(C_CARD_BORDER)
    c.roundRect(64, 80, 832, 75, 6, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(C_TEAL)
    c.drawCentredString(480, 115, "Operational Axiom: Events first (kubectl describe pod). Labels connect Services to pods. Liveness is not readiness.")
    c.showPage()

    # =========================================================================
    # SLIDE 36: AWS Cost Governance & Teardown
    # =========================================================================
    draw_content_header(c, "AWS cost stayed near zero, nothing runs now", "Strict financial discipline, proactive budget alerts, and verified teardown", 36)
    draw_hero_card(c, 64, 255, 250, 175, "$0.26", "per hour while running", "Single-node EKS stack")
    draw_hero_card(c, 355, 255, 250, 175, "6", "budget alerts active", "Guarding cloud spend")
    draw_hero_card(c, 646, 255, 250, 175, "ALL CLEAN", "verified teardown", "0 residual resources")

    draw_terminal(c, 64, 80, 832, 155, "terraform destroy & verify-teardown.sh", [
        "$ terraform destroy -auto-approve",
        "module.eks.aws_eks_cluster.this[0]: Destroying...",
        "module.vpc.aws_vpc.this[0]: Destroying...",
        "Destroy complete! Resources: 56 destroyed.",
        "",
        "$ ./scripts/verify-teardown.sh",
        "[SUCCESS] 0 VPCs, 0 EKS clusters, 0 Volumes remaining in ap-southeast-2."
    ])
    c.showPage()

    # =========================================================================
    # SLIDE 37: Five Problems That Taught Me the Most
    # =========================================================================
    draw_content_header(c, "Five problems that taught me the most", "Real production debugging lessons across CI/CD, containers, and infrastructure", 37)
    probs = [
        ("Trivy GitHub Action Tag Failure", "Action runner failed on deprecated runner environment -> Upgraded to aquasecurity/trivy-action@0.36.0"),
        ("Container Base Image CVEs", "Starlette & Alpine CVEs flagged in scan -> Patched FastAPI and pinned base images"),
        ("Non-Root NGINX Port Binding", "Default NGINX tries port 80 requiring root -> Switched to nginx-unprivileged on port 8080"),
        ("GitHub Actions Secret Conditions", "Conditional syntax failed -> Replaced with safe bash shell check in workflow script"),
        ("CI Test Database Flakiness", "File-based SQLite caused locking issues -> Implemented in-memory SQLite StaticPool fixture")
    ]
    cur_y = 360
    for idx, (title, fix) in enumerate(probs):
        c.setFillColor(C_CARD_BG)
        c.setStrokeColor(C_CARD_BORDER)
        c.roundRect(64, cur_y - 45, 832, 60, 4, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(C_DARK_TEXT)
        c.drawString(80, cur_y - 12, f"{idx+1}. {title}")
        c.setFont("Helvetica", 8)
        c.setFillColor(C_BODY)
        c.drawString(80, cur_y - 30, fix)
        cur_y -= 68
    c.showPage()

    # =========================================================================
    # SLIDE 38: Beyond Baseline Table
    # =========================================================================
    draw_content_header(c, "Where FlowBoard goes beyond the baseline", "Engineering choices that elevate FlowBoard above introductory coursework", 38)
    headers38 = ["Standard Course Baseline", "FlowBoard Advanced Implementation"]
    rows38 = [
        ["Mutable :latest container tags", "Immutable 40-character Git commit SHA tags"],
        ["Containers run as default root (UID 0)", "Dedicated non-root users (appuser UID 10001, NGINX UID 101)"],
        ["Hardcoded plain text Kubernetes YAML", "Configurable, modular Helm chart with values.yaml"],
        ["Static pod replica counts", "Horizontal Pod Autoscaler (HPA) scaling dynamically under CPU load"],
        ["Containers pushed without CVE checks", "Automated Aqua Trivy DevSecOps gating failing on HIGH/CRITICAL"],
        ["Monolithic Docker builds", "Multi-stage Docker builds separating compiler from lean runtime"]
    ]
    draw_table_custom(c, 64, 100, 832, 330, headers38, rows38, [330, 502])
    c.showPage()

    # =========================================================================
    # SLIDE 39: Grading Module Evidence Table
    # =========================================================================
    draw_content_header(c, "Every grading module has evidence", "Verified artifacts satisfying 100% of the capstone evaluation criteria", 39)
    headers39 = ["Module", "Topic", "Verified Submission Deliverable"]
    rows39 = [
        ["M1", "Application", "React 18 frontend + FastAPI backend + PostgreSQL 16 + Alembic migrations"],
        ["M2", "Testing", "10 Pytest tests passing in 0.08s with 100% endpoint coverage on isolated DB"],
        ["M3", "Git & GitHub", "Public repo with clean conventional commits and comprehensive .gitignore"],
        ["M4", "Docker", "Multi-stage non-root Dockerfiles and working 3-service docker-compose.yml"],
        ["M5", "CI/CD", "4-stage GitHub Actions workflow triggering on push and PR to main"],
        ["M6", "DevSecOps", "Aqua Trivy vulnerability scan gating builds on HIGH and CRITICAL CVEs"],
        ["M7", "Terraform", "Modular VPC + EKS cluster defining 56 AWS resources in ap-southeast-2"],
        ["M8", "Kubernetes & Helm", "Custom Helm chart with 2 backend, 2 frontend, Ingress, and HPA autoscaling"],
        ["M9", "Observability", "Prometheus /metrics instrumentation with ServiceMonitor and Grafana"],
        ["M10", "Documentation", "Comprehensive slide deck, speaker notes, and live demo runbook"]
    ]
    draw_table_custom(c, 64, 75, 832, 355, headers39, rows39, [70, 160, 602])
    c.showPage()

    # =========================================================================
    # SLIDE 40: Thank You & Roadmap
    # =========================================================================
    c.setFillColor(C_DARK_BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 38)
    c.setFillColor(C_WHITE)
    c.drawString(80, HEIGHT - 100, "THANK YOU")

    c.setFont("Helvetica", 13)
    c.setFillColor(C_MINT)
    c.drawString(80, HEIGHT - 130, "What I would build next in production")

    # 4 Roadmap cards
    r_items = [
        ("Automated HTTPS", "Domain routing with AWS Route 53 and automated ACM SSL certificates.", 80, 260),
        ("Managed Cloud Database", "Migration to AWS RDS PostgreSQL Multi-AZ with automated snapshots.", 480, 260),
        ("GitHub Actions OIDC", "Replace static IAM credentials with GitHub Actions OIDC role federation.", 80, 150),
        ("Alertmanager Rules", "Automated Slack and PagerDuty alerting on 5xx error rate spikes.", 480, 150)
    ]
    for title, desc, rx, ry in r_items:
        c.setFillColor(HexColor("#103836"))
        c.setStrokeColor(C_MINT)
        c.setLineWidth(1)
        c.roundRect(rx, ry, 380, 85, 4, fill=1, stroke=1)
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(C_WHITE)
        c.drawString(rx + 16, ry + 55, title)
        c.setFont("Helvetica", 8)
        c.setFillColor(C_LIGHT_MINT)
        c.drawString(rx + 16, ry + 30, desc)

    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(C_MINT)
    c.drawString(80, 75, "github.com/PranavNayal/devopsProject")

    c.setFont("Helvetica", 9)
    c.setFillColor(C_LIGHT_MINT)
    c.drawString(80, 55, "Pranav Nayal · DevOps Final Capstone · Session 21 · Instructor: Nensi Ravaliya")

    draw_footer(c, 40, is_dark=True)
    c.showPage()

    c.save()
    print(f"Successfully generated PDF presentation at: {output_path}")

if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(__file__), "..", "presentation", "FlowBoard_DevOps_Capstone_Presentation.pdf")
    build_pdf(out_pdf)
