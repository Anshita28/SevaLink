"""Slides 19-28: teamwork, management, cost, ethics, paper, roadmap and backup."""

from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from deck_lib import *


# ------------------------------------------------------------------ 19 team
def slide_team(prs):
    s = new_slide(prs)
    header(s, 19, "Team work", "Split of work and individual contribution",
           "Two members, one repository: model and data ownership on one side, app and integration on the other.")

    people = [
        ("Bhumika Rajoria", "2300291530054", "DATA & MODELS", TEAL, TEAL_SOFT, [
            "Dataset audit, integrity checks and preprocessing contract for both corpora.",
            "CNN architecture design and training for SisFall and UniMiB.",
            "Threshold policy, Keras/TFLite export and parity verification.",
            "Results analysis, error breakdown and the metric tables in this deck.",
            "Reproducibility package: environment manifest, fixtures and audit reports.",
        ]),
        ("Anshita Singh", "2300291530033", "APP & INTEGRATION", GREEN, GREEN_SOFT, [
            "Android architecture: Compose UI, Hilt, Room and DataStore layers.",
            "Foreground sensor service, wake lock and the stage-1 detection gate.",
            "Full-screen verification overlay with lock-screen behaviour.",
            "Permission onboarding, accessibility and device compatibility (minSdk 26).",
            "Build verification, demo recording and the UI sections of this deck.",
        ]),
    ]
    for i, (name, roll, tag, color, fill, bullets) in enumerate(people):
        x = ML + i * 6.10
        card(s, x, 1.62, 5.85, 3.62, fill=WHITE, line=LINE, accent=color)
        text(s, x + 0.28, 1.78, 4.0, 0.32, name, size=16, bold=True, color=INK,
             font=FONT_LIGHT)
        text(s, x + 0.28, 2.10, 3.0, 0.24, roll, size=9.5, color=MUTED)
        chip(s, x + 3.95, 1.80, 1.65, 0.30, tag, fill=fill, color=color, size=8.2)
        paragraphs(s, x + 0.28, 2.52, 5.30, 2.55,
                   [P(t, bullet=True, size=10.5, sa=10) for t in bullets])

    rect(s, ML, 5.45, CW, 0.86, fill=INK, line=None, radius=0.10)
    text(s, ML + 0.28, 5.58, CW - 0.6, 0.62,
         "Shared by both: literature review, dataset curation, end-to-end testing, documentation and "
         "presentation. Each workstream is owned end to end and reviewed weekly with the mentor; the "
         "Git log, notebook revisions and experiment folders provide the audit trail.",
         size=10.5, color=RGBColor(0xD5, 0xE2, 0xEA), line_spacing=1.14)

    text(s, ML, 6.44, CW, 0.28,
         "Evidence available on request: training notebooks, evaluation CSVs, exported models and "
         "parity fixtures, Android module history.",
         size=9.3, italic=True, color=MUTED)

    footer(s, 19)
    s.notes_slide.notes_text_frame.text = (
        "The work split is deliberate: one of us owns data and models, the other owns the app and "
        "integration, and everything else - literature, testing, documentation - is shared. Both "
        "workstreams produced artefacts you have already seen: notebooks and export fixtures on one "
        "side, the Android module tree on the other. We meet the mentor weekly and log progress in "
        "the repository.")


