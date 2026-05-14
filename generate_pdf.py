#!/usr/bin/env python3
"""Generate Chelsea Wade UGC Portfolio PDF using reportlab."""

import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ── CONFIG ──
OUTPUT = "/Users/chelseaknox/Desktop/UGC Portfolio/Chelsea Wade - UGC Portfolio.pdf"
THUMB_DIR = "/Users/chelseaknox/Desktop/UGC Portfolio/thumbnails/"
W, H = letter  # 612 x 792

# Colors
CORAL = HexColor("#E8735A")
CORAL_LIGHT = HexColor("#FCEEE9")
PEACH = HexColor("#F4A98A")
SAGE = HexColor("#7BAE7F")
SAGE_LIGHT = HexColor("#EAF4EB")
LAVENDER = HexColor("#C4A8D4")
LAVENDER_LIGHT = HexColor("#F3EDF7")
GOLD = HexColor("#D4A843")
GOLD_LIGHT = HexColor("#FFF3E0")
WARM_CREAM = HexColor("#FFF8F3")
TEXT_DARK = HexColor("#2D2A26")
TEXT_MID = HexColor("#5C574F")
TEXT_LIGHT = HexColor("#8A8480")
WHITE = white


def draw_rounded_rect(c, x, y, w, h, r, fill_color=None, stroke=False, stroke_color=None):
    """Draw a rounded rectangle."""
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    if fill_color:
        c.setFillColor(fill_color)
    if stroke and stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(1)
    if fill_color and stroke:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    elif stroke:
        c.drawPath(p, fill=0, stroke=1)


def draw_gradient_rect(c, x, y, w, h, color1, color2, steps=50):
    """Simulate a horizontal gradient with thin vertical strips."""
    strip_w = w / steps
    r1, g1, b1 = color1.red, color1.green, color1.blue
    r2, g2, b2 = color2.red, color2.green, color2.blue
    for i in range(steps):
        t = i / (steps - 1)
        r = r1 + (r2 - r1) * t
        g = g1 + (g2 - g1) * t
        b = b1 + (b2 - b1) * t
        c.setFillColor(Color(r, g, b))
        c.rect(x + i * strip_w, y, strip_w + 0.5, h, fill=1, stroke=0)


def draw_pill(c, x, y, w, h, fill_color, text, text_color, font_size=9):
    """Draw a pill/tag shape with centered text."""
    draw_rounded_rect(c, x, y, w, h, h / 2, fill_color=fill_color)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", font_size)
    c.drawCentredString(x + w / 2, y + h / 2 - font_size / 3, text)


def draw_credential_card(c, x, y, w, h, number, label):
    """Draw a credential card."""
    draw_rounded_rect(c, x, y, w, h, 10, fill_color=WHITE)
    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(x + w / 2, y + h - 30, number)
    c.setFillColor(TEXT_LIGHT)
    c.setFont("Helvetica", 7.5)
    # Word wrap label
    words = label.split()
    lines = []
    current = ""
    for word in words:
        test = current + " " + word if current else word
        if c.stringWidth(test, "Helvetica", 7.5) < w - 12:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    label_y = y + 12 + (len(lines) - 1) * 9
    for line in lines:
        c.drawCentredString(x + w / 2, label_y, line)
        label_y -= 9


def draw_stat_card(c, x, y, w, h, value, label):
    """Draw an audience stat card."""
    draw_rounded_rect(c, x, y, w, h, 10, fill_color=WHITE)
    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(x + w / 2, y + h - 30, value)
    c.setFillColor(TEXT_LIGHT)
    c.setFont("Helvetica", 8)
    c.drawCentredString(x + w / 2, y + 10, label)


