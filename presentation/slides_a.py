"""Slides 1-9: framing, approach, data and the SisFall model."""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from deck_lib import *


# ------------------------------------------------------------------ 1 title
def slide_title(prs):
    s = new_slide(prs, bg=INK)
    # geometric motif
    for x, y, d in [(9.10, -0.55, 5.6), (10.55, 2.35, 3.9), (11.85, 4.55, 1.45)]:
        rect(s, x, y, d, d, fill=None, line=RGBColor(0x23, 0x51, 0x69),
             lw=1.2, shape=MSO_SHAPE.OVAL)
    rect(s, 11.93, 5.18, 0.55, 0.55, fill=ORANGE, shape=MSO_SHAPE.OVAL)
    rect(s, 10.55, 2.35, 3.9, 0.012, fill=RGBColor(0x2E, 0x63, 0x7C),
         shape=MSO_SHAPE.RECTANGLE)

    text(s, 0.95, 0.80, 8.0, 0.28, "4TH YEAR   \u00b7   FINAL MAJOR PROJECT   \u00b7   PRESENTATION 2",
         size=10.5, bold=True, color=ORANGE, spc=1.6)
    text(s, 0.90, 1.22, 7.5, 1.10, "SevaLink", size=64, bold=True, color=WHITE,
         font=FONT_LIGHT)
    text(s, 0.95, 2.40, 7.6, 1.10,
         "A smartphone-based fall detection and emergency alert system for senior citizens",
         size=21, color=RGBColor(0xCF, 0xDE, 0xE7), font=FONT_LIGHT, line_spacing=1.12)

    rect(s, 0.97, 3.72, 1.55, 0.045, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.97, 3.98, 7.8, 0.34,
         "On-device deep learning   \u00b7   10-second user verification   \u00b7   offline SMS escalation",
         size=12, color=RGBColor(0x9F, 0xB6, 0xC4))

    # meta
    text(s, 0.97, 5.16, 3.4, 0.24, "PROJECT MENTOR", size=9, bold=True,
         color=RGBColor(0x7F, 0x9B, 0xAC), spc=1.4)
    text(s, 0.97, 5.40, 4.4, 0.28, "Dr. Mukesh Kumar Tripathi", size=13.5,
         bold=True, color=WHITE)

    text(s, 5.60, 5.16, 6.9, 0.24, "TEAM", size=9, bold=True,
         color=RGBColor(0x7F, 0x9B, 0xAC), spc=1.4)
    text(s, 5.60, 5.40, 6.9, 0.26, "Bhumika Rajoria  (2300291530054)", size=13.5,
         bold=True, color=WHITE)
    text(s, 5.60, 5.68, 6.9, 0.26, "Anshita Singh  (2300291530033)", size=13.5,
         bold=True, color=WHITE)

    rect(s, 0.97, 6.28, 11.65, 0.012, fill=RGBColor(0x28, 0x57, 0x6E),
         shape=MSO_SHAPE.RECTANGLE)
    text(s, 0.97, 6.42, 8.2, 0.28, "Department of CSE (AI & ML)  \u00b7  KIET Deemed to be University",
         size=10.5, color=RGBColor(0xA9, 0xBE, 0xCB))
    text(s, 9.20, 6.42, 3.4, 0.28, "31 October 2026", size=10.5, bold=True,
         color=RGBColor(0xD5, 0xE2, 0xEA), align=PP_ALIGN.RIGHT)

    s.notes_slide.notes_text_frame.text = (
        "Good morning. We are Bhumika and Anshita, presenting SevaLink - a fall detection "
        "and emergency alert system that runs entirely on an ordinary Android smartphone. "
        "This second review covers the finalised technical approach, the working implementation, "
        "results from two subject-independent models, and the validation and project-management "
        "work behind them. The deck is organised around the nine evaluation criteria.")