# ------------------------------------------------------------------ 20 management
def slide_management(prs):
    s = new_slide(prs)
    header(s, 20, "Project management", "Plan, progress and the risks we are tracking",
           "Ten-month plan with a review checkpoint each phase; three of nine phases are complete today.")

    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]
    x0, grid_w = 2.42, 10.05
    step = grid_w / 10.0
    for i, m in enumerate(months):
        text(s, x0 + i * step, 1.68, step, 0.22, m, size=8.5, bold=True,
             color=MUTED, align=PP_ALIGN.CENTER)
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                   Inches(x0 + i * step), Inches(1.92),
                                   Inches(x0 + i * step), Inches(5.14))
        ln.line.color.rgb = RGBColor(0xEC, 0xF0, 0xF3)
        ln.line.width = Pt(0.75)

    phases = [
        ("Literature, datasets, scope", 0, 2, TEAL),
        ("Baseline LSTM, P1 review", 1, 3, TEAL),
        ("Preprocessing + two CNNs", 2, 4, TEAL),
        ("Android app shell", 2, 5, TEAL),
        ("CNN integration, escalation", 4, 6, ORANGE),
        ("Reviewed labels, pocket data", 5, 7, GREY),
        ("Pilot validation", 6, 8, GREY),
        ("Paper draft, similarity check", 7, 9, GREY),
        ("Patent decision, final review", 8, 10, GREY),
    ]
    y = 2.00
    for label, a, b, color in phases:
        text(s, ML, y - 0.02, 1.60, 0.24, label, size=9, color=INK, line_spacing=1.0)
        rect(s, x0 + a * step, y + 0.045, max((b - a) * step - 0.05, 0.22), 0.19,
             fill=color, radius=0.5)
        y += 0.34

    for pos, label, color in [(2.0, "P1 review", MUTED), (4.0, "P2 \u00b7 today", ORANGE),
                              (10.0, "Final", MUTED)]:
        xx = min(x0 + pos * step, x0 + grid_w - 0.01)
        mt = text(s, xx - 0.55, 5.16, 1.10, 0.22, label, size=8.2, bold=True,
                  color=color, align=PP_ALIGN.CENTER)
        mt.text_frame.paragraphs[0].runs[0].font.color.rgb = color

    rect(s, ML, 5.46, CW, 0.012, fill=LINE, shape=MSO_SHAPE.RECTANGLE)
    text(s, ML, 5.52, 4.0, 0.22, "KEY RISKS AND MITIGATION", size=9, bold=True,
         color=ORANGE, spc=1.1)
    risks = [
        ("Provisional labels", "Human-reviewed subset for the held-out split before the pilot."),
        ("Waist \u2192 pocket gap", "Own pocket-phone recordings; UniMiB model as the deployment path."),
        ("Battery at 50 Hz", "Stage-1 gating, wake lock scoped to monitoring; benchmark in December."),
        ("SMS DLT approval", "Start carrier registration early; siren plus local log as fallback."),
    ]
    for i, (title, body) in enumerate(risks):
        x = ML + i * 3.00
        rect(s, x, 5.76, 2.85, 0.92, fill=MIST, line=None)
        text(s, x + 0.16, 5.84, 2.55, 0.22, title, size=9.2, bold=True, color=INK)
        text(s, x + 0.16, 6.06, 2.58, 0.56, body, size=8.3, color=GREY, line_spacing=1.06)

    footer(s, 20)
    s.notes_slide.notes_text_frame.text = (
        "The plan has nine phases across ten months. The dark teal bars are complete or nearly "
        "complete - literature, the baseline LSTM from the first review, preprocessing, the two "
        "CNNs, and the app shell. The orange bar is what we are working on now: wiring the exported "
        "CNN into the service and finishing escalation. Grey bars are planned. The four risks below "
        "are the ones we actively manage, each with a concrete mitigation.")


