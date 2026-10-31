"""Design system helpers for the SevaLink Presentation 2 deck."""

from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData

# ---------------------------------------------------------------- palette
INK = RGBColor(0x0E, 0x28, 0x41)
TEAL = RGBColor(0x15, 0x60, 0x82)
TEAL_DARK = RGBColor(0x0F, 0x44, 0x5C)
TEAL_SOFT = RGBColor(0xE7, 0xF1, 0xF5)
ORANGE = RGBColor(0xE9, 0x71, 0x32)
ORANGE_SOFT = RGBColor(0xFD, 0xEF, 0xE7)
GREEN = RGBColor(0x1E, 0x7A, 0x3C)
GREEN_SOFT = RGBColor(0xE8, 0xF3, 0xEB)
RED = RGBColor(0xB3, 0x26, 0x1E)
RED_SOFT = RGBColor(0xFB, 0xEA, 0xE8)
GREY = RGBColor(0x5B, 0x6B, 0x78)
MUTED = RGBColor(0x8A, 0x99, 0xA5)
LINE = RGBColor(0xDC, 0xE3, 0xE8)
MIST = RGBColor(0xF2, 0xF5, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Calibri"
FONT_LIGHT = "Calibri Light"

SW, SH = 13.333, 7.5
ML = 0.72                      # left margin
CW = SW - 2 * ML               # content width


# ---------------------------------------------------------------- basics
def new_slide(prs, bg=WHITE):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fill = s.background.fill
    fill.solid()
    fill.fore_color.rgb = bg
    return s


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.9,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.shadow.inherit = False
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(lw)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = radius
        except (IndexError, ValueError):
            pass
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    return sp


def text(slide, x, y, w, h, s, size=14, bold=False, color=INK, font=FONT,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.0,
         italic=False, spc=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = s
    f = r.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = font
    f.color.rgb = color
    if spc:
        f._rPr.set("spc", str(int(spc * 100)))
    return tb


def P(runs, size=13, color=INK, bold=False, bullet=False, level=0,
      sa=7, sb=0, ls=1.06, align=PP_ALIGN.LEFT):
    """Paragraph spec. `runs` is a string or list of (text, overrides)."""
    if isinstance(runs, str):
        runs = [(runs, {})]
    return dict(runs=runs, size=size, color=color, bold=bold, bullet=bullet,
                level=level, sa=sa, sb=sb, ls=ls, align=align)


def paragraphs(slide, x, y, w, h, items, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor

    for i, spec in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = spec["align"]
        p.line_spacing = spec["ls"]
        p.space_before = Pt(spec["sb"])
        p.space_after = Pt(spec["sa"])
        if spec["bullet"]:
            pPr = p._p.get_or_add_pPr()
            marL = 0.24 + 0.22 * spec["level"]
            pPr.set("marL", str(int(Inches(marL))))
            pPr.set("indent", str(int(Inches(-0.22))))
            bullet_run = p.add_run()
            bullet_run.text = ("\u2022  " if spec["level"] == 0 else "\u2013  ")
            bf = bullet_run.font
            bf.size = Pt(spec["size"])
            bf.bold = True
            bf.name = FONT
            bf.color.rgb = ORANGE if spec["level"] == 0 else MUTED
        for txt, ov in spec["runs"]:
            r = p.add_run()
            r.text = txt
            f = r.font
            f.size = Pt(ov.get("s", spec["size"]))
            f.bold = ov.get("b", spec["bold"])
            f.italic = ov.get("i", False)
            f.name = FONT
            f.color.rgb = ov.get("c", spec["color"])
    return tb


def header(slide, num, section, title, kicker=None, title_size=27):
    text(slide, ML, 0.40, 8.0, 0.26,
         f"{num:02d}  \u00b7  {section.upper()}", size=10.5, bold=True,
         color=ORANGE, spc=1.4)
    text(slide, ML, 0.66, CW, 0.62, title, size=title_size, bold=True,
         color=INK, font=FONT_LIGHT)
    if kicker:
        text(slide, ML, 1.20, CW - 0.2, 0.30, kicker, size=12, color=GREY)
    y = 1.52 if kicker else 1.32
    rect(slide, ML, y, CW, 0.014, fill=LINE, shape=MSO_SHAPE.RECTANGLE)
    rect(slide, ML, y, 1.05, 0.03, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)


def footer(slide, page=None):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(ML), Inches(7.03),
                                   Inches(SW - ML), Inches(7.03))
    ln.line.color.rgb = LINE
    ln.line.width = Pt(0.75)
    text(slide, ML, 7.10, 8.5, 0.24,
         "SevaLink  \u00b7  Smartphone-based fall detection and emergency alert",
         size=8.5, color=MUTED)
    if page is not None:
        text(slide, SW - ML - 1.2, 7.10, 1.2, 0.24, f"{page:02d}", size=8.5,
             bold=True, color=MUTED, align=PP_ALIGN.RIGHT)
    else:
        text(slide, SW - ML - 4.0, 7.10, 4.0, 0.24,
             "Final Major Project  \u00b7  Presentation 2  \u00b7  31 Oct 2026",
             size=8.5, color=MUTED, align=PP_ALIGN.RIGHT)


def chip(slide, x, y, w, h, label, fill=TEAL_SOFT, color=TEAL, size=10,
         bold=True, line=None):
    sp = rect(slide, x, y, w, h, fill=fill, line=line, radius=0.35)
    tf = sp.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = FONT
    r.font.color.rgb = color
    return sp


def card(slide, x, y, w, h, fill=WHITE, line=LINE, accent=None):
    rect(slide, x, y, w, h, fill=fill, line=line)
    if accent:
        rect(slide, x, y + 0.14, 0.045, h - 0.28, fill=accent,
             shape=MSO_SHAPE.RECTANGLE)


def kpi(slide, x, y, w, h, value, label, sub=None, color=TEAL, fill=MIST,
        value_size=30):
    card(slide, x, y, w, h, fill=fill, line=None)
    text(slide, x + 0.20, y + 0.13, w - 0.35, 0.52, value, size=value_size,
         bold=True, color=color, font=FONT_LIGHT)
    text(slide, x + 0.20, y + 0.13 + value_size / 72.0 + 0.10, w - 0.35, 0.28,
         label, size=10.5, bold=True, color=INK)
    if sub:
        text(slide, x + 0.20, y + h - 0.34, w - 0.35, 0.26, sub, size=8.8,
             color=GREY)


def table(slide, x, y, w, rows, col_widths, fs=11, hfs=10, rh=0.34,
          align=None, header=True, header_fill=TEAL, header_color=WHITE,
          zebra=True, bold_first=False, cell_colors=None, first_col_w=None):
    nrows, ncols = len(rows), len(rows[0])
    gf = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y),
                                Inches(w), Inches(rh * nrows))
    tbl = gf.table
    tbl.first_row = header
    tbl.horz_banding = False
    tbl.vert_banding = False
    for i, cw in enumerate(col_widths):
        tbl.columns[i].width = Inches(cw)
    for r in range(nrows):
        tbl.rows[r].height = Inches(rh)
        for c in range(ncols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.10)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            is_head = header and r == 0
            fill = header_fill if is_head else (MIST if (zebra and r % 2 == 0) else WHITE)
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (align[c] if align else PP_ALIGN.LEFT)
            run = p.add_run()
            run.text = str(rows[r][c])
            f = run.font
            f.size = Pt(hfs if is_head else fs)
            f.bold = is_head or (bold_first and c == 0)
            f.name = FONT
            f.color.rgb = header_color if is_head else INK
            if cell_colors and (r, c) in cell_colors:
                f.color.rgb = cell_colors[(r, c)]
    return tbl