# ------------------------------------------------------------------ 2 agenda
def slide_agenda(prs):
    s = new_slide(prs)
    header(s, 2, "Agenda", "Structured to the review rubric",
           "Each evaluation criterion is addressed explicitly, with evidence from the build.")

    items = [
        ("01", "Technical approach, finalised",
         "Frozen sensor contract, windowing, two-model pipeline."),
        ("02", "Implementation (\u2265 70%)",
         "Android modules, model export, verified build status."),
        ("03", "Results and validation",
         "Window- and event-level metrics on unseen participants."),
        ("04", "Presentation",
         "This 25-slide walkthrough plus backup material."),
        ("05", "Team work and contribution",
         "Split of work, evidence per member."),
        ("06", "Management, cost, scalability",
         "Timeline, risks, unit economics, scale-up path."),
        ("07", "Ethics, safety, sustainability",
         "Privacy, DPDP Act 2023, environmental impact."),
        ("08", "Research paper and plagiarism",
         "Manuscript structure, venue, similarity plan."),
        ("09", "Paper / patent readiness",
         "Novelty, prior art, submission status."),
    ]
    for i, (num, title, detail) in enumerate(items):
        col, row = divmod(i, 5)
        x = ML + col * 6.13
        y = 1.66 + row * 1.03
        text(s, x, y, 0.55, 0.32, num, size=17, bold=True, color=ORANGE,
             font=FONT_LIGHT)
        text(s, x + 0.62, y - 0.02, 5.0, 0.30, title, size=13.5, bold=True, color=INK)
        text(s, x + 0.62, y + 0.30, 5.1, 0.34, detail, size=10.5, color=GREY,
             line_spacing=1.05)
        rect(s, x, y + 0.82, 5.65, 0.008, fill=LINE, shape=MSO_SHAPE.RECTANGLE)

    footer(s, 2)
    s.notes_slide.notes_text_frame.text = (
        "The deck follows the evaluation sheet in order, so every criterion is easy to locate. "
        "Slides 9 to 16 are the technical core; 17 to 22 cover management, ethics and the paper. "
        "Backup slides carry full metric tables and references and can be used during questions.")


# ------------------------------------------------------------------ 3 problem
def slide_problem(prs):
    s = new_slide(prs)
    header(s, 3, "Context", "Falls are sudden. Help usually is not.",
           "The problem is not detecting an impact \u2014 it is getting the right help, fast, without crying wolf.")

    paragraphs(s, ML, 1.66, 7.15, 2.70, [
        P([("Falls are the second leading cause of unintentional injury deaths worldwide.", {})],
          bullet=True, size=13.5, sa=11),
        P([("28\u201335% of people aged 65+ fall at least once a year; the danger is often the ", {}),
           ("\u201clong lie\u201d", {"b": True}),
           (" \u2014 time spent on the floor before help arrives.", {})],
          bullet=True, size=13.5, sa=11),
        P([("Dedicated fall alarms cost ", {}), ("\u20b94,000\u201325,000", {"b": True}),
           (" and add another device to wear, charge and forget.", {})],
          bullet=True, size=13.5, sa=11),
        P([("Impact-only phone apps fire when the phone is dropped, so users switch them off.", {})],
          bullet=True, size=13.5, sa=11),
    ])

    card(s, ML, 4.62, 7.15, 1.55, fill=ORANGE_SOFT, line=None, accent=ORANGE)
    text(s, ML + 0.26, 4.80, 6.65, 0.26, "THE GAP WE ADDRESS", size=9.5, bold=True,
         color=ORANGE, spc=1.2)
    text(s, ML + 0.26, 5.08, 6.60, 0.95,
         "An affordable, phone-only system that verifies with the user before escalating, "
         "keeps the model on the device, and can still raise an alarm when there is no internet.",
         size=12.5, color=INK, line_spacing=1.12)

    text(s, ML, 6.46, 7.3, 0.28, "Sources: WHO Falls fact sheet; SisFall and UniMiB SHAR dataset documentation.",
         size=8.5, color=MUTED)

    kpi(s, 8.35, 1.66, 4.25, 1.50, "28\u201335%", "of adults aged 65+ fall each year",
        sub="World Health Organization", color=TEAL, fill=MIST, value_size=30)
    kpi(s, 8.35, 3.32, 4.25, 1.50, "\u20b90", "extra hardware required",
        sub="Uses the smartphone the user already owns", color=ORANGE,
        fill=ORANGE_SOFT, value_size=30)
    kpi(s, 8.35, 4.98, 4.25, 1.50, "68 KB", "on-device model, no cloud",
        sub="Works offline; no subscription, no server", color=GREEN,
        fill=GREEN_SOFT, value_size=30)

    footer(s, 3)
    s.notes_slide.notes_text_frame.text = (
        "The clinical problem is the long lie, not the fall itself. Commercial pendants work but "
        "cost money and need charging; phone apps that alert on impact alone are turned off because "
        "of false alarms. SevaLink's thesis is that verification before escalation is what makes a "
        "phone-only system usable.")