# ------------------------------------------------------------------ 21 cost
def slide_cost(prs):
    s = new_slide(prs)
    header(s, 21, "Cost & scalability", "Near-zero recurring cost per user, and it scales without a server",
           "Indicative figures for an Indian deployment; nothing here requires a subscription.")

    rows = [["Item", "Choice made", "Indicative cost"],
            ["Model training compute", "Google Colab free GPU tier (T4); Pro optional", "\u20b90  (Pro \u20b91,000 / month, optional)"],
            ["Development tools", "Android Studio, Kotlin, TensorFlow, TensorFlow Lite", "\u20b90 \u2014 open source"],
            ["Backend / cloud", "None: all inference and storage on the phone", "\u20b90 per month, ever"],
            ["Test device", "Existing Android smartphone", "\u20b90 incremental"],
            ["Datasets", "SisFall Original and UniMiB SHAR, research licences", "\u20b90"],
            ["Emergency SMS", "Carrier transactional SMS, 1\u20133 alerts per user per month", "\u2248 \u20b90.15\u20130.25 per SMS"],
            ["Distribution (optional)", "Google Play developer account, one time", "$25 \u2248 \u20b92,100"]]
    table(s, ML, 1.62, CW, rows, [2.95, 5.65, 3.29], fs=10.3, hfs=9.3, rh=0.425,
          bold_first=True)

    kpis = [("\u20b90", "recurring platform cost", "no server, subscription or per-request fee"),
            ("68 KB", "model shipped to the device", "no per-request or per-token cost"),
            ("\u20b94k\u201325k", "device cost avoided", "versus commercial fall pendants")]
    for i, (v, l, sub) in enumerate(kpis):
        kpi(s, ML + i * 4.04, 5.08, 3.80, 1.10, v, l, sub=sub,
            color=TEAL if i != 1 else GREEN, fill=MIST if i != 1 else GREEN_SOFT,
            value_size=22)

    text(s, ML, 6.28, CW, 0.60,
         "Scaling: cost per additional user is effectively zero, the model runs on Android 8 and above "
         "(\u2248 95% of active devices), and results are unaffected by user count. The path to reach is "
         "localisation, a caregiver companion app and optional cloud backup \u2014 all additive, none required "
         "for the core safety function.",
         size=9.8, color=GREY, line_spacing=1.14)

    footer(s, 21)
    s.notes_slide.notes_text_frame.text = (
        "The economics are the strongest part of the pitch. Training ran on a free Colab GPU, the "
        "toolchain is open source, and because inference is on the device there is no server bill at "
        "all. The only running cost is the emergency SMS, about twenty paise per message, one to "
        "three a month. A commercial pendant costs four to twenty-five thousand rupees plus a "
        "monthly plan. Cost per extra user here is essentially zero, which is what makes it scalable.")


# ------------------------------------------------------------------ 22 ethics
def slide_ethics(prs):
    s = new_slide(prs)
    header(s, 22, "Ethics & sustainability", "Privacy by architecture, safety stated honestly",
           "Because nothing is uploaded, the ethical surface is much smaller \u2014 but the safety limits must be said out loud.")

    quads = [
        (TEAL, TEAL_SOFT, "PRIVACY AND CONSENT", [
            "Explicit permission and purpose notice at onboarding, before monitoring starts.",
            "Sensor streams never leave the device; only an emergency SMS carries data.",
            "Caregiver numbers stay in local storage and can be deleted by the user.",
            "Aligned with the DPDP Act 2023: notice, purpose limitation, retention and erasure.",
        ]),
        (RED, RED_SOFT, "SAFETY AND CLINICAL LIMITS", [
            "Not a medical device and not a substitute for medical care or supervision.",
            "False negatives are possible; the system is an additional layer, not the only one.",
            "Permissions, battery and sensor health are checked so silent failure is visible.",
            "No diagnosis, no medication advice, no health claims anywhere in the UI.",
        ]),
        (GREEN, GREEN_SOFT, "ENVIRONMENT", [
            "No additional hardware to manufacture, ship, charge or discard.",
            "68 KB model and local inference avoid continuous cloud compute and data transfer.",
            "Monitoring reuses an existing phone; the marginal energy is one sensor stream.",
            "Offline-first design means no data-centre footprint per user.",
        ]),
        (ORANGE, ORANGE_SOFT, "SOCIAL AND ECONOMIC SUSTAINABILITY", [
            "Supports independent living rather than institutional care.",
            "Zero recurring cost removes the subscription barrier for low-income households.",
            "Accessible interface: large controls, high contrast, plain language, voice-friendly.",
            "Caregivers get verified information instead of constant checking.",
        ]),
    ]
    for i, (edge, fill, tag, lines) in enumerate(quads):
        col, row = i % 2, i // 2
        x = ML + col * 6.10
        y = 1.58 + row * 2.60
        card(s, x, y, 5.85, 2.42, fill=fill, line=None)
        chip(s, x + 0.24, y + 0.18, 2.35, 0.28, tag, fill=WHITE, color=edge, size=8.2)
        paragraphs(s, x + 0.24, y + 0.58, 5.35, 1.75,
                   [P(t, bullet=True, size=9.8, sa=7) for t in lines])

    footer(s, 22)
    s.notes_slide.notes_text_frame.text = (
        "Ethically the design does most of the work: sensor data never leaves the phone, so the "
        "privacy risk is limited to the emergency message itself. We follow the DPDP Act on notice, "
        "purpose limitation and erasure. On safety we are deliberately conservative - this is not a "
        "medical device, false negatives are possible, and the UI makes no diagnostic claims. "
        "Environmentally there is no extra hardware and no cloud inference.")


