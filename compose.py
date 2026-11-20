#!/usr/bin/env python3
"""Compose the 20 November 2026 front page into assets/entry.png.

Design tool only: uses Pillow and the system DejaVu fonts to draw a
1024x1024 newspaper front page. The competition entrypoint (main.py)
is standard-library only and copies the finished PNG byte for byte,
so the graded output is deterministic.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "entry.png"

W = H = 1024
MARGIN = 34
RIGHT = W - MARGIN

PAPER = (247, 242, 230)
INK = (24, 24, 24)
ACCENT = (158, 27, 32)
SOFT = (110, 100, 84)
RULE = (178, 165, 132)
BLOCK_BG = (255, 252, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, w, kicker, headline, summary,
               head_size=23, sum_size=17, head_lines_max=3):
    """Draw one story block; returns the y just below it."""
    kf = font(SANS_B, 15)
    draw.text((x, y), kicker.upper(), font=kf, fill=ACCENT)
    y += 21
    hf = font(SANS_B, head_size)
    for line in wrap(draw, headline, hf, w)[:head_lines_max]:
        draw.text((x, y), line, font=hf, fill=INK)
        y += int(head_size * 1.2)
    y += 2
    sf = font(SANS, sum_size)
    for line in wrap(draw, summary, sf, w):
        draw.text((x, y), line, font=sf, fill=(52, 50, 46))
        y += int(sum_size * 1.28)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    d.line([(MARGIN, 24), (RIGHT, 24)], fill=INK, width=5)
    d.line([(MARGIN, 33), (RIGHT, 33)], fill=INK, width=2)
    title_f = font(SERIF_B, 54)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 42), title, font=title_f, fill=INK)

    # Date band: the day, named loud and clear.
    band_y = 116
    d.rectangle([MARGIN, band_y, RIGHT, band_y + 48], fill=INK)
    date_f = font(SANS_B, 30)
    date_txt = "FRIDAY \u00b7 NOVEMBER 20 \u00b7 2026"
    dw = d.textlength(date_txt, font=date_f)
    d.text(((W - dw) / 2, band_y + 9), date_txt, font=date_f, fill=PAPER)
    sub_f = font(SERIF, 18)
    sub = "The world's news of Friday, 20 November 2026 \u2014 in one picture"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, band_y + 56), sub, font=sub_f, fill=SOFT)

    # ---- Lead story -----------------------------------------------------
    y = band_y + 88
    lead_h = 194
    d.rectangle([MARGIN, y, RIGHT, y + lead_h], fill=BLOCK_BG)
    d.rectangle([MARGIN, y, MARGIN + 8, y + lead_h], fill=ACCENT)
    draw_block(
        d, MARGIN + 28, y + 15, RIGHT - MARGIN - 56,
        "The Hague \u00b7 World Court \u2014 Lead Story",
        "World Court Rules Myanmar Committed Genocide Against the Rohingya",
        "The International Court of Justice voted 9\u20136 that Myanmar "
        "committed genocide against the Rohingya in northern Rakhine \u2014 "
        "its first-ever finding of genocide by a state, in The Gambia's "
        "case.",
        head_size=32, sum_size=20,
    )
    y += lead_h + 16
    d.line([(MARGIN, y - 8), (RIGHT, y - 8)], fill=RULE, width=2)

    # ---- Six-story grid, two columns ------------------------------------
    col_w = (RIGHT - MARGIN - 30) // 2
    col_x = [MARGIN, MARGIN + col_w + 30]
    stories = [
        ("Shenzhen \u00b7 Summit",
         "Trump, Xi and Putin Sign Four-Point Peace Declaration",
         "Their first three-way summit, in Shenzhen, produced a joint "
         "peace declaration \u2014 but no breakthrough on Ukraine."),
        ("Markets \u00b7 Artificial Intelligence",
         "Anthropic Soars on Nasdaq Debut, Yet Stocks Fall",
         "Anthropic (ANT) closed near $97, up 17% on its $83 IPO price \u2014 "
         "but the S&P 500 fell 2% and Japan's Nikkei dropped 4.8%."),
        ("Riyadh \u00b7 Middle East",
         "Houthi Missiles Damage Riyadh Finance Tower",
         "Missiles damaged the Public Investment Fund tower in the "
         "financial district; on Friday Saudi Arabia intercepted another "
         "missile and five drones."),
        ("Ukraine \u00b7 War",
         "Ukraine Strikes Kerch Bridge a Third Time in Four Days",
         "The strike halted rail traffic and Putin vowed a response. "
         "Allies met in Berlin; the UK pledged 1,000+ drones in a "
         "\u00a3260 million package."),
        ("Kenya \u00b7 Health",
         "Kenya Discharges Last Ebola Patient \u2014 Outbreak Over",
         "Kenya sent home its last Ebola patient, ending the outbreak "
         "37 days after the first case was confirmed."),
        ("World Economy \u00b7 IMF",
         "IMF Warns Public Debt Nears 100% of World GDP",
         "The IMF warned that global public debt is approaching the "
         "size of the entire world economy."),
    ]
    row_y = y + 2
    for row in range(3):
        ends = []
        for col in range(2):
            kicker, head, summ = stories[row * 2 + col]
            ends.append(draw_block(d, col_x[col], row_y, col_w,
                                   kicker, head, summ))
        row_y = max(ends) + 11
        if row < 2:
            d.line([(MARGIN, row_y - 7), (RIGHT, row_y - 7)],
                   fill=RULE, width=1)

    # ---- Bottom strip ----------------------------------------------------
    d.line([(MARGIN, row_y - 2), (RIGHT, row_y - 2)], fill=INK, width=3)
    strip_end = draw_block(
        d, MARGIN, row_y + 10, RIGHT - MARGIN,
        "United States \u00b7 Travel",
        "FAA Ground Stop Strands About 1.5 Million Travelers",
        "A nationwide FAA ground stop left roughly 1.5 million air "
        "travelers stranded across the United States on Friday.",
        head_size=24, sum_size=18,
    )
    assert strip_end < H - 52, f"layout overflow: strip ends at {strip_end}"

    # ---- Footer -----------------------------------------------------------
    foot_f = font(SERIF, 17)
    foot = "All stories as reported on Friday, 20 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.line([(MARGIN, H - 44), (RIGHT, H - 44)], fill=INK, width=2)
    d.text(((W - fw) / 2, H - 36), foot, font=foot_f, fill=SOFT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, OUT.stat().st_size, "bytes; strip_end =", strip_end)


if __name__ == "__main__":
    main()