# ------------------------------------------------------------------ 4 objectives
def slide_targets(prs):
    s = new_slide(prs)
    header(s, 4, "Objectives", "Targets frozen at Presentation 1 \u2014 and measured against here",
           "No moving goalposts: the same six targets are reported with their current status.")

    rows = [
        ["Objective", "Target set at Presentation 1", "Status today"],
        ["On-device inference", "\u2264 250 KB model; \u2264 1 s model-side delay",
         "DONE \u2014 68 KB; 0.32 s"],
        ["Fall recall", "\u2265 95% on participants never seen in training",
         "PARTIAL \u2014 98.4% UniMiB; 90.7% SisFall"],
        ["False alarms", "\u2264 1 non-fall alarm per hour",
         "PARTIAL \u2014 2.77 / h on SisFall"],
        ["User verification", "10 s cancellable countdown, lock-screen capable",
         "DONE \u2014 full-screen overlay"],
        ["Offline escalation", "SMS + GPS with no internet connection",
         "PENDING \u2014 integration in progress"],
        ["Reproducibility", "Fixed seeds, subject-wise splits, export parity \u2264 1e-5",
         "DONE \u2014 14 tests; 3e-9 / 8e-8"],
    ]
    colors = {(1, 2): GREEN, (2, 2): ORANGE, (3, 2): ORANGE, (4, 2): GREEN,
              (5, 2): RED, (6, 2): GREEN}
    table(s, ML, 1.66, CW, rows, [3.05, 5.10, 3.74], fs=10.5, hfs=9.5, rh=0.66,
          cell_colors=colors, bold_first=True,
          align=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])

    text(s, ML, 6.42, CW, 0.30,
         "DONE = measured and verified     PARTIAL = target not yet met on every dataset     "
         "PENDING = build incomplete", size=9.5, color=GREY)
    text(s, ML, 6.70, CW, 0.26,
         "Fall recall and false alarms are event-level measures; the dataset caveats are on slide 15.",
         size=9.5, italic=True, color=MUTED)

    footer(s, 4)
    s.notes_slide.notes_text_frame.text = (
        "These are the same targets we set in the first review. Two are fully met: model size and "
        "reproducibility. Recall is met on UniMiB but not yet on SisFall, and false alarms are still "
        "above target. Escalation - SMS and GPS - is the main unfinished build item, and we are "
        "stating that plainly rather than hiding it.")