# ------------------------------------------------------------------ 23 paper & IP
def slide_paper(prs):
    s = new_slide(prs)
    header(s, 23, "Research output", "Paper and patent readiness, with status stated plainly",
           "Data, figures and references are frozen from this run; writing and the similarity check are what remain.")

    card(s, ML, 1.62, 5.85, 4.62, fill=WHITE, line=LINE, accent=TEAL)
    text(s, ML + 0.28, 1.78, 4.0, 0.24, "MANUSCRIPT", size=9.2, bold=True, color=TEAL, spc=1.1)
    text(s, ML + 0.28, 2.04, 5.00, 0.56,
         "\u201cA Lightweight Two-Stage On-Device Fall Detection and Verification System for "
         "Smartphones\u201d", size=12, bold=True, color=INK, font=FONT_LIGHT,
         line_spacing=1.08)
    paragraphs(s, ML + 0.28, 2.68, 5.02, 2.10, [
        P("Contributions: two-stage rule plus CNN cascade at 50 Hz; subject-independent results on "
          "two corpora; event-level evaluation with false-alarm rate and delay; parity-verified "
          "TFLite deployment.", bullet=True, size=9.8, sa=7),
        P("Structure: abstract, introduction, related work, methodology, implementation, results, "
          "discussion, limitations, conclusion, references.", bullet=True, size=9.8, sa=7),
        P("Venue plan: IEEE / Springer conference on computing and pervasive healthcare; "
          "candidate venues shortlisted with the mentor.", bullet=True, size=9.8, sa=7),
        P("Plagiarism: Turnitin / iThenticate check before submission, target below 15% excluding "
          "references; datasets and prior work cited; tool use disclosed.", bullet=True, size=9.8, sa=7),
    ])
    chip(s, ML + 0.28, 5.02, 2.60, 0.30, "DRAFT IN PREPARATION", fill=ORANGE_SOFT,
         color=ORANGE, size=8.2)
    text(s, ML + 3.05, 5.02, 2.55, 0.30, "similarity report pending", size=8.6,
         color=MUTED)

    card(s, 6.10, 1.62, 5.85, 4.62, fill=WHITE, line=LINE, accent=ORANGE)
    text(s, 6.38, 1.78, 4.0, 0.24, "PATENT READINESS", size=9.2, bold=True, color=ORANGE, spc=1.1)
    paragraphs(s, 6.38, 2.04, 5.32, 2.40, [
        P("Candidate novelty: a two-stage gate that discriminates phone drops from human falls and "
          "escalates only after an unanswered verification prompt, entirely offline.",
          bullet=True, size=9.8, sa=7),
        P("Prior-art search planned against IP India, Google Patents and Espacenet; fall detection "
          "is crowded art, so the claim would rest on the verification-plus-escalation combination.",
          bullet=True, size=9.8, sa=7),
        P("Status: not filed. Decision gate is the prior-art result, taken with the mentor.",
          bullet=True, size=9.8, sa=7),
    ])
    text(s, 6.38, 4.06, 5.32, 0.22, "TECHNICAL COMMUNICATION", size=9, bold=True,
         color=MUTED, spc=1.1)
    paragraphs(s, 6.38, 4.32, 5.32, 1.30, [
        P("This deck, a recorded demo, the repository README and a model card for each exported "
          "network.", bullet=True, size=9.8, sa=7),
        P("Reproducibility package: notebooks, environment manifest, preprocessing fixtures and "
          "parity tests.", bullet=True, size=9.8, sa=7),
    ])
    chip(s, 6.38, 5.72, 2.60, 0.30, "NOT FILED \u2014 SEARCH PLANNED", fill=RED_SOFT,
         color=RED, size=8.2)

    rect(s, ML, 6.42, CW, 0.46, fill=MIST, line=None, radius=0.10)
    text(s, ML + 0.24, 6.52, CW - 0.5, 0.28,
         "Submission readiness: results and figures are final for this run; remaining work is "
         "writing, internal review and the similarity report.",
         size=9.8, color=INK)

    footer(s, 23)
    s.notes_slide.notes_text_frame.text = (
        "On the research side, the paper is in preparation with a clear contribution list and a "
        "target of an IEEE or Springer conference. The similarity check happens before submission "
        "and we aim below fifteen percent excluding references. On patent, we are honest: nothing is "
        "filed. Fall detection is crowded art, so the candidate claim would rest on the combination "
        "of drop discrimination, verification and offline escalation, and the decision depends on a "
        "prior-art search we still have to run.")