def arrow(slide, x, y, w=0.26, h=0.20, color=MUTED):
    sp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y),
                                Inches(w), Inches(h))
    sp.shadow.inherit = False
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    sp.line.fill.background()
    return sp


def progress(slide, x, y, w, pct, h=0.10, color=TEAL, track=None):
    track = track or RGBColor(0xE3, 0xEA, 0xEE)
    rect(slide, x, y, w, h, fill=track, radius=0.5)
    if pct > 0:
        rect(slide, x, y, max(w * pct / 100.0, 0.06), h, fill=color, radius=0.5)


def bar_chart(slide, x, y, w, h, cats, series, colors, vmin=0, vmax=100,
              numfmt="0.0"):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y),
                                Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.font.name = FONT
    ch.font.size = Pt(10)
    ch.font.color.rgb = GREY
    ch.has_title = False
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(10)
    ch.legend.font.name = FONT
    ch.legend.font.color.rgb = INK
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.overlap = -6
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.font.size = Pt(9)
    dl.font.bold = True
    dl.font.name = FONT
    dl.font.color.rgb = INK
    dl.number_format = numfmt
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    va = ch.value_axis
    va.minimum_scale = vmin
    va.maximum_scale = vmax
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xE8, 0xED, 0xF1)
    va.major_gridlines.format.line.width = Pt(0.5)
    va.tick_labels.font.size = Pt(9)
    va.format.line.fill.background()
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(10)
    ca.tick_labels.font.color.rgb = INK
    ca.format.line.color.rgb = LINE
    for s, col in zip(ch.series, colors):
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = col
    return ch