# ------------------------------------------------------------------ 5 pipeline
def slide_pipeline(prs):
    s = new_slide(prs)
    header(s, 5, "Technical approach", "One cascade, from sensor sample to caregiver",
           "Frozen at this review: the app, the model and the alert path share one versioned contract.")

    boxes = [
        ("Sensors", "accelerometer\n+ gyro where present\n50 Hz"),
        ("Ring buffer", "100 samples\n2 s sliding window"),
        ("Stage 1 gate", "free-fall \u2192 impact\nrule-based, no model"),
        ("Stage 2 CNN", "TFLite, 68 / 104 KB\nnormalised window"),
        ("Verification", "10 s countdown\nfull-screen overlay"),
        ("Escalation", "SMS + Maps link\nauto-call, local log"),
    ]
    x = ML
    w, gap = 1.78, 0.24
    text(s, ML, 1.70, 9.6, 0.22, "ON DEVICE \u2014 SENSOR DATA NEVER LEAVES THE PHONE",
         size=8.5, bold=True, color=GREEN, spc=0.8)
    text(s, 10.82, 1.70, 1.80, 0.22, "NETWORK", size=8.5, bold=True,
         color=ORANGE, spc=0.8)
    for i, (title, detail) in enumerate(boxes):
        fill = TEAL_SOFT if i < 5 else ORANGE_SOFT
        edge = TEAL if i < 5 else ORANGE
        rect(s, x, 1.98, w, 1.18, fill=fill, line=None)
        rect(s, x, 1.98, w, 0.055, fill=edge, shape=MSO_SHAPE.RECTANGLE)
        text(s, x + 0.14, 2.12, w - 0.24, 0.28, title, size=12.5, bold=True, color=INK)
        text(s, x + 0.14, 2.44, w - 0.22, 0.64, detail, size=9, color=GREY, line_spacing=1.08)
        if i < 5:
            arrow(s, x + w + 0.02, 2.48, 0.20, 0.18)
        x += w + gap

    cards = [
        ("Battery", "The CNN runs only on impact candidates, not on every window. "
                    "Stage 1 is arithmetic on one sample."),
        ("Precision", "Slow sit-downs and pocket jostle fail the free-fall gate before the model "
                      "is ever asked."),
        ("Latency", "Impact to decision is one 2 s window. Mean model-side detection delay "
                    "measured at 0.32 s."),
    ]
    for i, (title, body) in enumerate(cards):
        cx = ML + i * 4.04
        card(s, cx, 3.52, 3.80, 1.30, fill=WHITE, line=LINE, accent=TEAL)
        text(s, cx + 0.22, 3.66, 3.4, 0.24, title, size=11.5, bold=True, color=TEAL)
        text(s, cx + 0.22, 3.94, 3.42, 0.80, body, size=9.8, color=GREY, line_spacing=1.10)

    text(s, ML, 5.14, 4.0, 0.24, "FROZEN CONTRACT", size=9, bold=True, color=MUTED, spc=1.2)
    chips = ["50 Hz sampling", "2 s / 3 s windows", "10 s verification", "Offline SMS"]
    for i, label in enumerate(chips):
        chip(s, ML + i * 3.00, 5.42, 2.85, 0.46, label, fill=MIST, color=INK, size=10.5)
    text(s, ML, 6.10, CW, 0.60,
         "Every stage is versioned in the repository: sensor units, filter coefficients, "
         "normalisation statistics, decision threshold and alarm policy travel with the model file.",
         size=10.5, color=GREY, line_spacing=1.12)

    footer(s, 5)
    s.notes_slide.notes_text_frame.text = (
        "This is the whole system on one line. Sensors feed a two-second ring buffer. A rule gate "
        "looks for free-fall followed by impact, and only then does the CNN see a window. If the "
        "model says fall, the phone takes over the screen for ten seconds and escalates if the user "
        "does not cancel. The contract between stages is frozen and versioned with the model.")