# ------------------------------------------------------------------ 24 roadmap / conclusion
def slide_conclusion(prs):
    s = new_slide(prs)
    header(s, 24, "Roadmap", "What happens between now and the final review",
           "Five steps, each with an owner and a month, focused on the gaps identified on slides 15 and 17.")

    steps = [
        ("Nov 2026", "Bind the exported CNN", "Replace the mock classifier, re-run parity on the "
                                              "device and measure per-window latency."),
        ("Dec 2026", "Finish escalation", "SMS with GPS link, auto-call, incident logging and "
                                          "false-alarm capture in the history screen."),
        ("Jan 2027", "Sharpen the labels", "Human-reviewed SisFall subset plus our own pocket "
                                           "recordings for event-level validation."),
        ("Feb 2027", "Validate with users", "Small caregiver pilot: acceptance, alert clarity and "
                                            "battery behaviour over full days."),
        ("Mar\u2013Apr 2027", "Publish and close", "Paper submission, prior-art decision, final "
                                                   "report and demonstration."),
    ]
    x = ML
    for i, (when, title, body) in enumerate(steps):
        rect(s, x, 1.66, 2.24, 1.86, fill=MIST, line=None)
        rect(s, x, 1.66, 2.24, 0.05, fill=ORANGE if i == 0 else TEAL,
             shape=MSO_SHAPE.RECTANGLE)
        text(s, x + 0.16, 1.80, 2.0, 0.22, when, size=8.6, bold=True, color=ORANGE)
        text(s, x + 0.16, 2.06, 1.96, 0.50, title, size=11, bold=True, color=INK,
             line_spacing=1.05)
        text(s, x + 0.16, 2.62, 1.96, 0.82, body, size=8.6, color=GREY, line_spacing=1.08)
        x += 2.41

    rect(s, ML, 3.78, CW, 2.90, fill=INK, line=None, radius=0.10)
    text(s, ML + 0.34, 3.94, 6.0, 0.26, "CONCLUSION", size=9.5, bold=True,
         color=ORANGE, spc=1.4)
    paragraphs(s, ML + 0.34, 4.26, 11.2, 1.05, [
        P("Two subject-independent CNNs trained, evaluated and exported \u2014 68 KB accelerometer-only "
          "model ready for the phone, 104 KB six-axis model retained as a reference.",
          bullet=True, size=11, sa=8, color=RGBColor(0xE6, 0xEE, 0xF3)),
        P("Deployment path verified end to end at the model level: export parity within 3e-9 and "
          "8e-8, with a versioned sensor, preprocessing and alarm contract.",
          bullet=True, size=11, sa=8, color=RGBColor(0xE6, 0xEE, 0xF3)),
        P("Remaining work is concentrated and named: CNN binding, SMS and GPS escalation, "
          "human-reviewed labels and field validation.",
          bullet=True, size=11, sa=8, color=RGBColor(0xE6, 0xEE, 0xF3)),
    ])
    rect(s, ML + 0.34, 5.62, 11.2, 0.85, fill=RGBColor(0x14, 0x35, 0x52), line=None)
    text(s, ML + 0.58, 5.74, 10.8, 0.30,
         "A fall should never wait for someone to notice.", size=15, bold=True,
         color=WHITE, font=FONT_LIGHT)
    text(s, ML + 0.58, 6.06, 10.8, 0.30,
         "SevaLink turns the phone already in the pocket into a caregiver alert that works without "
         "internet, without extra hardware and without a subscription.",
         size=10, color=RGBColor(0xA9, 0xBE, 0xCB))

    footer(s, 24)
    s.notes_slide.notes_text_frame.text = (
        "The plan from here is concrete. In November we bind the exported model and measure latency. "
        "In December we finish SMS, GPS and incident logging. In January we human-review the labels "
        "and record our own pocket data. February is a small caregiver pilot, and March to April is "
        "the paper, the patent decision and the final report. To close: two models trained and "
        "exported, the deployment contract verified, and a short, named list of remaining work.")