def build_pdf():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("Chelsea Wade - UGC Portfolio")
    c.setAuthor("Chelsea Wade")

    margin = 48
    content_w = W - 2 * margin

    # ════════════════════════════════════════
    # PAGE 1
    # ════════════════════════════════════════

    # Background
    c.setFillColor(WARM_CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Hero gradient banner
    hero_h = 140
    hero_y = H - hero_h
    draw_gradient_rect(c, 0, hero_y, W, hero_h, CORAL, LAVENDER)

    # Hero text
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 36)
    c.drawString(margin, hero_y + hero_h - 50, "Chelsea Wade")

    c.setFont("Helvetica", 13)
    c.setFillColor(Color(1, 1, 1, 0.92))
    c.drawString(margin, hero_y + hero_h - 72, "UGC Creator & Content Strategist  |  Homeschool Mom  |  AI Educator")

    c.setFont("Helvetica", 9)
    c.setFillColor(Color(1, 1, 1, 0.8))
    c.drawString(margin, hero_y + 16, "chelseacknox@gmail.com  |  TikTok: @chelseacknox  |  Instagram: @chelseacwade")

    # ── ABOUT SECTION ──
    y = hero_y - 32

    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y, "ABOUT ME")

    y -= 24
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y, "Marketing Brain, Creator Heart")

    y -= 20
    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica", 10)

    about_lines = [
        "I'm a working mom and first-generation homeschooler creating content at the",
        "intersection of faith, motherhood, and intentional living. I bring a warm, authentic",
        "voice that resonates with moms who care deeply about their families' well-being.",
        "",
        "What sets me apart: I don't just create content — I study it. With a marketing degree",
        "(graduated cum laude) and hands-on experience analyzing 160+ social media profiles",
        "quarterly, I understand what makes content perform, not just look pretty.",
    ]
    for line in about_lines:
        c.drawString(margin, y, line)
        y -= 14

    # ── PILLARS ──
    y -= 8
    pill_data = [
        ("Homeschooling", CORAL_LIGHT, CORAL),
        ("Faith + Family", SAGE_LIGHT, SAGE),
        ("Motherhood", LAVENDER_LIGHT, LAVENDER),
        ("AI + Education", GOLD_LIGHT, GOLD),
    ]
    px = margin
    for text, bg, fg in pill_data:
        pw = c.stringWidth(text, "Helvetica-Bold", 9) + 30
        draw_pill(c, px, y, pw, 24, bg, text, fg, 9)
        px += pw + 8

    # ── CREDENTIAL CARDS ──
    y -= 40
    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y + 8, "WHAT I BRING")

    y -= 8
    card_w = (content_w - 3 * 12) / 4
    card_h = 70
    creds = [
        ("160+", "Social profiles analyzed quarterly"),
        ("2-5x", "Posts per week across platforms"),
        ("2", "Active niches"),
        ("Daily", "Trend & hook research"),
    ]
    for i, (num, lab) in enumerate(creds):
        cx = margin + i * (card_w + 12)
        draw_credential_card(c, cx, y - card_h, card_w, card_h, num, lab)

    # ── AUDIENCE SECTION ──
    y = y - card_h - 32
    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y, "AUDIENCE")

    y -= 24
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y, "Who's Watching")

    y -= 16
    stat_w = (content_w - 2 * 12) / 3
    stat_h = 60
    stats_row1 = [
        ("26K", "TikTok Followers"),
        ("93%", "Female Audience"),
        ("21K", "Monthly Views"),
    ]
    for i, (val, lab) in enumerate(stats_row1):
        sx = margin + i * (stat_w + 12)
        draw_stat_card(c, sx, y - stat_h, stat_w, stat_h, val, lab)

    y -= stat_h + 10
    stats_row2 = [
        ("52%", "Age 35-44"),
        ("24%", "Age 25-34"),
        ("SE US", "Primary Location"),
    ]
    for i, (val, lab) in enumerate(stats_row2):
        sx = margin + i * (stat_w + 12)
        draw_stat_card(c, sx, y - stat_h, stat_w, stat_h, val, lab)

    # ── BRAND EXPERIENCE ──
    y = y - stat_h - 32
    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y, "BRAND EXPERIENCE")

    y -= 20
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Brands I've Worked With")

    y -= 24
    # StarSpark tag
    tag_text = "StarSpark Math AI Tutor"
    tag_sub = " — Paid Partnership"
    tw = c.stringWidth(tag_text, "Helvetica-Bold", 10) + c.stringWidth(tag_sub, "Helvetica", 9) + 30
    draw_rounded_rect(c, margin, y, tw, 28, 14, fill_color=WHITE, stroke=True, stroke_color=HexColor("#E8E4DF"))
    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 14, y + 9, tag_text)
    c.setFillColor(TEXT_LIGHT)
    c.setFont("Helvetica", 9)
    c.drawString(margin + 14 + c.stringWidth(tag_text, "Helvetica-Bold", 10) + 2, y + 9, tag_sub)

    # ════════════════════════════════════════
    # PAGE 2 - CONTENT SAMPLES
    # ════════════════════════════════════════
    c.showPage()

    # Background
    c.setFillColor(WARM_CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # White card for content section
    card_margin = 36
    card_y = H - 36
    card_x = card_margin
    card_w_full = W - 2 * card_margin

    y = H - 50

    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, y, "CONTENT SAMPLES")

    y -= 24
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y, "My Content in Action")

    y -= 16
    c.setFillColor(TEXT_MID)
    c.setFont("Helvetica", 9.5)
    c.drawString(margin, y, "Styles include talking head, text overlay, storytelling, day-in-the-life, and series content.")

    # ── VIDEO THUMBNAILS ──
    y -= 24
    videos = [
        ("3 Reasons Why Homeschool", "Talking Head", "3 Reasons Why Homeschool"),
        ("Curriculum Overview - Day in the Life", "Day in the Life", "Curriculum Overview"),
        ("Curriculum Overview", "Series", "Day 7 — Co-Op Day"),
        ("Series - Homeschool", "Car Vlog", "Day 10 of Homeschooling"),
        ("Text layover", "Text Overlay", "Setting Up Our Space"),
        ("Text on Screen", "List Style", "3 Micro Habits"),
        ("text on screen ", "POV / Story", "POV: Life Update"),
    ]

    thumb_w = (content_w - 6 * 10) / 7
    thumb_h = thumb_w * (16 / 9)
    tx = margin

    for i, (filename, tag, title) in enumerate(videos):
        img_path = os.path.join(THUMB_DIR, filename + ".jpg")
        if os.path.exists(img_path):
            # Draw rounded clip area
            c.saveState()
            p = c.beginPath()
            p.roundRect(tx, y - thumb_h, thumb_w, thumb_h, 8)
            c.clipPath(p, stroke=0)

            # Draw image
            img = ImageReader(img_path)
            c.drawImage(img, tx, y - thumb_h, thumb_w, thumb_h, preserveAspectRatio=False)

            # Gradient overlay at bottom
            overlay_h = thumb_h * 0.4
            for s in range(20):
                t = s / 19
                alpha = t * 0.7
                c.setFillColor(Color(0, 0, 0, alpha))
                sh = overlay_h / 20
                c.rect(tx, y - thumb_h + s * sh, thumb_w, sh + 0.5, fill=1, stroke=0)

            # Tag
            c.setFillColor(Color(1, 1, 1, 0.3))
            tag_w = c.stringWidth(tag, "Helvetica-Bold", 5.5) + 8
            draw_rounded_rect(c, tx + 4, y - thumb_h + 18, tag_w, 12, 3, fill_color=Color(1, 1, 1, 0.25))
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 5.5)
            c.drawString(tx + 8, y - thumb_h + 21, tag.upper())

            # Title
            c.setFont("Helvetica", 6)
            c.drawString(tx + 4, y - thumb_h + 6, title)

            c.restoreState()

        tx += thumb_w + 10

    # ── CTA SECTION ──
    y = y - thumb_h - 40
    cta_h = 120
    cta_x = margin
    cta_w = content_w

    draw_gradient_rect(c, cta_x, y - cta_h, cta_w, cta_h, CORAL, PEACH)
    # Round corners overlay
    c.saveState()
    p = c.beginPath()
    p.roundRect(cta_x, y - cta_h, cta_w, cta_h, 16)
    c.clipPath(p, stroke=0)
    draw_gradient_rect(c, cta_x, y - cta_h, cta_w, cta_h, CORAL, PEACH)
    c.restoreState()

    # CTA text
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(W / 2, y - 36, "Let's Create Together")

    c.setFont("Helvetica", 10)
    c.setFillColor(Color(1, 1, 1, 0.9))
    c.drawCentredString(W / 2, y - 56, "I'd love to bring your brand to life with authentic, strategy-driven")
    c.drawCentredString(W / 2, y - 70, "content that connects with moms who care.")

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, y - 96, "chelseacknox@gmail.com")

    # Footer
    c.setFillColor(TEXT_LIGHT)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 24, "© 2025 Chelsea Wade. All rights reserved.")

    c.save()
    print(f"PDF saved: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