# ------------------------------------------------------------------ 6 two models
def slide_two_models(prs):
    s = new_slide(prs)
    header(s, 6, "Technical approach", "Two datasets, two models \u2014 and one deliberate change",
           "The deployment model no longer uses the gyroscope. Here is why, and what the second model is for.")

    specs_a = [("Input", "1 \u00d7 100 \u00d7 4   (2 s @ 50 Hz)"),
               ("Channels", "ax, ay, az, |a|"),
               ("Corpus", "30 subjects \u00b7 11,771 windows"),
               ("Footprint", "12,432 parameters \u00b7 68 KB"),
               ("Held-out recall", "98.42% (window-level)")]
    specs_b = [("Input", "1 \u00d7 150 \u00d7 6   (3 s @ 50 Hz)"),
               ("Channels", "ax, ay, az, gx, gy, gz"),
               ("Corpus", "38 subjects \u00b7 4,500 recordings"),
               ("Footprint", "25,761 parameters \u00b7 104 KB"),
               ("Held-out recall", "90.65% (window-level)")]

    for i, (tag, tagcol, tagfill, title, spec, accent) in enumerate([
        ("PRIMARY \u00b7 DEPLOYMENT", GREEN, GREEN_SOFT,
         "UniMiB SHAR \u2014 accelerometer only", specs_a, GREEN),
        ("REFERENCE \u00b7 6-AXIS", TEAL, TEAL_SOFT,
         "SisFall Original \u2014 acc + gyro", specs_b, TEAL),
    ]):
        x = ML + i * 6.10
        card(s, x, 1.62, 5.85, 3.85, fill=WHITE, line=LINE)
        chip(s, x + 0.24, 1.80, 1.95, 0.30, tag, fill=tagfill, color=tagcol, size=8.5)
        text(s, x + 0.24, 2.20, 5.35, 0.34,
             title, size=15.5, bold=True, color=INK, font=FONT_LIGHT)
        for j, (k, v) in enumerate(spec):
            yy = 2.68 + j * 0.50
            text(s, x + 0.24, yy, 1.35, 0.24, k.upper(), size=8.2, bold=True,
                 color=MUTED, spc=0.9)
            text(s, x + 1.62, yy - 0.02, 4.0, 0.26, v, size=10.5, color=INK)
            rect(s, x + 0.24, yy + 0.34, 5.35, 0.007, fill=LINE, shape=MSO_SHAPE.RECTANGLE)

    # decision band
    rect(s, ML, 5.62, CW, 1.10, fill=INK, line=None, radius=0.10)
    text(s, ML + 0.28, 5.76, 4.9, 0.24, "WHY THE DEPLOYMENT MODEL DROPS THE GYROSCOPE",
         size=8.8, bold=True, color=ORANGE, spc=1.0)
    reasons = [
        "Pocket-phone protocol matches the real deployment condition.",
        "Many low-cost Android phones have no gyroscope at all.",
        "One sensor stream, 43% smaller model, lower power draw.",
    ]
    for i, r in enumerate(reasons):
        rx = ML + 0.28 + i * 3.85
        text(s, rx, 6.06, 3.55, 0.55, r, size=9.8,
             color=RGBColor(0xD5, 0xE2, 0xEA), line_spacing=1.08)
    text(s, ML, 6.80, CW, 0.22,
         "SisFall's 6-axis model is retained to test whether gyroscope data materially improves recall; "
         "it is not the model we ship.", size=9, italic=True, color=MUTED)

    footer(s, 6)
    s.notes_slide.notes_text_frame.text = (
        "This is the main technical change since the first review. The model we deploy is trained on "
        "UniMiB SHAR using accelerometer magnitude and three axes - no gyroscope. UniMiB was recorded "
        "with the phone in a trouser pocket, which is our real condition; cheap phones often lack a "
        "gyroscope; and the model is 68 KB instead of 104 KB. The SisFall six-axis model stays as a "
        "reference to check that gyroscope data is not buying us anything.")


# ------------------------------------------------------------------ 7 datasets
def slide_data(prs):
    s = new_slide(prs)
    header(s, 7, "Data", "Two public corpora, validated before a single epoch",
           "Integrity checks run before preprocessing; anything that failed inspection was quarantined, not silently dropped.")

    rows = [
        ["Dataset", "Participants", "Data used", "Sensor / placement", "Split (train / val / test)"],
        ["SisFall Original", "38  (23 young, 15 elderly)", "4,500 recordings \u00b7 1,798 falls",
         "Waist-mounted \u00b7 6-axis", "24 / 7 / 7 participants"],
        ["UniMiB SHAR", "30", "11,771 windows \u00b7 4,192 falls",
         "Trouser pocket \u00b7 accelerometer", "21 / 4 / 5 participants"],
    ]
    table(s, ML, 1.62, CW, rows, [2.45, 2.25, 2.70, 2.65, 1.84], fs=10.5, hfs=9.3,
          rh=0.68, bold_first=True)

    text(s, ML, 3.86, 7.0, 0.26, "INTEGRITY CHECKS THAT RAN BEFORE TRAINING",
         size=9.2, bold=True, color=ORANGE, spc=1.2)
    left = [
        "SHA-256-pinned archive; 4,505 raw files inspected and 5 folder/filename identity conflicts (SA15) quarantined \u2014 4,500 eligible, none dropped silently.",
        "Numeric range and bit-width validation, duplicate-file scan, and the SisFall README file-count discrepancy documented in the audit report.",
    ]
    right = [
        "24 participants contain both classes; 14 elderly participants are ADL-only \u2014 the stratified participant split preserves this structure.",
        "Splits assigned by participant before windowing; SE06 is forced into the test split so elderly falls remain represented.",
    ]
    paragraphs(s, ML, 4.16, 5.70, 1.55, [P(t, bullet=True, size=10.5, sa=9) for t in left])
    paragraphs(s, ML + 6.10, 4.16, 5.70, 1.55, [P(t, bullet=True, size=10.5, sa=9) for t in right])

    rect(s, ML, 5.92, CW, 0.78, fill=TEAL_SOFT, line=None, radius=0.10)
    rect(s, ML, 5.92, 0.055, 0.78, fill=TEAL, shape=MSO_SHAPE.RECTANGLE)
    text(s, ML + 0.28, 6.06, CW - 0.5, 0.50,
         "No participant appears in more than one split. Windowing happens after splitting, so "
         "overlapping windows cannot leak a test subject into training.",
         size=11.5, color=INK, line_spacing=1.10)

    footer(s, 7)
    s.notes_slide.notes_text_frame.text = (
        "Both datasets are public and well known. The audit matters more than the headline counts: "
        "five SisFall files had a folder/filename mismatch, so they were quarantined rather than "
        "quietly deleted, leaving 4,500 eligible recordings. Splits are by participant, before "
        "windowing, which is the only way to avoid subject leakage with overlapping windows.")