# ------------------------------------------------------------------ 25 thanks
def slide_thanks(prs):
    s = new_slide(prs, bg=INK)
    rect(s, 9.30, -0.90, 5.4, 5.4, fill=None, line=RGBColor(0x23, 0x51, 0x69), lw=1.2,
         shape=MSO_SHAPE.OVAL)
    rect(s, 10.80, 2.60, 3.6, 3.6, fill=None, line=RGBColor(0x23, 0x51, 0x69), lw=1.2,
         shape=MSO_SHAPE.OVAL)
    rect(s, 11.95, 5.30, 0.5, 0.5, fill=ORANGE, shape=MSO_SHAPE.OVAL)

    text(s, 1.00, 2.10, 8.0, 0.30, "THANK YOU", size=11, bold=True, color=ORANGE, spc=2.0)
    text(s, 0.95, 2.50, 8.5, 1.00, "Questions and discussion", size=40, bold=True,
         color=WHITE, font=FONT_LIGHT)
    rect(s, 1.00, 3.68, 1.55, 0.045, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)
    text(s, 1.00, 3.94, 8.2, 0.60,
         "We are happy to walk through the notebooks, the exported models or the Android module "
         "tree in detail.", size=12.5, color=RGBColor(0xAF, 0xC4, 0xD0), line_spacing=1.14)

    text(s, 1.00, 5.05, 4.6, 0.24, "TEAM", size=9, bold=True,
         color=RGBColor(0x7F, 0x9B, 0xAC), spc=1.4)
    text(s, 1.00, 5.30, 5.0, 0.28, "Bhumika Rajoria  \u00b7  Anshita Singh", size=13,
         bold=True, color=WHITE)
    text(s, 1.00, 5.58, 5.4, 0.26, "2300291530054  \u00b7  2300291530033", size=10.5,
         color=RGBColor(0xA9, 0xBE, 0xCB))

    text(s, 6.60, 5.05, 5.8, 0.24, "GUIDANCE", size=9, bold=True,
         color=RGBColor(0x7F, 0x9B, 0xAC), spc=1.4)
    text(s, 6.60, 5.30, 5.8, 0.28, "Dr. Mukesh Kumar Tripathi", size=13, bold=True,
         color=WHITE)
    text(s, 6.60, 5.58, 5.8, 0.26, "Department of CSE (AI & ML), KIET Deemed to be University",
         size=10.5, color=RGBColor(0xA9, 0xBE, 0xCB))

    s.notes_slide.notes_text_frame.text = (
        "Thank you. We are happy to go into any part in detail - the notebooks, the exported models "
        "or the Android modules - and backup slides carry the full metric tables and references.")


