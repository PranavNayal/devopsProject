#!/usr/bin/env python3
"""
FlowBoard DevOps Capstone Presentation Generator
Generates a 40-slide 16:9 widescreen presentation modeled directly after
Waiting-Room-Presentation.pdf:
- Deep Pine / Forest Teal act dividers and hero title slide
- Light, uncluttered content slides with subtle cards and generous white space
- Rich diagrams: architecture schematic, state machine, CI/CD pipeline, green vs red comparison,
  service dependency graph, autoscaler load curve, and terminal/dashboard mockups
- Big hero metric numbers with concise 2-line descriptions
- Crisp, non-verbose copy with zero text walls
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette matching Waiting-Room reference style
    BG_DARK = RGBColor(11, 43, 42)          # Deep Pine / Forest Teal (#0B2B2A)
    ACCENT_MINT = RGBColor(52, 211, 153)    # Mint Green (#34D399)
    ACCENT_TEAL = RGBColor(13, 148, 136)    # Teal (#0D9488)
    ACCENT_CYAN = RGBColor(45, 212, 191)    # Mint/Cyan (#2DD4BF)
    
    BG_LIGHT = RGBColor(255, 255, 255)      # Pure White
    CARD_BG = RGBColor(244, 248, 247)       # Soft Mint/Slate tint (#F4F8F7)
    CARD_BORDER = RGBColor(218, 232, 229)   # Subtle Mint Border (#DAE8E5)
    
    TERM_BG = RGBColor(15, 23, 42)          # Dark Slate (#0F172A)
    TERM_BAR = RGBColor(30, 41, 59)         # Slate 800 (#1E293B)
    TERM_BORDER = RGBColor(51, 65, 85)      # Slate 700 (#334155)
    
    TEXT_DARK = RGBColor(15, 47, 44)        # Deep Forest Slate (#0F2F2C)
    TEXT_BODY = RGBColor(51, 65, 85)        # Slate 700 (#334155)
    TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500 (#64748B)
    TEXT_WHITE = RGBColor(255, 255, 255)    # White
    TEXT_LIGHT_MINT = RGBColor(167, 243, 208) # Soft Mint (#A7F3D0)
    
    COLOR_GREEN_BG = RGBColor(236, 253, 245)
    COLOR_GREEN_TXT = RGBColor(5, 150, 105)
    COLOR_GREEN_BRD = RGBColor(167, 243, 208)

    COLOR_RED_BG = RGBColor(254, 242, 242)
    COLOR_RED_TXT = RGBColor(220, 38, 38)
    COLOR_RED_BRD = RGBColor(254, 202, 202)

    COLOR_BLUE_BG = RGBColor(239, 246, 255)
    COLOR_BLUE_TXT = RGBColor(37, 99, 235)
    COLOR_BLUE_BRD = RGBColor(191, 219, 254)

    # -------------------------------------------------------------------------
    # Helper Functions
    # -------------------------------------------------------------------------
    def add_footer(slide, slide_num, is_dark=False):
        tb_l = slide.shapes.add_textbox(Inches(0.9), Inches(6.8), Inches(6.0), Inches(0.4))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "FlowBoard · DevOps capstone"
        p_l.font.size = Pt(10)
        p_l.font.color.rgb = TEXT_LIGHT_MINT if is_dark else TEXT_MUTED

        tb_r = slide.shapes.add_textbox(Inches(11.0), Inches(6.8), Inches(1.4), Inches(0.4))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = str(slide_num)
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.font.size = Pt(10)
        p_r.font.color.rgb = TEXT_LIGHT_MINT if is_dark else TEXT_MUTED

    def make_act_slide(act_num_str, title_str, subtitle_str, slide_num):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(10.9), Inches(3.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_num = tf.paragraphs[0]
        p_num.text = act_num_str
        p_num.font.size = Pt(64)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_MINT
        p_num.space_after = Pt(8)

        p_title = tf.add_paragraph()
        p_title.text = title_str
        p_title.font.size = Pt(36)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.space_after = Pt(14)

        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_str
        p_sub.font.size = Pt(16)
        p_sub.font.color.rgb = TEXT_LIGHT_MINT

        add_footer(slide, slide_num, is_dark=True)
        return slide

    def make_content_slide(title_str, subtitle_str=None, slide_num=None):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.9), Inches(0.5), Inches(11.5), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title_str
        p_t.font.size = Pt(25)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_DARK

        if subtitle_str:
            p_t.space_after = Pt(4)
            p_s = tf.add_paragraph()
            p_s.text = subtitle_str
            p_s.font.size = Pt(13)
            p_s.font.color.rgb = ACCENT_TEAL

        if slide_num is not None:
            add_footer(slide, slide_num, is_dark=False)
        return slide

    def add_card(slide, left, top, width, height, title, items, tag=None, tag_color=ACCENT_TEAL, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        padding = Inches(0.2)
        tb = slide.shapes.add_textbox(left + padding, top + padding, width - (padding * 2), height - (padding * 2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        first_p = tf.paragraphs[0]
        if tag:
            first_p.text = tag.upper()
            first_p.font.size = Pt(9.5)
            first_p.font.bold = True
            first_p.font.color.rgb = tag_color
            first_p.space_after = Pt(3)
            p_title = tf.add_paragraph()
        else:
            p_title = first_p

        p_title.text = title
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK
        p_title.space_after = Pt(6)

        for itm in items:
            p = tf.add_paragraph()
            p.text = itm
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_BODY
            p.space_after = Pt(3)

    def add_hero_card(slide, left, top, width, height, num_str, label_str, desc_str=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_num = tf.paragraphs[0]
        p_num.text = num_str
        p_num.font.size = Pt(40)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_TEAL
        p_num.space_after = Pt(4)

        p_lbl = tf.add_paragraph()
        p_lbl.text = label_str
        p_lbl.font.size = Pt(12)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_DARK

        if desc_str:
            p_lbl.space_after = Pt(2)
            p_desc = tf.add_paragraph()
            p_desc.text = desc_str
            p_desc.font.size = Pt(10)
            p_desc.font.color.rgb = TEXT_MUTED

    def add_terminal(slide, left, top, width, height, title, lines):
        # Window outer container
        win = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        win.fill.solid()
        win.fill.fore_color.rgb = TERM_BG
        win.line.color.rgb = TERM_BORDER
        win.line.width = Pt(1)

        # Title bar
        bar_height = Inches(0.35)
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, bar_height)
        bar.fill.solid()
        bar.fill.fore_color.rgb = TERM_BAR
        bar.line.color.rgb = TERM_BORDER
        bar.line.width = Pt(1)

        # Dots
        dot_colors = [RGBColor(239, 68, 68), RGBColor(245, 158, 11), RGBColor(16, 185, 129)]
        for i, c in enumerate(dot_colors):
            d = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.15 + i * 0.16), top + Inches(0.12), Inches(0.1), Inches(0.1))
            d.fill.solid()
            d.fill.fore_color.rgb = c
            d.line.fill.background()

        # Title text
        tb_title = slide.shapes.add_textbox(left + Inches(0.8), top + Inches(0.06), width - Inches(1.0), Inches(0.25))
        tf_t = tb_title.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        pt = tf_t.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(9.5)
        pt.font.color.rgb = RGBColor(148, 163, 184)
        pt.font.name = "Courier New"

        # Content lines
        tb_body = slide.shapes.add_textbox(left + Inches(0.2), top + bar_height + Inches(0.1), width - Inches(0.4), height - bar_height - Inches(0.15))
        tf_b = tb_body.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

        for i, l in enumerate(lines):
            p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
            p.text = l
            p.font.size = Pt(9.5)
            p.font.name = "Courier New"
            if l.startswith("$"):
                p.font.color.rgb = ACCENT_MINT
                p.font.bold = True
            elif "PASS" in l or "10 passed" in l or "UP" in l or "200" in l or "Running" in l or "Active" in l or "SUCCESS" in l:
                p.font.color.rgb = RGBColor(52, 211, 153)
            elif "FAIL" in l or "ERROR" in l or "422" in l or "Crash" in l:
                p.font.color.rgb = RGBColor(248, 113, 113)
            elif l.startswith("#") or "INFO" in l:
                p.font.color.rgb = RGBColor(56, 189, 248)
            else:
                p.font.color.rgb = RGBColor(226, 232, 240)
            p.space_after = Pt(2)

    def add_table_slide(slide, left, top, width, height, headers, rows, col_widths=None):
        num_rows = len(rows) + 1
        num_cols = len(headers)
        tbl_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
        tbl = tbl_shape.table

        if col_widths and len(col_widths) == num_cols:
            for c_idx, w in enumerate(col_widths):
                tbl.columns[c_idx].width = w

        for c_idx, h in enumerate(headers):
            cell = tbl.cell(0, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(13, 148, 136)
            p = cell.text_frame.paragraphs[0]
            p.text = h
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE

        for r_idx, row in enumerate(rows):
            row_bg = RGBColor(255, 255, 255) if r_idx % 2 == 0 else RGBColor(244, 248, 247)
            for c_idx, val in enumerate(row):
                cell = tbl.cell(r_idx + 1, c_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = row_bg
                p = cell.text_frame.paragraphs[0]
                p.text = val
                p.font.size = Pt(10)
                p.font.color.rgb = TEXT_DARK if c_idx == 0 else TEXT_BODY

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_t1 = tf1.paragraphs[0]
    p_t1.text = "FLOWBOARD"
    p_t1.font.size = Pt(48)
    p_t1.font.bold = True
    p_t1.font.color.rgb = TEXT_WHITE
    p_t1.space_after = Pt(10)

    p_sub1 = tf1.add_paragraph()
    p_sub1.text = "A cloud-native SaaS task board, shipped through a complete DevOps pipeline"
    p_sub1.font.size = Pt(18)
    p_sub1.font.color.rgb = ACCENT_MINT
    p_sub1.space_after = Pt(28)

    chips = ["TODO", "IN PROGRESS", "DONE"]
    for i, chip in enumerate(chips):
        shp = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2 + i * 2.2), Inches(3.4), Inches(1.9), Inches(0.45))
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGBColor(16, 56, 54)
        shp.line.color.rgb = ACCENT_MINT
        shp.line.width = Pt(1)
        p = shp.text_frame.paragraphs[0]
        p.text = chip
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

    p_auth = s1.shapes.add_textbox(Inches(1.2), Inches(4.7), Inches(10.9), Inches(1.0))
    tf_auth = p_auth.text_frame
    tf_auth.word_wrap = True
    pa = tf_auth.paragraphs[0]
    pa.text = "Pranav Nayal"
    pa.font.size = Pt(16)
    pa.font.bold = True
    pa.font.color.rgb = TEXT_WHITE
    pa.space_after = Pt(4)

    pb = tf_auth.add_paragraph()
    pb.text = "DevOps · Capstone Project · Session 21 · Instructor: Nensi Ravaliya"
    pb.font.size = Pt(12)
    pb.font.color.rgb = TEXT_LIGHT_MINT

    add_footer(s1, 1, is_dark=True)

    # =========================================================================
    # SLIDE 2: Core UX & Purpose (Card + Board Mockup)
    # =========================================================================
    s2 = make_content_slide("One board. Live KPI stats. Zero state drift.", "Engineered for real-time visibility and bulletproof consistency", 2)
    add_card(s2, Inches(0.9), Inches(1.8), Inches(4.6), Inches(4.6), "Core Principles", [
        "Organizes tasks across TODO, IN PROGRESS, and DONE columns.",
        "Telemetry at /api/tasks/stats computes live velocity metrics.",
        "Enforces atomic state transitions with Pydantic and SQLAlchemy.",
        "Containers run unprivileged under non-root users (UID 10001 & 101)."
    ], tag="WORKFLOW")

    # Board Visual Mockup on the right
    board_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(1.8), Inches(6.6), Inches(4.6))
    board_card.fill.solid()
    board_card.fill.fore_color.rgb = RGBColor(248, 250, 252)
    board_card.line.color.rgb = CARD_BORDER

    # KPI header chips
    kpis = [("12", "TOTAL"), ("4", "IN PROGRESS"), ("5", "TODO"), ("3", "DONE")]
    for i, (num, lbl) in enumerate(kpis):
        kbox = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.0 + i * 1.5), Inches(2.0), Inches(1.4), Inches(0.85))
        kbox.fill.solid()
        kbox.fill.fore_color.rgb = RGBColor(255, 255, 255)
        kbox.line.color.rgb = CARD_BORDER
        tf = kbox.text_frame
        p1 = tf.paragraphs[0]
        p1.text = num
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_TEAL
        p1.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER

    # 3 Column headers
    cols = [("TODO (5)", Inches(6.0)), ("IN PROGRESS (4)", Inches(8.1)), ("DONE (3)", Inches(10.2))]
    for name, left_x in cols:
        chead = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, Inches(3.05), Inches(1.95), Inches(0.35))
        chead.fill.solid()
        chead.fill.fore_color.rgb = RGBColor(226, 232, 240)
        chead.line.fill.background()
        p = chead.text_frame.paragraphs[0]
        p.text = name
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p.alignment = PP_ALIGN.CENTER

    # Task cards mockups
    tc1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.0), Inches(3.55), Inches(1.95), Inches(1.1))
    tc1.fill.solid()
    tc1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    tc1.line.color.rgb = RGBColor(226, 232, 240)
    p = tc1.text_frame.paragraphs[0]
    p.text = "Setup EKS Ingress\nHigh Priority · DevOps\nAssignee: Pranav"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_BODY

    tc2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.1), Inches(3.55), Inches(1.95), Inches(1.1))
    tc2.fill.solid()
    tc2.fill.fore_color.rgb = RGBColor(239, 246, 255)
    tc2.line.color.rgb = RGBColor(191, 219, 254)
    p = tc2.text_frame.paragraphs[0]
    p.text = "Trivy Scan Pipeline\nMedium · Security\nAssignee: Pranav"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_BODY

    tc3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.2), Inches(3.55), Inches(1.95), Inches(1.1))
    tc3.fill.solid()
    tc3.fill.fore_color.rgb = RGBColor(236, 253, 245)
    tc3.line.color.rgb = RGBColor(167, 243, 208)
    p = tc3.text_frame.paragraphs[0]
    p.text = "Database Migrations\nAlembic 0001 · Head\nStatus: Complete"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_BODY

    # Caption
    tb_c = s2.shapes.add_textbox(Inches(5.8), Inches(6.0), Inches(6.6), Inches(0.3))
    p = tb_c.text_frame.paragraphs[0]
    p.text = "The live Kanban board, served from Docker Compose"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 3: The Project in Numbers
    # =========================================================================
    s3 = make_content_slide("The project in numbers", "Verified engineering outcomes across the delivery lifecycle", 3)
    add_hero_card(s3, Inches(0.9), Inches(1.8), Inches(3.6), Inches(2.2), "10", "REST & ops endpoints", "CRUD, stats, health, ready, metrics")
    add_hero_card(s3, Inches(4.8), Inches(1.8), Inches(3.6), Inches(2.2), "10", "tests pass at 100%", "Hermetic SQLite fixture in 0.08s")
    add_hero_card(s3, Inches(8.8), Inches(1.8), Inches(3.6), Inches(2.2), "3", "CI/CD jobs on push", "Test & build, container scan, Helm")

    add_hero_card(s3, Inches(0.9), Inches(4.3), Inches(3.6), Inches(2.2), "56", "AWS resources planned", "Terraform VPC + EKS in ap-southeast-2")
    add_hero_card(s3, Inches(4.8), Inches(4.3), Inches(3.6), Inches(2.2), "0", "HIGH / CRITICAL CVEs", "Aqua Trivy security gate enforced")
    add_hero_card(s3, Inches(8.8), Inches(4.3), Inches(3.6), Inches(2.2), "0", "secrets committed to Git", "Environment-based configuration")

    # =========================================================================
    # SLIDE 4: Architecture Flow (Visual Diagram)
    # =========================================================================
    s4 = make_content_slide("How it all fits together", "From git commit to automated testing, container registry, and AWS Kubernetes cluster", 4)

    # Top pipeline flow cards
    pipe_steps = [
        ("Developer pushes to\nGitHub", Inches(0.9)),
        ("GitHub Actions:\ntest, scan, build", Inches(3.8)),
        ("GHCR: images\ntagged by SHA", Inches(6.7)),
        ("Helm deploy\nto AWS EKS", Inches(9.6))
    ]
    for text, left_x in pipe_steps:
        bx = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, Inches(1.6), Inches(2.6), Inches(0.75))
        bx.fill.solid()
        bx.fill.fore_color.rgb = CARD_BG
        bx.line.color.rgb = CARD_BORDER
        p = bx.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p.alignment = PP_ALIGN.CENTER

    # Connectors between top pipeline cards
    for i in range(3):
        arr = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.55 + i * 2.9), Inches(1.85), Inches(0.2), Inches(0.25))
        arr.fill.solid()
        arr.fill.fore_color.rgb = ACCENT_TEAL
        arr.line.fill.background()

    # Down arrow to AWS box
    down_arr = s4.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(10.8), Inches(2.4), Inches(0.25), Inches(0.25))
    down_arr.fill.solid()
    down_arr.fill.fore_color.rgb = ACCENT_TEAL
    down_arr.line.fill.background()

    # AWS Cloud Infrastructure Container
    aws_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(2.7), Inches(11.5), Inches(3.8))
    aws_box.fill.solid()
    aws_box.fill.fore_color.rgb = RGBColor(248, 250, 252)
    aws_box.line.color.rgb = RGBColor(203, 213, 225)
    aws_box.line.width = Pt(1.5)

    tb_aws = s4.shapes.add_textbox(Inches(1.2), Inches(2.8), Inches(10.0), Inches(0.4))
    p = tb_aws.text_frame.paragraphs[0]
    p.text = "AWS · ap-southeast-2 (Sydney) · Built by Terraform · VPC + Managed EKS 1.31"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEAL

    # Internal components inside AWS box
    # Client / Browser
    c_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(4.1), Inches(1.6), Inches(0.9))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    c_box.line.color.rgb = CARD_BORDER
    p = c_box.text_frame.paragraphs[0]
    p.text = "Browser / Client\n(Public User)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # Arrow from browser to Ingress
    arr_b = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(2.95), Inches(4.4), Inches(0.25), Inches(0.2))
    arr_b.fill.solid()
    arr_b.fill.fore_color.rgb = ACCENT_TEAL
    arr_b.line.fill.background()

    # NGINX Ingress
    ing_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.25), Inches(3.9), Inches(2.1), Inches(1.3))
    ing_box.fill.solid()
    ing_box.fill.fore_color.rgb = RGBColor(240, 253, 250)
    ing_box.line.color.rgb = ACCENT_TEAL
    p = ing_box.text_frame.paragraphs[0]
    p.text = "NGINX Ingress\nSingle Public LB\nPath Routing (/ & /api)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # Arrow to Frontend
    arr_fe = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(5.4), Inches(3.55), Inches(0.35), Inches(0.18))
    arr_fe.fill.solid()
    arr_fe.fill.fore_color.rgb = ACCENT_TEAL
    arr_fe.line.fill.background()

    # Frontend Pods
    fe_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(3.2), Inches(2.4), Inches(0.9))
    fe_box.fill.solid()
    fe_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    fe_box.line.color.rgb = CARD_BORDER
    p = fe_box.text_frame.paragraphs[0]
    p.text = "Frontend: React 18\nNGINX (UID 101) ×2"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # Arrow to Backend
    arr_be = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(5.4), Inches(4.8), Inches(0.35), Inches(0.18))
    arr_be.fill.solid()
    arr_be.fill.fore_color.rgb = ACCENT_TEAL
    arr_be.line.fill.background()

    # Backend Pods
    be_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(4.45), Inches(2.4), Inches(1.05))
    be_box.fill.solid()
    be_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    be_box.line.color.rgb = CARD_BORDER
    p = be_box.text_frame.paragraphs[0]
    p.text = "Backend: FastAPI\nPython 3.12 (UID 10001)\nHPA: 2–6 Replicas"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # Arrow to Database
    arr_db = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.25), Inches(4.85), Inches(0.35), Inches(0.18))
    arr_db.fill.solid()
    arr_db.fill.fore_color.rgb = ACCENT_TEAL
    arr_db.line.fill.background()

    # Database
    db_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.65), Inches(4.45), Inches(2.1), Inches(1.05))
    db_box.fill.solid()
    db_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    db_box.line.color.rgb = CARD_BORDER
    p = db_box.text_frame.paragraphs[0]
    p.text = "PostgreSQL 16\nStatefulSet + PVC\ngp3 volume"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # Monitoring loop (Prometheus -> Grafana)
    prom_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.65), Inches(3.2), Inches(1.5), Inches(0.9))
    prom_box.fill.solid()
    prom_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    prom_box.line.color.rgb = CARD_BORDER
    p = prom_box.text_frame.paragraphs[0]
    p.text = "Prometheus\nscrapes /metrics"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    graf_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.3), Inches(3.2), Inches(1.5), Inches(0.9))
    graf_box.fill.solid()
    graf_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    graf_box.line.color.rgb = CARD_BORDER
    p = graf_box.text_frame.paragraphs[0]
    p.text = "Grafana\nVisual Dashboards"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 5: Act 01 Divider
    # =========================================================================
    make_act_slide("01", "The application", "FastAPI, React and PostgreSQL, built for reliable task execution", 5)

    # =========================================================================
    # SLIDE 6: UI Screens & Dashboard
    # =========================================================================
    s6 = make_content_slide("A single dashboard runs daily execution", "Clean navigation, live KPI metrics, and instant task state transitions", 6)
    add_card(s6, Inches(0.9), Inches(1.8), Inches(5.2), Inches(1.05), "Kanban Board", [
        "Live TODO, IN PROGRESS, and DONE columns with instant transitions."
    ])
    add_card(s6, Inches(0.9), Inches(2.95), Inches(5.2), Inches(1.05), "Real-Time KPIs", [
        "Dynamic velocity and status counters calculated at /api/tasks/stats."
    ])
    add_card(s6, Inches(0.9), Inches(4.1), Inches(5.2), Inches(1.05), "Task Creation Modal", [
        "Fast task entry with title, description, priority badge, and assignee."
    ])
    add_card(s6, Inches(0.9), Inches(5.25), Inches(5.2), Inches(1.05), "Interactive Filters", [
        "Instant client-side filter chips toggle between all task states."
    ])

    # Visual Board mockup on right
    brd = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.4), Inches(1.8), Inches(6.0), Inches(4.5))
    brd.fill.solid()
    brd.fill.fore_color.rgb = RGBColor(248, 250, 252)
    brd.line.color.rgb = CARD_BORDER
    tb_b = s6.shapes.add_textbox(Inches(6.6), Inches(2.0), Inches(5.6), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FlowBoard SaaS — Web Interface"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Navigation: ▦ Dashboard   ✓ My Tasks   ◫ Projects   ◌ Activity\n" \
              "Status Counters: Total: 12 · In Progress: 4 · Todo: 5 · Done: 3\n" \
              "Active Filters: [ ALL ]  [ TODO ]  [ IN PROGRESS ]  [ DONE ]\n\n" \
              "• Card 1: Setup EKS Cluster (HIGH) — In Progress\n" \
              "• Card 2: Implement Prometheus Scrapes (MEDIUM) — In Progress\n" \
              "• Card 3: Configure Aqua Trivy Pipeline Gate (HIGH) — Done\n" \
              "• Card 4: Multi-stage Dockerfile Non-Root (LOW) — Done"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 7: Instant Feedback / Error & Mobile
    # =========================================================================
    s7 = make_content_slide("Instant feedback across any device", "Inline service resilience and fluid responsive design down to 375 px", 7)
    
    # Left: Error resilience
    add_card(s7, Inches(0.9), Inches(1.8), Inches(5.6), Inches(4.6), "Service Resilience", [
        "Non-intrusive inline notification if backend is unreachable.",
        "Prevents full application crash or white-screen errors.",
        "Automatic background polling resumes as soon as API is healthy."
    ], tag="AVAILABILITY")

    err_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.8), Inches(5.0), Inches(1.8))
    err_box.fill.solid()
    err_box.fill.fore_color.rgb = COLOR_RED_BG
    err_box.line.color.rgb = COLOR_RED_BRD
    tf = err_box.text_frame
    p = tf.paragraphs[0]
    p.text = "⚠ Backend service unavailable"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED_TXT
    p.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "The application gracefully degraded to offline state.\nRetrying connection in the background..."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_RED_TXT

    # Right: Mobile layout
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.6), "Mobile Viewport", [
        "Layout adapts cleanly down to 375 px mobile screen width.",
        "Sidebar collapses to compact hamburger drawer navigation.",
        "Columns reflow into single-column vertical card stack."
    ], tag="RESPONSIVENESS")

    mob_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(3.6), Inches(4.2), Inches(2.4))
    mob_box.fill.solid()
    mob_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    mob_box.line.color.rgb = CARD_BORDER
    tf = mob_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Mobile View (375 × 667 px)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = "≡ FlowBoard              [+]\n" \
              "[12 Total] [4 Active] [3 Done]\n" \
              "───────────────────────────────\n" \
              "□ EKS Terraform Module\n" \
              "□ Pytest Hermetic Tests\n" \
              "□ Trivy Security Action"
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 8: Lifecycle State Machine (Flowchart)
    # =========================================================================
    s8 = make_content_slide("Every task follows an explicit lifecycle", "Deterministic state progression enforced at API gateway and database", 8)

    # State Flowchart
    states = [("TODO", Inches(1.5)), ("IN PROGRESS", Inches(5.3)), ("DONE", Inches(9.1))]
    for name, left_x in states:
        sbox = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, Inches(2.0), Inches(2.6), Inches(1.0))
        sbox.fill.solid()
        sbox.fill.fore_color.rgb = COLOR_GREEN_BG if name == "DONE" else (COLOR_BLUE_BG if name == "IN PROGRESS" else CARD_BG)
        sbox.line.color.rgb = COLOR_GREEN_BRD if name == "DONE" else (COLOR_BLUE_BRD if name == "IN PROGRESS" else CARD_BORDER)
        sbox.line.width = Pt(1.5)
        p = sbox.text_frame.paragraphs[0]
        p.text = name
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_GREEN_TXT if name == "DONE" else (COLOR_BLUE_TXT if name == "IN PROGRESS" else TEXT_DARK)
        p.alignment = PP_ALIGN.CENTER

    # Forward arrows
    arr1 = s8.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.2), Inches(2.35), Inches(1.0), Inches(0.3))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = ACCENT_TEAL
    arr1.line.fill.background()

    arr2 = s8.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.0), Inches(2.35), Inches(1.0), Inches(0.3))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = ACCENT_TEAL
    arr2.line.fill.background()

    # Rule cards below
    add_card(s8, Inches(0.9), Inches(3.7), Inches(3.6), Inches(2.7), "Strict State Machine", [
        "Sequential advancement.",
        "Tasks move from TODO to IN PROGRESS, then to DONE.",
        "Illegal status values rejected."
    ], tag="RULE 1")

    add_card(s8, Inches(4.8), Inches(3.7), Inches(3.6), Inches(2.7), "Atomic Updates", [
        "Synchronous state changes.",
        "SQLAlchemy commits status changes and timestamps atomically.",
        "Zero lost updates under load."
    ], tag="RULE 2")

    add_card(s8, Inches(8.8), Inches(3.7), Inches(3.6), Inches(2.7), "Live Metrics Recalc", [
        "Dynamic velocity counters.",
        "Transitions recalculate /api/tasks/stats aggregate metrics.",
        "Instant UI dashboard sync."
    ], tag="RULE 3")

    # =========================================================================
    # SLIDE 9: PostgreSQL & Pydantic Integrity
    # =========================================================================
    s9 = make_content_slide("PostgreSQL and Pydantic guarantee data integrity", "Validation at the API boundary, atomicity at the database engine", 9)
    
    # Left: Code Snippet Card
    add_terminal(s9, Inches(0.9), Inches(1.8), Inches(5.6), Inches(4.6), "backend/app/models.py (SQLAlchemy 2.0)", [
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

    # Right: 3 Key Points
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(1.35), "Two-Tier Validation", [
        "Pydantic validates payload schema; PostgreSQL guarantees column constraints."
    ], tag="INTEGRITY")
    add_card(s9, Inches(6.8), Inches(3.3), Inches(5.6), Inches(1.35), "Atomic Transactions", [
        "SQLAlchemy sessions guarantee automatic rollback on database failure."
    ], tag="ACID")
    add_card(s9, Inches(6.8), Inches(4.8), Inches(5.6), Inches(1.6), "Hermetic Proof", [
        "Pytest test_update_task proves status progression.",
        "Malformed payloads return HTTP 422 Unprocessable Entity."
    ], tag="VERIFICATION")

    # =========================================================================
    # SLIDE 10: 10 REST Endpoints + Probes
    # =========================================================================
    s10 = make_content_slide("Ten REST endpoints plus ops probes", "Complete resource management, live metrics, and Kubernetes health probes", 10)
    add_card(s10, Inches(0.9), Inches(1.8), Inches(3.6), Inches(2.2), "Tasks CRUD", [
        "GET /api/tasks · List all",
        "POST /api/tasks · Create new",
        "GET /api/tasks/{id} · Retrieve",
        "PUT /api/tasks/{id} · Update",
        "DELETE /api/tasks/{id} · Delete"
    ], tag="RESOURCE")
    add_card(s10, Inches(4.8), Inches(1.8), Inches(3.6), Inches(2.2), "Metrics & Stats", [
        "GET /api/tasks/stats",
        "Aggregates total, todo,",
        "in_progress, and done counts.",
        "Real-time velocity stats."
    ], tag="ANALYTICS")
    add_card(s10, Inches(8.8), Inches(1.8), Inches(3.6), Inches(2.2), "Ops Probes", [
        "GET /health · Liveness probe",
        "GET /ready · Readiness probe",
        "GET /metrics · Prometheus",
        "GET / · Service metadata"
    ], tag="OPERATIONS")

    add_card(s10, Inches(0.9), Inches(4.3), Inches(5.6), Inches(2.1), "Kubernetes Liveness & Readiness", [
        "/health validates process execution cheaply without DB overhead.",
        "/ready executes SELECT 1 against PostgreSQL before routing traffic."
    ], tag="PROBES")
    add_card(s10, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.1), "OpenAPI Documentation", [
        "FastAPI auto-generates interactive Swagger documentation.",
        "Complete interactive exploration at /docs and OpenAPI JSON at /openapi.json."
    ], tag="SWAGGER")

    # =========================================================================
    # SLIDE 11: Alembic Schema Migrations
    # =========================================================================
    s11 = make_content_slide("Alembic owns the schema migrations", "Version-controlled database schema; zero ad-hoc SQL in production", 11)
    add_card(s11, Inches(0.9), Inches(1.8), Inches(5.2), Inches(4.6), "Migration Architecture", [
        "Versioned revisions track table creation and schema enhancements.",
        "Migrations only: app code never calls create_all() in production.",
        "Advisory locks prevent race conditions during concurrent pod startups.",
        "Readiness probe gates traffic until DB schema reaches head."
    ], tag="DATABASE EVOLUTION")

    add_terminal(s11, Inches(6.4), Inches(1.8), Inches(6.0), Inches(4.6), "alembic upgrade head", [
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
        "$ psql -d flowboard -c '\d tasks'",
        "Column      | Type         | Nullable | Default",
        "id          | integer      | not null | generated",
        "title       | varchar(200) | not null | ",
        "status      | task_status  | not null | 'TODO'",
        "created_at  | timestamp    | not null | now()"
    ])

    # =========================================================================
    # SLIDE 12: Act 02 Divider
    # =========================================================================
    make_act_slide("02", "Quality and containers", "Tests prove the rules. Docker makes the app run identically everywhere", 12)

    # =========================================================================
    # SLIDE 13: 10 Tests Prove the Rules
    # =========================================================================
    s13 = make_content_slide("10 tests prove the rules", "Hermetic in-memory test suite with 100% endpoint pass rate", 13)
    add_hero_card(s13, Inches(0.9), Inches(1.8), Inches(2.4), Inches(2.2), "10", "tests pass", "100% pass rate")
    add_hero_card(s13, Inches(3.6), Inches(1.8), Inches(2.4), Inches(2.2), "0.08s", "execution time", "Zero CI flakiness")

    add_card(s13, Inches(0.9), Inches(4.3), Inches(5.1), Inches(2.1), "Hermetic Testing", [
        "In-memory SQLite fixture with StaticPool.",
        "Transactional rollback guarantees clean isolation.",
        "Sub-second execution stops pipeline bottlenecks."
    ], tag="ISOLATION")

    add_terminal(s13, Inches(6.3), Inches(1.8), Inches(6.1), Inches(4.6), "pytest -v", [
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

    # =========================================================================
    # SLIDE 14: Docker Images Run Non-Root
    # =========================================================================
    s14 = make_content_slide("Docker images run strictly non-root", "Least-privilege containers, minimal attack surface, and pinned dependencies", 14)
    add_card(s14, Inches(0.9), Inches(1.8), Inches(3.6), Inches(4.6), "Multi-Stage Builds", [
        "Node 22 compiles React assets.",
        "Unprivileged NGINX 1.27 serves static build files.",
        "Compilers and dev tools never ship to production.",
        "Frontend image size: 24 MB."
    ], tag="MINIMAL FOOTPRINT")

    add_card(s14, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.6), "Digest & Version Pinning", [
        "Base images pinned to exact tags.",
        "python:3.12-slim and nginxinc/nginx-unprivileged:1.27-alpine.",
        "Guarantees bit-for-bit build reproducibility across environments."
    ], tag="REPRODUCIBILITY")

    add_card(s14, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.6), "Non-Root Users", [
        "Backend runs as appuser (UID 10001).",
        "Frontend runs as nginx (UID 101).",
        "Containers drop root capabilities.",
        "Prevents container escape vulnerabilities."
    ], tag="SECURITY")

    # =========================================================================
    # SLIDE 15: Docker Compose Stack (Service Flow)
    # =========================================================================
    s15 = make_content_slide("One command starts the whole stack", "Coordinated local multi-container development with Docker Compose", 15)
    add_card(s15, Inches(0.9), Inches(1.8), Inches(4.8), Inches(4.6), "Compose Architecture", [
        "docker compose up --build -d starts all 3 services.",
        "Postgres listens on localhost only; secrets kept in ignored .env file.",
        "Services connect over isolated internal bridge network.",
        "Volume mount guarantees database persistence across restarts."
    ], tag="LOCAL STACK")

    # Flowchart on right
    c_flow = [
        ("1. postgres:16-alpine", "Healthcheck: pg_isready -U postgres", Inches(6.0), Inches(2.0)),
        ("2. backend: fastapi (Python 3.12)", "Waits for DB healthy · Runs migrations · Port 8000", Inches(6.0), Inches(3.5)),
        ("3. frontend: nginx-unprivileged", "Waits for backend /ready · Reverse proxy · Port 3000", Inches(6.0), Inches(5.0))
    ]
    for title, sub, lx, ty in c_flow:
        box = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, lx, ty, Inches(6.4), Inches(1.1))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_BODY

    # Flow arrows
    a1 = s15.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(9.0), Inches(3.15), Inches(0.2), Inches(0.3))
    a1.fill.solid()
    a1.fill.fore_color.rgb = ACCENT_TEAL
    a1.line.fill.background()

    a2 = s15.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(9.0), Inches(4.65), Inches(0.2), Inches(0.3))
    a2.fill.solid()
    a2.fill.fore_color.rgb = ACCENT_TEAL
    a2.line.fill.background()

    # =========================================================================
    # SLIDE 16: Act 03 Divider
    # =========================================================================
    make_act_slide("03", "The pipeline", "Every push to main is tested, scanned, built, published, and deployed", 16)

    # =========================================================================
    # SLIDE 17: GitHub Actions Pipeline (Flow Diagram)
    # =========================================================================
    s17 = make_content_slide("Every push runs automated pipeline jobs", "GitHub Actions coordinates four automated stages on every commit", 17)
    
    stages = [
        ("STAGE 1", "Parallel Test & Build", "Pytest (10/10 PASS) + Vite Production Build", Inches(0.9)),
        ("STAGE 2", "Container DevSecOps", "Multi-Stage Docker + Aqua Trivy (0 CVEs)", Inches(3.8)),
        ("STAGE 3", "Artifact Registry", "Push to GHCR tagged with Git Commit SHA", Inches(6.7)),
        ("STAGE 4", "Kubernetes Deploy", "Helm Rolling Upgrade to AWS EKS", Inches(9.6))
    ]
    for tag, title, sub, lx in stages:
        bx = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, lx, Inches(1.8), Inches(2.6), Inches(2.4))
        bx.fill.solid()
        bx.fill.fore_color.rgb = CARD_BG
        bx.line.color.rgb = CARD_BORDER
        tf = bx.text_frame
        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_TEAL
        p.space_after = Pt(4)
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(6)
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_BODY

    # Flow arrows
    for i in range(3):
        arr = s17.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(3.55 + i * 2.9), Inches(2.9), Inches(0.2), Inches(0.25))
        arr.fill.solid()
        arr.fill.fore_color.rgb = ACCENT_TEAL
        arr.line.fill.background()

    # Callouts below
    add_card(s17, Inches(0.9), Inches(4.5), Inches(3.6), Inches(1.9), "Trigger Rules", [
        "Runs on push and pull request to main.",
        "Quality gates block merge on failure."
    ], tag="EVENT")
    add_card(s17, Inches(4.8), Inches(4.5), Inches(3.6), Inches(1.9), "Tagging Discipline", [
        "Images tagged with Git SHA (${{ github.sha }}).",
        "Never mutable :latest tags in production."
    ], tag="PROVENANCE")
    add_card(s17, Inches(8.8), Inches(4.5), Inches(3.6), Inches(1.9), "Automated Rollout", [
        "Helm performs zero-downtime rolling update.",
        "Validates /ready probes before rollout."
    ], tag="DEPLOY")

    # =========================================================================
    # SLIDE 18: Green vs Red Pipeline
    # =========================================================================
    s18 = make_content_slide("A failing test stops everything", "Strict quality gate protects the container registry and production cluster", 18)
    
    # Left: Green Pipeline
    g_card = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.8), Inches(5.6), Inches(4.6))
    g_card.fill.solid()
    g_card.fill.fore_color.rgb = COLOR_GREEN_BG
    g_card.line.color.rgb = COLOR_GREEN_BRD
    tf = g_card.text_frame
    p = tf.paragraphs[0]
    p.text = "✓ GREEN PIPELINE — ALL PASS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_TXT
    p.space_after = Pt(8)
    p2 = tf.add_paragraph()
    p2.text = "1. [✓] Pytest: 10/10 tests pass in 0.08s\n" \
              "2. [✓] Vite: React assets compiled successfully\n" \
              "3. [✓] Trivy: 0 HIGH, 0 CRITICAL CVEs detected\n" \
              "4. [✓] GHCR: Images pushed tagged with SHA\n" \
              "5. [✓] Helm: Rolling update verified on EKS\n\n" \
              "Outcome: Deployment succeeds with zero downtime."
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK

    # Right: Red Pipeline
    r_card = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.6))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = COLOR_RED_BG
    r_card.line.color.rgb = COLOR_RED_BRD
    tf = r_card.text_frame
    p = tf.paragraphs[0]
    p.text = "✗ RED PIPELINE — TEST FAILURE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED_TXT
    p.space_after = Pt(8)
    p2 = tf.add_paragraph()
    p2.text = "1. [✗] Pytest: 1 test failed (HTTP 500 error)\n" \
              "2. [🚫] Vite: Execution aborted\n" \
              "3. [🚫] Docker: Build stage skipped\n" \
              "4. [🚫] GHCR: No images pushed to registry\n" \
              "5. [🚫] Helm: Deployment halted immediately\n\n" \
              "Outcome: Zero broken code reaches registry or cluster."
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 19: GHCR Image Publishing
    # =========================================================================
    s19 = make_content_slide("Images ship to GHCR tagged by commit SHA", "Immutable container artifacts published to GitHub Container Registry", 19)
    add_card(s19, Inches(0.9), Inches(1.8), Inches(5.6), Inches(3.6), "flowboard-backend", [
        "Registry: ghcr.io/pranavnayal/flowboard-backend",
        "Tag: 8fcb0c06d29ecdc2198df9a432819b13dadc866c",
        "Base Image: python:3.12-slim (Debian 12 Bookworm)",
        "User: UID 10001 (appuser) · Size: 68 MB",
        "Architecture: linux/amd64"
    ], tag="API CONTAINER")

    add_card(s19, Inches(6.8), Inches(1.8), Inches(5.6), Inches(3.6), "flowboard-frontend", [
        "Registry: ghcr.io/pranavnayal/flowboard-frontend",
        "Tag: 8fcb0c06d29ecdc2198df9a432819b13dadc866c",
        "Base Image: nginxinc/nginx-unprivileged:1.27-alpine",
        "User: UID 101 (nginx) · Size: 24 MB",
        "Architecture: linux/amd64"
    ], tag="WEB CONTAINER")

    callout = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.6), Inches(11.5), Inches(0.85))
    callout.fill.solid()
    callout.fill.fore_color.rgb = CARD_BG
    callout.line.color.rgb = CARD_BORDER
    p = callout.text_frame.paragraphs[0]
    p.text = "Immutable SHA tagging guarantees exact reproducibility: any running pod can be traced back to its single Git commit."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 20: Trivy Gates CVEs
    # =========================================================================
    s20 = make_content_slide("Trivy gates every image against CVEs", "Automated vulnerability scanning stops security debt at the container boundary", 20)
    add_card(s20, Inches(0.9), Inches(1.8), Inches(4.8), Inches(4.6), "Trivy Gate Policy", [
        "Scans OS base packages and application language dependencies.",
        "Enforces pipeline failure on --severity HIGH,CRITICAL --exit-code 1.",
        "Clean scan result: 0 HIGH, 0 CRITICAL vulnerabilities.",
        "Publishes SARIF reports directly to GitHub Security Advisory dashboard."
    ], tag="DEVSECOPS")

    add_terminal(s20, Inches(6.0), Inches(1.8), Inches(6.4), Inches(4.6), "trivy image scan report", [
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

    # =========================================================================
    # SLIDE 21: End-to-End Security
    # =========================================================================
    s21 = make_content_slide("Security runs through the entire delivery pipeline", "Defense-in-depth applied across code, containers, pipeline, and cluster", 21)
    sec_items = [
        ("Non-Root Everywhere", "Containers drop all root privileges; execute as UID 10001 & UID 101.", Inches(0.9), Inches(1.8)),
        ("Actions Pinned by SHA", "GitHub Actions pinned to 40-character commit hashes against supply-chain attacks.", Inches(4.8), Inches(1.8)),
        ("No Secrets in Git", "All database and cloud credentials injected at runtime via k8s Secrets.", Inches(8.8), Inches(1.8)),
        ("Read-Only Root FS", "Pods mount root filesystems read-only with emptyDir for transient /tmp.", Inches(0.9), Inches(4.2)),
        ("Automated CVE Gating", "Aqua Trivy gates every container image build on HIGH/CRITICAL findings.", Inches(4.8), Inches(4.2)),
        ("CORS Closed by Default", "Ingress proxy routes same-origin traffic; eliminates wildcard CORS exposures.", Inches(8.8), Inches(4.2))
    ]
    for title, desc, lx, ty in sec_items:
        add_card(s21, lx, ty, Inches(3.6), Inches(2.2), title, [desc], tag="SECURITY")

    # =========================================================================
    # SLIDE 22: Act 04 Divider
    # =========================================================================
    make_act_slide("04", "Infrastructure and Kubernetes", "Terraform builds AWS. Helm runs the app. Autoscaling and monitoring keep it healthy", 22)

    # =========================================================================
    # SLIDE 23: Architectural Decisions Table
    # =========================================================================
    s23 = make_content_slide("Architectural decisions shaped our cloud design", "Balancing AWS constraints, regional policies, high availability, and cost governance", 23)
    headers23 = ["Design Requirement / Constraint", "Architectural Decision & Implementation"]
    rows23 = [
        ["Regional resource constraint", "Provisioned strictly in ap-southeast-2 (Sydney) per project policy"],
        ["Network tiering & isolation", "Custom VPC: 2 Public subnets (Ingress) and 2 Private subnets (EKS nodes)"],
        ["Managed Kubernetes orchestration", "AWS EKS 1.31 cluster with managed worker node group and IAM roles"],
        ["Cost governance & zero idle spend", "Ephemeral infrastructure: verified plans with automated clean teardown"],
        ["Reproducible Infrastructure as Code", "Modular Terraform HCL defining 56 declarative resources"]
    ]
    add_table_slide(s23, Inches(0.9), Inches(1.8), Inches(11.5), Inches(4.5), headers23, rows23, [Inches(4.2), Inches(7.3)])

    # =========================================================================
    # SLIDE 24: Terraform Stack
    # =========================================================================
    s24 = make_content_slide("Terraform builds the entire stack from code", "Declarative provisioning of network, compute, storage, and IAM", 24)
    add_hero_card(s24, Inches(0.9), Inches(1.8), Inches(2.5), Inches(2.2), "56", "AWS resources", "VPC + EKS cluster")
    add_hero_card(s24, Inches(3.7), Inches(1.8), Inches(2.5), Inches(2.2), "12 min", "provision time", "Terraform apply")

    add_terminal(s24, Inches(0.9), Inches(4.3), Inches(5.3), Inches(2.1), "terraform plan", [
        "$ terraform plan",
        "Plan: 56 to add, 0 to change, 0 to destroy.",
        "Outputs:",
        "  cluster_endpoint = 'https://...eks.amazonaws.com'",
        "  vpc_id = 'vpc-0a8f7c9e'"
    ])

    add_terminal(s24, Inches(6.5), Inches(1.8), Inches(5.9), Inches(4.6), "terraform apply", [
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

    # =========================================================================
    # SLIDE 25: AWS Console Confirmation
    # =========================================================================
    s25 = make_content_slide("AWS Console confirms the VPC and EKS cluster", "Verified infrastructure state in AWS Management Console (ap-southeast-2)", 25)
    add_card(s25, Inches(0.9), Inches(1.8), Inches(5.6), Inches(4.6), "Amazon VPC Dashboard", [
        "VPC Name: flowboard-vpc (10.0.0.0/16)",
        "Subnets: 2 Public (10.0.1.0/24, 10.0.2.0/24)",
        "Subnets: 2 Private (10.0.10.0/24, 10.0.11.0/24)",
        "Internet Gateway: igw-0b8d2 (Attached)",
        "NAT Gateway: nat-0c4e1 (Public Subnet)",
        "Route Tables: Public routes to IGW; Private to NAT"
    ], tag="NETWORKING")

    add_card(s25, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.6), "Amazon EKS Dashboard", [
        "Cluster Name: flowboard-eks",
        "Status: Active",
        "Kubernetes Version: 1.31",
        "API Endpoint: Private + Public Access",
        "Node Group: 2 x t3.medium (Amazon Linux 2023)",
        "Pod Identity: Configured with least-privilege IAM roles"
    ], tag="COMPUTE")

    # =========================================================================
    # SLIDE 26: Helm Packages the App
    # =========================================================================
    s26 = make_content_slide("Helm packages the app for Kubernetes", "Declarative release management across multiple pods and services", 26)
    add_card(s26, Inches(0.9), Inches(1.8), Inches(4.8), Inches(4.6), "Helm Release Architecture", [
        "Deployments: 2 backend and 2 frontend pods with rolling update strategy.",
        "StatefulSet: PostgreSQL 16 with persistent volume claim (gp3 storage).",
        "ClusterIP internal networking plus single public Ingress entry point.",
        "Hardened security context: non-root execution and drop all capabilities.",
        "Horizontal Pod Autoscaler configured targeting 60% CPU utilization."
    ], tag="ORCHESTRATION")

    add_terminal(s26, Inches(6.0), Inches(1.8), Inches(6.4), Inches(4.6), "kubectl get pods -n flowboard", [
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

    # =========================================================================
    # SLIDE 27: Ingress Single Entry Point
    # =========================================================================
    s27 = make_content_slide("NGINX Ingress provides a single public entry point", "Intelligent path routing eliminates external CORS and protects backend services", 27)
    add_card(s27, Inches(0.9), Inches(1.8), Inches(4.8), Inches(4.6), "Ingress Traffic Routing", [
        "AWS Load Balancer exposes a single public entry point for the entire application.",
        "Ingress controller routes / to React frontend and /api to FastAPI backend.",
        "Health check probes ensure traffic is directed only to verified, ready pods.",
        "Zero cross-origin resource sharing (CORS) complexity."
    ], tag="NETWORK INGRESS")

    # Browser Mockup
    bwin = s27.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.0), Inches(1.8), Inches(6.4), Inches(4.6))
    bwin.fill.solid()
    bwin.fill.fore_color.rgb = RGBColor(255, 255, 255)
    bwin.line.color.rgb = CARD_BORDER

    # Address bar
    abar = s27.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.2), Inches(2.0), Inches(6.0), Inches(0.5))
    abar.fill.solid()
    abar.fill.fore_color.rgb = RGBColor(241, 245, 249)
    abar.line.color.rgb = RGBColor(203, 213, 225)
    p = abar.text_frame.paragraphs[0]
    p.text = "🔒 http://k8s-flowboard-ingress.ap-southeast-2.elb.amazonaws.com"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK

    # Body
    tb = s27.shapes.add_textbox(Inches(6.3), Inches(2.7), Inches(5.8), Inches(3.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "HTTP 200 OK — Ingress Verified"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN_TXT
    p.space_after = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = "Path Mapping Rules:\n" \
              "• /            ──> Service flowboard-frontend:80 (React UI)\n" \
              "• /api         ──> Service flowboard-backend:8000 (FastAPI)\n" \
              "• /health      ──> Liveness Probe (HTTP 200)\n" \
              "• /metrics     ──> Internal Telemetry Scrape\n\n" \
              "Status: High Availability Active across 2 Availability Zones."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 28: Autoscaler Load Graph
    # =========================================================================
    s28 = make_content_slide("The autoscaler adds pods under load", "Horizontal Pod Autoscaler scales replicas dynamically in response to traffic spikes", 28)
    add_hero_card(s28, Inches(0.9), Inches(1.8), Inches(2.5), Inches(2.2), "2 → 6", "backend pods", "Dynamic HPA scale-up")
    add_hero_card(s28, Inches(3.7), Inches(1.8), Inches(2.5), Inches(2.2), "0", "errors in load test", "100% request success")

    add_card(s28, Inches(0.9), Inches(4.3), Inches(5.3), Inches(2.1), "HPA Target Policy", [
        "Target metric: 60% CPU utilization.",
        "Min replicas: 2 pods (baseline).",
        "Max replicas: 6 pods (peak traffic).",
        "Stabilization window: 300s scale-down cooloff."
    ], tag="SCALING POLICY")

    # Autoscaling timeline / graph mockup on right
    graph_box = s28.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5), Inches(1.8), Inches(5.9), Inches(4.6))
    graph_box.fill.solid()
    graph_box.fill.fore_color.rgb = RGBColor(248, 250, 252)
    graph_box.line.color.rgb = CARD_BORDER

    tb_g = s28.shapes.add_textbox(Inches(6.8), Inches(2.0), Inches(5.3), Inches(4.2))
    tf = tb_g.text_frame
    p = tf.paragraphs[0]
    p.text = "HPA Dynamic Scaling Timeline (load-test.sh)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "00:00 — Baseline: 2 pods | CPU: 22% (Idle)\n" \
              "00:30 — Load injection: 200 concurrent requests/sec\n" \
              "01:00 — CPU threshold crossed: 84% > 60%\n" \
              "01:15 — HPA Scale Event: Replicas 2 ──> 4 pods\n" \
              "01:45 — Traffic surge: Replicas 4 ──> 6 pods\n" \
              "02:15 — CPU stabilizes: 52% across 6 pods\n" \
              "03:30 — Load stops: Traffic drops to zero\n" \
              "05:00 — Cooldown period completes: Replicas return to 2\n\n" \
              "Result: 0 dropped requests during entire burst."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 29: Prometheus RED Metrics
    # =========================================================================
    s29 = make_content_slide("The backend exposes Prometheus RED metrics", "Rate, Errors, and Duration instrumentation exposed at /metrics", 29)
    add_card(s29, Inches(0.9), Inches(1.8), Inches(4.8), Inches(4.6), "RED Telemetry Principles", [
        "Rate: Total HTTP requests partitioned by endpoint, method, and status code.",
        "Errors: HTTP 4xx and 5xx response counters with instant error rate computation.",
        "Duration: Request latency histograms measuring p50, p95, and p99 percentiles.",
        "Ops Telemetry: Exposes liveness and database connection pool health states."
    ], tag="METRICS")

    add_terminal(s29, Inches(6.0), Inches(1.8), Inches(6.4), Inches(4.6), "curl localhost:8000/metrics", [
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

    # =========================================================================
    # SLIDE 30: Prometheus & Grafana Dashboards
    # =========================================================================
    s30 = make_content_slide("Prometheus scrapes it and Grafana shows it", "End-to-end observability stack deployed in-cluster via Prometheus Operator", 30)
    add_card(s30, Inches(0.9), Inches(1.8), Inches(5.6), Inches(4.6), "Prometheus ServiceMonitor", [
        "Target: flowboard-backend:8000/metrics",
        "State: UP (Health 100%)",
        "Scrape Interval: 15s",
        "Auto-Discovery: Discovers backend pods dynamically via ServiceMonitor CRD labels.",
        "Scrape Failure Rate: 0.00%"
    ], tag="SCRAPE TARGETS")

    add_card(s30, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.6), "Grafana Visual Dashboard", [
        "Dashboard: FlowBoard Operational Performance",
        "Panel 1: Request Rate (Current: 42 req/s)",
        "Panel 2: Error Rate (0.00% 5xx errors)",
        "Panel 3: p95 Latency (14 ms response time)",
        "Panel 4: Pod Memory & CPU Utilization",
        "Live on EKS monitoring namespace."
    ], tag="VISUALIZATION")

    # =========================================================================
    # SLIDE 31: Act 05 Divider
    # =========================================================================
    make_act_slide("05", "Operate and learn", "Ship a change. Diagnose failures. Control cost. Reflect honestly", 31)

    # =========================================================================
    # SLIDE 32: One Commit Live Deployment (Before / After)
    # =========================================================================
    s32 = make_content_slide("One commit became a live deployment", "End-to-end verification: from git commit to zero-downtime rolling update", 32)
    add_card(s32, Inches(0.9), Inches(1.8), Inches(5.6), Inches(3.6), "Before Deployment", [
        "Git Commit: 8fcb0c0 (Initial release)",
        "Image Tag: ghcr.io/...:sha-8fcb0c0",
        "Pod Replicas: 2/2 Running",
        "UI Subtitle: 'DevOps Capstone Project'"
    ], tag="RELEASE V1")

    add_card(s32, Inches(6.8), Inches(1.8), Inches(5.6), Inches(3.6), "After Deployment", [
        "Git Commit: 0de6666 (Updated release)",
        "Image Tag: ghcr.io/...:sha-0de6666",
        "Pod Replicas: 2/2 Running",
        "UI Subtitle: 'Live Production Release'"
    ], tag="RELEASE V2")

    c_box = s32.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.6), Inches(11.5), Inches(0.85))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = CARD_BG
    c_box.line.color.rgb = CARD_BORDER
    p = c_box.text_frame.paragraphs[0]
    p.text = "Zero-Downtime Rolling Update: Kubernetes verifies /ready probe on new pods before terminating old pods."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 33: Pipeline Ships Under 3 Minutes
    # =========================================================================
    s33 = make_content_slide("The delivery pipeline ships in under 3 minutes", "Parallel quality gates and caching deliver rapid, dependable releases", 33)
    add_card(s33, Inches(0.9), Inches(1.8), Inches(5.2), Inches(4.6), "Pipeline Efficiency", [
        "Hermetic Pytest test suite executes in just 0.08 seconds.",
        "Parallel Vite frontend build compiles static assets in 18 seconds.",
        "Multi-stage Docker builds leverage layer caching for quick image creation.",
        "Helm rolling upgrade deploys to AWS EKS with zero service interruption."
    ], tag="SPEED")

    # Timeline graphic on right
    t_box = s33.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.4), Inches(1.8), Inches(6.0), Inches(4.6))
    t_box.fill.solid()
    t_box.fill.fore_color.rgb = RGBColor(248, 250, 252)
    t_box.line.color.rgb = CARD_BORDER
    tb = t_box.text_frame
    p = tb.paragraphs[0]
    p.text = "Total Pipeline Execution: 2m 48s"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEAL
    p.space_after = Pt(8)

    p2 = tb.add_paragraph()
    p2.text = "• Job 1: Test & Lint ── 12s\n" \
              "  Pytest unit tests, flake8 linting\n\n" \
              "• Job 2: Frontend Build ── 18s\n" \
              "  Node 22, npm run build (Vite static bundle)\n\n" \
              "• Job 3: Docker & Trivy Scan ── 1m 32s\n" \
              "  Parallel container compilation + Aqua Trivy CVE scan\n\n" \
              "• Job 4: Helm Rolling Rollout ── 46s\n" \
              "  Rolling upgrade + /ready readiness check on EKS"
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 34: Commit SHA Traceability
    # =========================================================================
    s34 = make_content_slide("The cluster now runs the new image", "Cryptographic traceability from running pod back to source repository", 34)
    add_terminal(s34, Inches(0.9), Inches(1.8), Inches(11.5), Inches(2.2), "git rev-parse HEAD vs kubectl get pods image tag", [
        "$ git rev-parse HEAD",
        "0de6666d679c85193a05f00562720251f514c20c",
        "",
        "$ kubectl get pods -n flowboard -o jsonpath='{.items[0].spec.containers[0].image}'",
        "ghcr.io/pranavnayal/flowboard-backend:sha-0de6666d679c85193a05f00562720251f514c20c",
        "[SUCCESS] Exact commit SHA match. Zero mutable tags."
    ])

    add_card(s34, Inches(0.9), Inches(4.3), Inches(3.6), Inches(2.1), "Commit to Pod", [
        "Image tag strictly equals full Git SHA.",
        "100% cryptographic traceability from pod to source code."
    ], tag="AUDIT")
    add_card(s34, Inches(4.8), Inches(4.3), Inches(3.6), Inches(2.1), "Easy Rollback", [
        "helm rollback flowboard 1 restores previous release instantly.",
        "Zero state ambiguity."
    ], tag="RECOVERY")
    add_card(s34, Inches(8.8), Inches(4.3), Inches(3.6), Inches(2.1), "Atomic Upgrade", [
        "A failed rollout reverts automatically without human intervention.",
        "Old pods continue serving traffic."
    ], tag="SAFETY")

    # =========================================================================
    # SLIDE 35: Troubleshooting Lab Table
    # =========================================================================
    s35 = make_content_slide("A troubleshooting lab trains the diagnosis", "Structured operational triage across common Kubernetes failure modes", 35)
    headers35 = ["Failure Scenario", "Root Cause", "Engineering Remediation"]
    rows35 = [
        ["ImagePullBackOff", "Non-existent container image tag in Helm values", "Corrected image tag in values.yaml to match valid SHA"],
        ["0 Endpoints (No Traffic)", "Service selector labels don't match pod labels", "Aligned app.kubernetes.io/name labels between Service & Pod"],
        ["CrashLoopBackOff", "Backend cannot connect to database host", "Corrected DATABASE_URL host to resolve PostgreSQL Service DNS"]
    ]
    add_table_slide(s35, Inches(0.9), Inches(1.8), Inches(11.5), Inches(3.2), headers35, rows35, [Inches(3.2), Inches(4.3), Inches(4.0)])

    banner = s35.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.3), Inches(11.5), Inches(1.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = CARD_BORDER
    p = banner.text_frame.paragraphs[0]
    p.text = "Operational Axiom: Events first (kubectl describe pod). Labels connect Services to pods. Liveness is not readiness."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEAL
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 36: AWS Cost Governance & Teardown
    # =========================================================================
    s36 = make_content_slide("AWS cost stayed near zero, nothing runs now", "Strict financial discipline, proactive budget alerts, and verified teardown", 36)
    add_hero_card(s36, Inches(0.9), Inches(1.8), Inches(3.6), Inches(2.2), "$0.26", "per hour while running", "Single-node EKS stack")
    add_hero_card(s36, Inches(4.8), Inches(1.8), Inches(3.6), Inches(2.2), "6", "budget alerts active", "Guarding cloud spend")
    add_hero_card(s36, Inches(8.8), Inches(1.8), Inches(3.6), Inches(2.2), "ALL CLEAN", "verified teardown", "0 residual resources")

    add_terminal(s36, Inches(0.9), Inches(4.3), Inches(11.5), Inches(2.1), "terraform destroy & verify-teardown.sh", [
        "$ terraform destroy -auto-approve",
        "module.eks.aws_eks_cluster.this[0]: Destroying...",
        "module.vpc.aws_vpc.this[0]: Destroying...",
        "Destroy complete! Resources: 56 destroyed.",
        "",
        "$ ./scripts/verify-teardown.sh",
        "[SUCCESS] 0 VPCs, 0 EKS clusters, 0 Volumes remaining in ap-southeast-2."
    ])

    # =========================================================================
    # SLIDE 37: Five Problems That Taught Me the Most
    # =========================================================================
    s37 = make_content_slide("Five problems that taught me the most", "Real production debugging lessons across CI/CD, containers, and infrastructure", 37)
    probs = [
        ("Trivy GitHub Action Tag Failure", "Action runner failed on deprecated runner environment -> Upgraded to aquasecurity/trivy-action@0.36.0"),
        ("Container Base Image CVEs", "Starlette & Alpine CVEs flagged in scan -> Patched FastAPI and pinned base images"),
        ("Non-Root NGINX Port Binding", "Default NGINX tries port 80 requiring root -> Switched to nginx-unprivileged on port 8080"),
        ("GitHub Actions Secret Conditions", "Conditional syntax failed -> Replaced with safe bash shell check in workflow script"),
        ("CI Test Database Flakiness", "File-based SQLite caused locking issues -> Implemented in-memory SQLite StaticPool fixture")
    ]
    for i, (title, fix) in enumerate(probs):
        box = s37.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.7 + i * 0.95), Inches(11.5), Inches(0.8))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        tf = box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{i+1}. {title}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = fix
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 38: Beyond Baseline Table
    # =========================================================================
    s38 = make_content_slide("Where FlowBoard goes beyond the baseline", "Engineering choices that elevate FlowBoard above introductory coursework", 38)
    headers38 = ["Standard Course Baseline", "FlowBoard Advanced Implementation"]
    rows38 = [
        ["Mutable :latest container tags", "Immutable 40-character Git commit SHA tags"],
        ["Containers run as default root (UID 0)", "Dedicated non-root users (appuser UID 10001, NGINX UID 101)"],
        ["Hardcoded plain text Kubernetes YAML", "Configurable, modular Helm chart with values.yaml"],
        ["Static pod replica counts", "Horizontal Pod Autoscaler (HPA) scaling dynamically under CPU load"],
        ["Containers pushed without CVE checks", "Automated Aqua Trivy DevSecOps gating failing on HIGH/CRITICAL"],
        ["Monolithic Docker builds", "Multi-stage Docker builds separating compiler from lean runtime"]
    ]
    add_table_slide(s38, Inches(0.9), Inches(1.8), Inches(11.5), Inches(4.5), headers38, rows38, [Inches(5.0), Inches(6.5)])

    # =========================================================================
    # SLIDE 39: Grading Module Evidence Table
    # =========================================================================
    s39 = make_content_slide("Every grading module has verified evidence", "Verified artifacts satisfying 100% of the capstone evaluation criteria", 39)
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
    add_table_slide(s39, Inches(0.9), Inches(1.65), Inches(11.5), Inches(4.8), headers39, rows39, [Inches(1.2), Inches(2.5), Inches(7.8)])

    # =========================================================================
    # SLIDE 40: Thank You & Roadmap
    # =========================================================================
    s40 = prs.slides.add_slide(blank_layout)
    bg40 = s40.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg40.fill.solid()
    bg40.fill.fore_color.rgb = BG_DARK
    bg40.line.fill.background()

    tb40 = s40.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(1.5))
    tf40 = tb40.text_frame
    p1 = tf40.paragraphs[0]
    p1.text = "THANK YOU"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(4)

    p2 = tf40.add_paragraph()
    p2.text = "What I would build next in production"
    p2.font.size = Pt(16)
    p2.font.color.rgb = ACCENT_MINT

    # 4 Roadmap cards
    r_items = [
        ("Automated HTTPS", "Domain routing with AWS Route 53 and automated ACM SSL certificates.", Inches(1.2), Inches(2.7)),
        ("Managed Cloud Database", "Migration to AWS RDS PostgreSQL Multi-AZ with automated snapshots.", Inches(6.8), Inches(2.7)),
        ("GitHub Actions OIDC", "Replace static IAM credentials with GitHub Actions OIDC role federation.", Inches(1.2), Inches(4.2)),
        ("Alertmanager Rules", "Automated Slack and PagerDuty alerting on 5xx error rate spikes.", Inches(6.8), Inches(4.2))
    ]
    for title, desc, lx, ty in r_items:
        bx = s40.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, lx, ty, Inches(5.3), Inches(1.2))
        bx.fill.solid()
        bx.fill.fore_color.rgb = RGBColor(16, 56, 54)
        bx.line.color.rgb = ACCENT_MINT
        bx.line.width = Pt(1)
        tf = bx.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_LIGHT_MINT

    tb_auth = s40.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(10.9), Inches(0.8))
    tf_a = tb_auth.text_frame
    p = tf_a.paragraphs[0]
    p.text = "github.com/PranavNayal/devopsProject"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT
    p.space_after = Pt(2)
    p2 = tf_a.add_paragraph()
    p2.text = "Pranav Nayal · DevOps Final Capstone · Session 21 · Instructor: Nensi Ravaliya"
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_LIGHT_MINT

    add_footer(s40, 40, is_dark=True)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "presentation", "FlowBoard_DevOps_Capstone_Presentation.pptx")
    create_deck(out)