# ------------------------------------------------------------------ 8 preprocessing
def slide_preprocess(prs):
    s = new_slide(prs)
    header(s, 8, "Data", "Preprocessing is causal, documented and identical in training and app",
           "The same contract is exported with the model, so the phone cannot silently diverge from the notebook.")

    left_steps = [
        ("1", "Physical units", "Acceleration (32/8192)\u00b7g; angular rate (4000/65536)\u00b7\u03c0/180."),
        ("2", "Common time grid", "200 Hz grid on the acc/gyro overlap; gaps > 100 ms are split, never extrapolated."),
        ("3", "Causal filtering", "4th-order 10 Hz Butterworth SOS, forward-only, state reset per segment."),
        ("4", "Window", "Decimate \u00f74 to 50 Hz \u2192 150 samples (3 s), stride 25 (0.5 s)."),
    ]
    right_steps = [
        ("1", "Layout verification", "151 \u00d7 3 axis-major layout confirmed by a roughness test (1.23 vs 2.56)."),
        ("2", "Centre crop", "100 samples (2 s); the impact peak is retained in 98% of fall windows."),
        ("3", "Fourth channel", "Magnitude |a| added \u2192 orientation-invariant representation."),
        ("4", "Normalise", "Per-channel z-score using training-subject statistics only."),
    ]
    for col, (title, sub, steps) in enumerate([
        ("SisFall \u00b7 200 Hz \u2192 50 Hz \u00b7 6-axis", "continuous recordings", left_steps),
        ("UniMiB SHAR \u00b7 50 Hz \u00b7 accelerometer", "pre-segmented windows", right_steps),
    ]):
        x = ML + col * 6.10
        card(s, x, 1.62, 5.85, 4.18, fill=WHITE, line=LINE)
        text(s, x + 0.26, 1.80, 5.3, 0.26, title, size=12.5, bold=True, color=TEAL)
        text(s, x + 0.26, 2.07, 5.3, 0.22, sub, size=9, color=MUTED)
        for j, (n, head, body) in enumerate(steps):
            yy = 2.46 + j * 0.82
            text(s, x + 0.26, yy, 0.32, 0.26, n, size=13, bold=True, color=ORANGE,
                 font=FONT_LIGHT)
            text(s, x + 0.66, yy - 0.02, 4.95, 0.24, head, size=10.8, bold=True, color=INK)
            text(s, x + 0.66, yy + 0.24, 4.95, 0.46, body, size=9.4, color=GREY,
                 line_spacing=1.06)

    chips_txt = [
        "No padding, no extrapolation,\nno per-window normalisation",
        "Labels: half-open E\u22121 \u2264 impact < E;\nambiguous windows excluded",
        "Normalisation and threshold fitted on\ntraining / validation only",
    ]
    for i, label in enumerate(chips_txt):
        cx = ML + i * 4.00
        rect(s, cx, 5.98, 3.82, 0.72, fill=MIST, line=None)
        text(s, cx + 0.16, 6.06, 3.55, 0.58, label, size=9.3, color=INK, line_spacing=1.10)

    footer(s, 8)
    s.notes_slide.notes_text_frame.text = (
        "Preprocessing is where most fall-detection results quietly break. We resample to a common "
        "200 Hz grid, split on gaps, filter causally so the phone can reproduce it sample by sample, "
        "then decimate to 50 Hz. SisFall gives three-second six-channel windows; UniMiB gives "
        "two-second four-channel windows with magnitude. Both use training-only statistics.")