# ------------------------------------------------------------------ 26 backup: metrics
def slide_backup_metrics(prs):
    s = new_slide(prs)
    header(s, 26, "Backup", "Full metric tables, both models, all splits",
           "Values exactly as produced by the executed notebooks; no post-hoc adjustment.")

    rows = [["Dataset", "Split", "Accuracy", "Precision", "Recall", "Specificity", "F1",
             "Event sens.", "Alarms / h", "Delay"],
            ["SisFall", "train", "99.88%", "99.65%", "96.44%", "99.99%", "98.02%", "95.83%", "0.51", "0.33 s"],
            ["SisFall", "validation", "99.89%", "100.00%", "96.00%", "100.00%", "97.96%", "92.00%", "0.00", "0.33 s"],
            ["SisFall", "test", "99.63%", "96.28%", "90.65%", "99.89%", "93.38%", "90.33%", "2.77", "0.32 s"],
            ["UniMiB", "test", "97.82%", "94.96%", "98.42%", "97.54%", "96.66%", "n/a", "n/a", "n/a"]]
    table(s, ML, 1.62, CW, rows, [1.35, 1.30, 1.15, 1.18, 1.10, 1.30, 1.05, 1.20, 1.16, 1.10],
          fs=9.8, hfs=8.8, rh=0.43, bold_first=True,
          align=[PP_ALIGN.LEFT, PP_ALIGN.LEFT] + [PP_ALIGN.RIGHT] * 8)

    text(s, ML, 3.86, CW, 0.24, "SISFALL \u00b7 WINDOW COUNTS AND ALARM DETAIL", size=9.2,
         bold=True, color=ORANGE, spc=1.1)
    rows2 = [["Split", "Non-fall windows", "Fall windows", "Ambiguous", "Alarm events",
              "Unmatched fall-trial alarms"],
             ["train", "73,448", "2,390", "12,265", "1,193", "41"],
             ["validation", "20,350", "600", "3,186", "297", "21"],
             ["test", "19,975", "599", "3,013", "295", "18"]]
    table(s, ML, 4.12, CW, rows2, [1.85, 2.25, 1.85, 1.65, 1.85, 2.44], fs=9.8, hfs=8.8,
          rh=0.42, bold_first=True,
          align=[PP_ALIGN.LEFT] + [PP_ALIGN.RIGHT] * 5)

    text(s, ML, 6.06, CW, 1.10,
         "Interpretation: SisFall window metrics use provisional rule-based labels (2 of 1,198 "
         "training falls human-reviewed); validation and test event metrics are therefore "
         "rule-consistency measures. UniMiB metrics are window-level only, because the corpus is "
         "pre-segmented and cannot support false-alarms-per-hour. Precision for UniMiB is derived "
         "from the reported confusion matrix (622 TP / 655 predicted fall).",
         size=9.6, color=GREY, line_spacing=1.16)

    footer(s, 26)
    s.notes_slide.notes_text_frame.text = (
        "This is the raw table if anyone wants exact figures. Note the SisFall test row is the "
        "weakest: 90.65% recall at window level, 90.33% at event level, 2.77 false alarms per hour. "
        "The train row is included only for completeness and is not evidence of generalisation.")


# ------------------------------------------------------------------ 27 backup: model cards
def slide_backup_models(prs):
    s = new_slide(prs)
    header(s, 27, "Backup", "Model cards and the deployment contract",
           "Everything a reviewer or a future maintainer needs to reproduce or replace a model.")

    rows = [["", "SisFall 6-axis CNN", "UniMiB accelerometer CNN"],
            ["Task", "Binary fall / no-fall over 3 s", "Binary fall / no-fall over 2 s"],
            ["Input", "1 \u00d7 150 \u00d7 6 float32, normalised",
             "1 \u00d7 100 \u00d7 4 float32, normalised"],
            ["Channels", "acc x, y, z \u00b7 gyro x, y, z", "acc x, y, z \u00b7 magnitude"],
            ["Architecture", "3 \u00d7 Conv1D + pool \u2192 GAP \u2192 Dense 32 \u2192 sigmoid",
             "3 \u00d7 dual separable conv + ECA \u2192 GAP \u2192 Dense 1"],
            ["Parameters", "25,761  \u00b7  100.6 KB", "12,432  \u00b7  48.6 KB"],
            ["Loss / optimiser", "Binary cross-entropy \u00b7 Adam 1e-3",
             "Focal loss (\u03b1 0.75, \u03b3 2) \u00b7 AdamW 5e-4"],
            ["Selection metric", "Validation PR-AUC (0.9966)", "Validation AUPRC (0.9979)"],
            ["Threshold", "0.995, chosen on validation only", "0.5, default"],
            ["Alarm policy", "Rising edge of a positive run, 5 s cooldown, per-trial reset",
             "Same policy applied to continuous data"],
            ["Prediction availability", "Exclusive window end + 100 ms", "Exclusive window end + 100 ms"],
            ["Known limitations", "Provisional labels; waist-mounted domain; recall 90.7%",
             "Pre-segmented corpus; no event-level metric"],
            ["Role", "Reference model where a gyroscope exists", "Deployment model across the fleet"]]
    table(s, ML, 1.62, CW, rows, [2.10, 4.60, 5.19], fs=9.5, hfs=9,
          rh=0.332, bold_first=True)

    text(s, ML, 6.28, CW, 0.46,
         "Both models are float32 TFLite with built-in operators only, and both were exported "
         "through the same parity gate. Preprocessing is outside the graph by design, so the phone "
         "and the notebook run identical code paths.",
         size=9.6, color=GREY, line_spacing=1.14)

    footer(s, 27)
    s.notes_slide.notes_text_frame.text = (
        "The model cards summarise everything needed to reproduce or replace either network: inputs, "
        "architecture, losses, selection metric, threshold, alarm policy and known limitations.")