# ------------------------------------------------------------------ 9 SisFall model
def slide_model_sisfall(prs):
    s = new_slide(prs)
    header(s, 9, "Model 1", "SisFall: a compact 1-D CNN over six channels",
           "Three convolution stages, global pooling and a single sigmoid \u2014 25,761 parameters in about 100 KB.")

    blocks = [("Input", "150 \u00d7 6", ""),
              ("Conv1D 32", "kernel 5", "same \u00b7 ReLU"),
              ("MaxPool", "\u00f7 2", "75 \u00d7 32"),
              ("Conv1D 64", "kernel 5", "pool \u00f7 2"),
              ("Conv1D 64", "kernel 3", "GAP \u2192 64"),
              ("Dense 32", "ReLU", "dropout 0.3"),
              ("Sigmoid", "1 output", "fall probability")]
    x = ML
    w, gap = 1.56, 0.12
    for i, (l1, l2, l3) in enumerate(blocks):
        fill = MIST if i not in (6,) else ORANGE_SOFT
        rect(s, x, 1.62, w, 1.02, fill=fill, line=None)
        text(s, x + 0.10, 1.72, w - 0.16, 0.26, l1, size=10.5, bold=True, color=INK)
        text(s, x + 0.10, 1.99, w - 0.16, 0.22, l2, size=8.8, bold=True,
             color=TEAL if i not in (6,) else ORANGE)
        text(s, x + 0.10, 2.22, w - 0.16, 0.30, l3, size=8, color=GREY, line_spacing=1.0)
        if i < 6:
            arrow(s, x + w + 0.005, 2.04, 0.11, 0.16)
        x += w + gap

    kpis = [("25,761", "parameters"), ("100.6 KB", "float32 TFLite"),
            ("0.9966", "best val PR-AUC"), ("18", "epochs to convergence")]
    for i, (v, l) in enumerate(kpis):
        kpi(s, ML + i * 3.00, 3.00, 2.85, 1.05, v, l, color=TEAL, fill=MIST, value_size=22)

    text(s, ML, 4.34, 5.6, 0.24, "TRAINING RECIPE", size=9, bold=True, color=ORANGE, spc=1.2)
    paragraphs(s, ML, 4.62, 5.55, 1.95, [
        P("Adam 1e-3, binary cross-entropy, batch 128", bullet=True, size=10.5, sa=7),
        P("\u2264 40 epochs, early stopping patience 7", bullet=True, size=10.5, sa=7),
        P("Best validation PR-AUC checkpoint restored", bullet=True, size=10.5, sa=7),
        P("Inverse-frequency class weights (2.9 : 1)", bullet=True, size=10.5, sa=7),
        P("Threshold selected on validation only", bullet=True, size=10.5, sa=7),
    ])

    text(s, 6.78, 4.34, 5.6, 0.24, "WHY THIS ARCHITECTURE", size=9, bold=True,
         color=ORANGE, spc=1.2)
    paragraphs(s, 6.78, 4.62, 5.70, 1.95, [
        P("Global average pooling removes dependence on where the impact lands inside the window.",
          bullet=True, size=10.5, sa=7),
        P("Stacked k=5 then k=3 kernels capture the impact spike and the stillness that follows.",
          bullet=True, size=10.5, sa=7),
        P("100 KB fits any Android device and leaves headroom for future quantisation.",
          bullet=True, size=10.5, sa=7),
    ])
    text(s, 6.78, 6.34, 5.75, 0.30,
         "Same cascade also runs on the 6-axis model if a device provides a gyroscope.",
         size=9, italic=True, color=MUTED)

    footer(s, 9)
    s.notes_slide.notes_text_frame.text = (
        "This is the six-axis reference model. It is deliberately small: three convolution stages, "
        "global average pooling, a 32-unit dense layer and one sigmoid. The pooling is important "
        "because it stops the network depending on exactly where in the window the impact occurs. "
        "It reaches a best validation PR-AUC of 0.9966 in 18 epochs.")


# keep RGBColor import available through deck_lib star import
def build(prs):
    slide_title(prs)
    slide_agenda(prs)
    slide_problem(prs)
    slide_targets(prs)
    slide_pipeline(prs)
    slide_two_models(prs)
    slide_data(prs)
    slide_preprocess(prs)
    slide_model_sisfall(prs)