# ------------------------------------------------------------------ 28 backup: references
def slide_backup_refs(prs):
    s = new_slide(prs)
    header(s, 28, "Backup", "Datasets, standards and references",
           "Everything used in this project is public and cited; no proprietary or personal data was used.")

    refs = [
        ("Datasets", [
            "Sucerquia A., L\u00f3pez J. D., Vargas-Bonilla J. F., \u201cSisFall: A Fall and Movement "
            "Dataset\u201d, Sensors, 2017.  (waist-mounted accelerometer + gyroscope, 38 participants)",
            "Micucci D., Mobilio M., Napoletano P., \u201cUniMiB SHAR: A Dataset for Human Activity "
            "Recognition Using Acceleration Data from Smartphones\u201d, Applied Sciences, 2017. "
            "(pocket smartphone, 30 participants)",
        ]),
        ("Standards and guidance", [
            "World Health Organization, Falls fact sheet \u2014 global fall incidence and injury burden.",
            "Digital Personal Data Protection Act, 2023 (India) \u2014 consent notice, purpose limitation, "
            "retention and erasure obligations applied to the onboarding and storage design.",
            "TRAI / DLT registration requirements for transactional SMS in India \u2014 constrains the "
            "alert delivery path.",
        ]),
        ("Literature that shaped the approach", [
            "A Smartphone-Based Fall Detection System (2012) \u2014 early accelerometer-based detection "
            "with caregiver alerting.",
            "Fall Detection in Older Adults with Mobile IoT Devices and Machine Learning in the Cloud "
            "and on the Edge (2020) \u2014 edge versus cloud processing on SisFall.",
            "A Smartphone-Based Online System for Fall Detection with Alert Notifications and Contextual "
            "Information of Real-Life Falls (2021) \u2014 73% real-world sensitivity and phone drops as "
            "the dominant false-alarm source.",
            "Lightweight Multi-Channel Fall Detection on Smartphone Accelerometers with Probabilistic "
            "Calibration and Event-Level Evaluation (2026) \u2014 event-level metrics and calibrated "
            "thresholds, which shaped slide 12.",
        ]),
        ("Tooling", [
            "TensorFlow / Keras 2.21, LiteRT (ai-edge-litert) 2.3, Android Studio, Kotlin 2.0, "
            "Jetpack Compose, Hilt, Room, DataStore.",
        ]),
    ]
    y = 1.62
    for heading, items in refs:
        text(s, ML, y, 4.0, 0.24, heading.upper(), size=9, bold=True, color=ORANGE, spc=1.1)
        paragraphs(s, ML, y + 0.26, CW, 1.0,
                   [P(t, bullet=True, size=9.4, sa=6) for t in items])
        y += 0.30 + 0.26 * len(items) + 0.34

    footer(s, 28)
    s.notes_slide.notes_text_frame.text = (
        "References for the datasets, the standards that constrain the design, the literature that "
        "shaped it, and the toolchain. All sources are public and cited in the manuscript.")


def build(prs):
    slide_team(prs)
    slide_management(prs)
    slide_cost(prs)
    slide_ethics(prs)
    slide_paper(prs)
    slide_conclusion(prs)
    slide_thanks(prs)
    slide_backup_metrics(prs)
    slide_backup_models(prs)
    slide_backup_refs(prs)
