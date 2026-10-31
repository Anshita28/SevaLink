"""Slides 10-18: UniMiB model, training protocol, results, validation, deployment, app."""

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from deck_lib import *


# ------------------------------------------------------------------ 10 UniMiB model
def slide_model_unimib(prs):
    s = new_slide(prs)
    header(s, 10, "Model 2", "UniMiB: separable convolutions with channel attention",
           "The deployment model \u2014 accelerometer only, 12,432 parameters, 68 KB.")

    blocks = [("Input", "100 \u00d7 4", "ax, ay, az, |a|"),
              ("Stage 1", "32 filters", "dual k=3 / k=5"),
              ("Stage 2", "64 filters", "dual k=3 / k=5"),
              ("Stage 3", "128 filters", "dual k=3 / k=5"),
              ("GAP", "\u2192 128", "global average"),
              ("Dense 1", "sigmoid", "fall probability")]
    x = ML
    w, gap = 1.85, 0.14
    for i, (l1, l2, l3) in enumerate(blocks):
        fill = ORANGE_SOFT if i == 5 else MIST
        rect(s, x, 1.62, w, 1.05, fill=fill, line=None)
        text(s, x + 0.12, 1.73, w - 0.2, 0.26, l1, size=11, bold=True, color=INK)
        text(s, x + 0.12, 2.00, w - 0.2, 0.22, l2, size=9, bold=True,
             color=ORANGE if i == 5 else TEAL)
        text(s, x + 0.12, 2.24, w - 0.2, 0.30, l3, size=8.2, color=GREY, line_spacing=1.0)
        if i < 5:
            arrow(s, x + w + 0.01, 2.06, 0.12, 0.16)
        x += w + gap
    text(s, ML, 2.76, CW, 0.24,
         "Every stage: separable conv k=3  \u2225  separable conv k=5  \u2192  concatenate  \u2192  batch norm  \u2192  ReLU  \u2192  ECA attention",
         size=9.3, color=GREY)

    kpis = [("12,432", "parameters"), ("48.6 KB", "float32 model"),
            ("0.9979", "best val PR-AUC"), ("42", "epochs trained")]
    for i, (v, l) in enumerate(kpis):
        kpi(s, ML + i * 3.00, 3.10, 2.85, 1.05, v, l, color=GREEN, fill=GREEN_SOFT,
            value_size=22)

    text(s, ML, 4.44, 5.6, 0.24, "TRAINING RECIPE", size=9, bold=True, color=ORANGE, spc=1.2)
    paragraphs(s, ML, 4.72, 5.55, 1.90, [
        P("Focal loss \u03b1 = 0.75, \u03b3 = 2 for the 4,192 : 7,579 imbalance", bullet=True, size=10.5, sa=7),
        P("AdamW at 5e-4 with weight decay 1e-4", bullet=True, size=10.5, sa=7),
        P("Batch 128, early stopping patience 10", bullet=True, size=10.5, sa=7),
        P("Best validation AUPRC weights restored", bullet=True, size=10.5, sa=7),
    ])
    text(s, 6.78, 4.44, 5.6, 0.24, "WHY THIS ARCHITECTURE", size=9, bold=True,
         color=ORANGE, spc=1.2)
    paragraphs(s, 6.78, 4.72, 5.70, 1.90, [
        P("Separable convolutions cut multiply-accumulates by roughly an order of magnitude "
          "against dense convolution at the same width.", bullet=True, size=10.5, sa=7),
        P("ECA attention re-weights channels with a single 5-tap 1-D convolution \u2014 no dense "
          "attention block.", bullet=True, size=10.5, sa=7),
        P("The magnitude channel makes the model insensitive to how the phone is oriented in "
          "the pocket.", bullet=True, size=10.5, sa=7),
    ])

    footer(s, 10)
    s.notes_slide.notes_text_frame.text = (
        "The deployment model is an LFNet-style network rebuilt in Keras. Each stage runs two "
        "separable convolutions in parallel, concatenates them, then applies ECA attention. That "
        "keeps the model at 68 KB while reaching a best validation PR-AUC of 0.9979. Focal loss "
        "handles the fall-to-activity imbalance without discarding activity windows.")


# ------------------------------------------------------------------ 11 protocol
def slide_protocol(prs):
    s = new_slide(prs)
    header(s, 11, "Validation", "Training protocol: nothing is tuned on the test split",
           "Six controls that make these numbers mean something beyond a single lucky run.")

    cards = [
        ("Subject-wise splits", "38 and 30 participants; test subjects appear in no training, "
                                "no normalisation and no threshold search."),
        ("Imbalance handling", "Inverse-frequency class weights on SisFall; focal loss "
                               "(\u03b1 0.75, \u03b3 2) on UniMiB."),
        ("Checkpoint policy", "Weights kept only when validation PR-AUC improves; early stopping "
                              "limits adaptation to the validation split."),
        ("Threshold policy", "Swept on validation only, 0 to 1 in 0.005 steps plus a no-alarm "
                             "sentinel; the test split is never consulted."),
        ("Determinism", "Seed 42 across NumPy, TensorFlow and the split generator; deterministic "
                        "ops; hash-pinned preprocessing cache."),
        ("Software checks", "14 unit tests: units, alignment, gap handling, causal filter parity, "
                            "label boundaries, alarm cooldown, undefined metrics."),
    ]
    for i, (title, body) in enumerate(cards):
        col, row = i % 3, i // 3
        x = ML + col * 4.04
        y = 1.62 + row * 1.72
        card(s, x, y, 3.80, 1.55, fill=WHITE, line=LINE, accent=TEAL)
        text(s, x + 0.24, y + 0.14, 3.35, 0.26, f"{i + 1:02d}", size=11, bold=True,
             color=ORANGE, font=FONT_LIGHT)
        text(s, x + 0.70, y + 0.14, 2.95, 0.26, title, size=11.5, bold=True, color=INK)
        text(s, x + 0.24, y + 0.48, 3.42, 0.98, body, size=9.6, color=GREY, line_spacing=1.10)

    rect(s, ML, 5.24, CW, 1.28, fill=TEAL_SOFT, line=None, radius=0.10)
    text(s, ML + 0.28, 5.38, 8.0, 0.24, "SHIPPED WITH EVERY RUN",
         size=9, bold=True, color=TEAL, spc=1.2)
    text(s, ML + 0.28, 5.66, CW - 0.6, 0.78,
         "Input contract and sensor units  \u00b7  filter coefficients and sampling phase  \u00b7  normalisation "
         "statistics  \u00b7  decision threshold and its selection record  \u00b7  alarm policy  \u00b7  Keras/TFLite "
         "parity fixtures  \u00b7  annotation provenance  \u00b7  full environment manifest.",
         size=11, color=INK, line_spacing=1.15)

    footer(s, 11)
    s.notes_slide.notes_text_frame.text = (
        "The protocol is the reason we can defend these numbers. Splits are by subject; the test "
        "subjects are never used for fitting, normalising or threshold selection. We fix every seed, "
        "keep the best validation checkpoint, and run fourteen unit tests over the pipeline before "
        "training. Every artefact needed to reproduce a run is exported with the model.")


# ------------------------------------------------------------------ 12 SisFall results
def slide_results_sisfall(prs):
    s = new_slide(prs)
    header(s, 12, "Results \u00b7 SisFall", "99.6% window accuracy \u2014 recall is the number to watch",
           "Held-out: 7 participants never seen in training, 20,574 windows, 300 fall events.")

    rows = [["Window metric", "Value"],
            ["Accuracy", "99.63%"], ["Precision", "96.28%"], ["Recall (sensitivity)", "90.65%"],
            ["Specificity", "99.89%"], ["F1-score", "93.38%"],
            ["PR-AUC", "98.33%"], ["ROC-AUC", "99.86%"]]
    table(s, ML, 1.62, 5.35, rows, [3.25, 2.10], fs=10.5, hfs=9.5, rh=0.335,
          align=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT], bold_first=True)

    text(s, ML, 4.54, 5.35, 0.24, "CONFUSION MATRIX (WINDOWS)", size=8.8, bold=True,
         color=MUTED, spc=1.0)
    cm = [["", "Pred: no fall", "Pred: fall"],
          ["Actual: no fall", "19,954", "21"],
          ["Actual: fall", "56", "543"]]
    table(s, ML, 4.80, 5.35, cm, [2.05, 1.70, 1.60], fs=10, hfs=9, rh=0.30,
          align=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT], bold_first=True)

    kpis = [("90.3%", "fall events detected", "271 of 300 held-out falls"),
            ("2.77 / h", "non-fall alarms", "6 alarms in 7,804 s of ADL"),
            ("0.32 s", "mean detection delay", "impact to model decision"),
            ("0.995", "decision threshold", "selected on validation only")]
    for i, (v, l, sub) in enumerate(kpis):
        col, row = i % 2, i // 2
        x = 6.42 + col * 3.12
        y = 1.62 + row * 1.38
        kpi(s, x, y, 2.95, 1.24, v, l, sub=sub, color=TEAL, fill=MIST, value_size=24)

    text(s, 6.42, 4.42, 6.05, 1.40,
         "At the selected operating point the model trades a little recall for very few false "
         "alarms: validation event sensitivity was 92.0%, so the 95% event-level target was not "
         "attained, and the threshold was chosen to maximise sensitivity at zero validation "
         "false alarms.",
         size=10.5, color=GREY, line_spacing=1.14)

    rect(s, ML, 6.00, CW, 0.92, fill=ORANGE_SOFT, line=None, radius=0.10)
    rect(s, ML, 6.00, 0.055, 0.92, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)
    text(s, ML + 0.28, 6.12, CW - 0.6, 0.72,
         "Read this honestly: SisFall annotations in this run are provisional rule-based estimates "
         "(2 of 1,198 training falls were human-reviewed), so these figures measure rule consistency, "
         "not independently verified real-world sensitivity.",
         size=10.5, color=INK, line_spacing=1.12)

    footer(s, 12)
    s.notes_slide.notes_text_frame.text = (
        "On the SisFall test participants the model is extremely specific: 99.9% of non-fall windows "
        "are rejected, 21 false positives in twenty thousand windows. Recall is 90.7%, and at event "
        "level 271 of 300 falls were caught with six false alarms per 7,804 seconds of activity - "
        "about 2.8 per hour. The label caveat at the bottom is essential: these are provisional "
        "labels, so we present them as rule-consistency, not clinical sensitivity.")


# ------------------------------------------------------------------ 13 UniMiB results
def slide_results_unimib(prs):
    s = new_slide(prs)
    header(s, 13, "Results \u00b7 UniMiB SHAR", "Held-out accuracy 97.8% at 98.4% sensitivity",
           "1,975 windows from 5 participants never used in training, normalisation or thresholding.")

    kpis = [("97.82%", "accuracy", "1,932 of 1,975 correct", GREEN, GREEN_SOFT),
            ("98.42%", "sensitivity (recall)", "622 of 632 falls caught", GREEN, GREEN_SOFT),
            ("97.54%", "specificity", "1,310 of 1,343 activities", TEAL, MIST),
            ("96.66%", "F1-score", "precision 94.96%", TEAL, MIST)]
    for i, (v, l, sub, c, f) in enumerate(kpis):
        kpi(s, ML + i * 3.00, 1.62, 2.85, 1.30, v, l, sub=sub, color=c, fill=f,
            value_size=24)

    text(s, ML, 3.16, 5.9, 0.24, "CONFUSION MATRIX (WINDOWS)", size=8.8, bold=True,
         color=MUTED, spc=1.0)
    cm = [["", "Pred: no fall", "Pred: fall"],
          ["Actual: no fall", "1,310", "33"],
          ["Actual: fall", "10", "622"]]
    table(s, ML, 3.42, 5.55, cm, [2.15, 1.75, 1.65], fs=10.5, hfs=9.3, rh=0.36,
          align=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT], bold_first=True)
    text(s, ML, 4.92, 5.55, 0.70,
         "Only 10 missed falls and 33 false positives across the held-out split; the operating "
         "point is the default 0.5 threshold, with no test-set tuning.",
         size=10.5, color=GREY, line_spacing=1.12)

    card(s, 6.85, 3.16, 5.75, 1.22, fill=WHITE, line=LINE, accent=GREEN)
    text(s, 7.07, 3.28, 5.3, 0.26, "PR-AUC ON HELD-OUT SUBJECTS", size=8.8, bold=True,
         color=MUTED, spc=1.0)
    text(s, 7.07, 3.54, 5.3, 0.40, "99.04%", size=24, bold=True, color=GREEN,
         font=FONT_LIGHT)
    text(s, 8.55, 3.66, 3.9, 0.60,
         "Threshold-free ranking quality: the model separates falls from daily activity across "
         "the whole score range, not just at 0.5.",
         size=9.6, color=GREY, line_spacing=1.08)

    card(s, 6.85, 4.54, 5.75, 1.08, fill=MIST, line=None)
    text(s, 7.07, 4.66, 5.3, 0.26, "OPERATING POINT", size=8.8, bold=True, color=MUTED, spc=1.0)
    text(s, 7.07, 4.92, 5.35, 0.60,
         "Recall 98.4% against specificity 97.5%: the model errs slightly towards detecting, "
         "which is the right bias for a safety system.",
         size=10, color=INK, line_spacing=1.10)

    rect(s, ML, 6.00, CW, 0.92, fill=ORANGE_SOFT, line=None, radius=0.10)
    rect(s, ML, 6.00, 0.055, 0.92, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)
    text(s, ML + 0.28, 6.12, CW - 0.6, 0.72,
         "UniMiB SHAR ships pre-segmented windows, so no false-alarms-per-hour or detection-delay "
         "metric is possible on this corpus. Event-level evaluation is therefore reported on the "
         "continuous SisFall recordings (previous slide).",
         size=10.5, color=INK, line_spacing=1.12)

    footer(s, 13)
    s.notes_slide.notes_text_frame.text = (
        "This is the model we deploy. On five unseen participants it reaches 97.8% accuracy with "
        "98.4% sensitivity - only ten falls missed in the whole test split - and a PR-AUC of 0.990. "
        "The bias is towards detection, which is correct for a safety system, and the cost is 33 "
        "false positives in 1,343 activity windows. UniMiB is pre-segmented, so false-alarm-per-hour "
        "is measured on SisFall instead.")


# ------------------------------------------------------------------ 14 comparison
def slide_compare(prs):
    s = new_slide(prs)
    header(s, 14, "Analysis", "What the comparison does and does not tell us",
           "Same metrics, same split logic, different test protocols \u2014 read the trends, not the decimals.")

    bar_chart(s, ML, 1.62, 6.55, 4.20,
              ["Accuracy", "Sensitivity", "Precision", "Specificity"],
              [("SisFall (6-axis)", (99.63, 90.65, 96.28, 99.89)),
               ("UniMiB (accelerometer)", (97.82, 98.42, 94.96, 97.54))],
              [TEAL, GREEN], vmin=70, vmax=103)
    text(s, ML, 5.86, 6.55, 0.24,
         "Window-level, held-out participants. Vertical axis starts at 70% for readability.",
         size=8.5, italic=True, color=MUTED)

    items = [
        ("Sensitivity", "The accelerometer-only model is 7.8 points better on recall \u2014 the "
                        "metric that matters for a safety device."),
        ("Specificity", "SisFall wins on specificity because its threshold was pushed to 0.995 "
                        "by the zero-false-alarm selection rule."),
        ("Precision", "Both models are within 1.3 points: no model is buying recall with a flood "
                      "of false alarms."),
        ("Protocol", "SisFall is continuous (event metrics possible); UniMiB is pre-segmented "
                     "(window metrics only). Absolute values are not directly comparable."),
        ("Domain", "UniMiB (trouser pocket) is closer to deployment than SisFall (waist-mounted); "
                   "the waist-to-pocket gap remains our main open risk."),
    ]
    paragraphs(s, 7.55, 1.62, 5.10, 4.60,
               [P([(h + " \u2014 ", {"b": True}), (b, {})], bullet=True, size=10.5, sa=11)
                for h, b in items])

    rect(s, ML, 6.22, CW, 0.70, fill=TEAL_SOFT, line=None, radius=0.10)
    text(s, ML + 0.28, 6.36, CW - 0.6, 0.46,
         "Working conclusion: ship the accelerometer-only model. Gyroscope data does not earn its "
         "extra sensor stream at these operating points, and the pocket protocol matches real use.",
         size=11, color=INK, line_spacing=1.10)

    footer(s, 14)
    s.notes_slide.notes_text_frame.text = (
        "Comparing the two directly: the accelerometer-only model is stronger on recall, the "
        "six-axis model is stronger on specificity because its threshold was pushed to 0.995 to "
        "avoid any validation false alarm. Precision is nearly identical. The important caveat is "
        "that the test sets are different - one continuous, one pre-segmented - so we read the "
        "trend, not the decimals. Our conclusion is to ship the accelerometer-only model.")


# ------------------------------------------------------------------ 15 validation limits
def slide_limits(prs):
    s = new_slide(prs)
    header(s, 15, "Validation", "What is proven, what is not, and what could break it",
           "Stated up front so the results are read at the right strength.")

    quads = [
        (GREEN, GREEN_SOFT, "VALIDATED", [
            "Subject-independent results on two public corpora.",
            "Export parity: Keras vs LiteRT within 3.0e-9 (SisFall) and 7.8e-8 (UniMiB).",
            "14 pipeline tests plus a versioned preprocessing contract.",
            "Threshold and alarm policy fixed before the test split was scored.",
        ]),
        (ORANGE, ORANGE_SOFT, "NOT YET VALIDATED", [
            "SisFall fall labels are provisional rule-based estimates, not human-reviewed events.",
            "No event-level false-alarm rate on continuous pocket-phone data.",
            "Android latency, battery draw and field false alarms are unmeasured.",
            "No independent clinician or caregiver review of alert usability yet.",
        ]),
        (RED, RED_SOFT, "THREATS TO VALIDITY", [
            "Waist-mounted training data vs pocket-mounted deployment.",
            "Simulated falls with mostly young participants.",
            "Threshold and normalisation transfer between corpora.",
            "Small test splits: 7 SisFall and 5 UniMiB held-out participants.",
        ]),
        (TEAL, TEAL_SOFT, "MITIGATION IN FLIGHT", [
            "Human-reviewed annotation subset for the held-out split.",
            "Our own pocket-phone recordings for domain adaptation.",
            "On-device benchmark plus a small caregiver pilot before the final review.",
            "Confidence intervals reported alongside the final event metrics.",
        ]),
    ]
    for i, (edge, fill, tag, lines) in enumerate(quads):
        col, row = i % 2, i // 2
        x = ML + col * 6.10
        y = 1.58 + row * 2.60
        card(s, x, y, 5.85, 2.42, fill=fill, line=None)
        chip(s, x + 0.24, y + 0.18, 1.60, 0.28, tag, fill=WHITE, color=edge, size=8.2)
        paragraphs(s, x + 0.24, y + 0.60, 5.35, 1.70,
                   [P(t, bullet=True, size=10, sa=8) for t in lines])

    footer(s, 15)
    s.notes_slide.notes_text_frame.text = (
        "We want to be explicit about strength of evidence. What is proven: subject-independent "
        "results on two corpora, exact export parity, and a tested pipeline. What is not: human-"
        "reviewed SisFall labels, continuous pocket-phone event metrics, and any Android latency or "
        "battery measurement. The threats and our mitigations are on the right. This is the slide "
        "that tells you where our remaining work is.")


# ------------------------------------------------------------------ 16 deployment
def slide_deploy(prs):
    s = new_slide(prs)
    header(s, 16, "Implementation", "Both models exported and verified against the on-device runtime",
           "The deployment artefact is not released until Keras and the LiteRT interpreter agree on held-out windows.")

    rows = [["Model", "Input tensor", "Parameters", "File size", "Max abs. parity error"],
            ["SisFall 6-axis CNN", "1 \u00d7 150 \u00d7 6  float32", "25,761", "103.9 KB", "3.0e-9"],
            ["UniMiB accelerometer CNN", "1 \u00d7 100 \u00d7 4  float32", "12,432", "67.8 KB", "7.8e-8"]]
    table(s, ML, 1.62, CW, rows, [3.05, 2.55, 1.85, 1.75, 2.69], fs=10.8, hfs=9.5,
          rh=0.50, bold_first=True,
          align=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT])

    labels = [("EXPORT CONTRACT", GREEN, [
        "Preprocessing runs on the phone; the graph accepts already-normalised windows.",
        "Alarm policy fixed with the model: rising edge of a positive run, 5 s cooldown.",
        "Prediction availability = window end + 100 ms, so escalation timing is deterministic.",
        "Sensor units, filter coefficients and normalisation travel with the model file.",
    ]), ("STILL OPEN", ORANGE, [
        "int8 post-training quantisation and its parity re-check.",
        "On-device inference latency per window on mid-range hardware.",
        "Battery profile for a full day at 50 Hz with the wake lock held.",
        "End-to-end alert delivery timing over the carrier SMS route.",
    ])]
    for i, (title, color, lines) in enumerate(labels):
        x = ML + i * 6.10
        card(s, x, 3.42, 5.85, 2.42, fill=WHITE, line=LINE, accent=color)
        text(s, x + 0.26, 3.54, 5.3, 0.24, title, size=9.2, bold=True, color=color, spc=1.1)
        paragraphs(s, x + 0.26, 3.86, 5.35, 1.85,
                   [P(t, bullet=True, size=10, sa=8) for t in lines])

    rect(s, ML, 6.06, CW, 0.86, fill=TEAL_SOFT, line=None, radius=0.10)
    text(s, ML + 0.28, 6.18, CW - 0.6, 0.60,
         "The export gate is enforced in code: the .tflite file is written only after Keras and "
         "LiteRT outputs agree within atol 1e-5 and rtol 1e-4. Both models passed.",
         size=11, color=INK, line_spacing=1.12)

    footer(s, 16)
    s.notes_slide.notes_text_frame.text = (
        "Deployment matters more than notebook accuracy, so we gate the export: the tflite file is "
        "only written if Keras and the LiteRT interpreter agree on the same held-out windows - "
        "three in a billion for SisFall, eight in a hundred million for UniMiB. The left column is "
        "the contract we ship; the right column is what is still open: quantisation, on-device "
        "latency, battery, and SMS delivery timing.")


# ------------------------------------------------------------------ 17 android
def slide_android(prs):
    s = new_slide(prs)
    header(s, 17, "Implementation", "The Android app: architecture and current build status",
           "Kotlin, Jetpack Compose, Hilt, Room and a foreground sensor service \u2014 an honest progress read-out.")

    layers = [
        ("UI", "Compose screens: onboarding, dashboard, contacts, history, settings, fall alert overlay"),
        ("State", "ViewModels with StateFlow; one UI state object per screen"),
        ("DI", "Hilt: singleton, service and view-model components; repositories bound by interface"),
        ("Data", "Room (caretakers, incidents)   \u00b7   DataStore (SMS, auto-call, siren, sensitivity)"),
        ("Service", "FallDetectionService: foreground, wake lock, 50 Hz sensors, 100-sample buffer, stage-1 gate"),
        ("ML", "FallClassifier interface \u2192 mock heuristic (bound)  |  TFLite wrapper (stub, next commit)"),
    ]
    y = 1.62
    for title, detail in layers:
        rect(s, ML, y, 6.35, 0.66, fill=MIST, line=None)
        rect(s, ML, y, 0.05, 0.66, fill=TEAL, shape=MSO_SHAPE.RECTANGLE)
        text(s, ML + 0.20, y + 0.09, 1.05, 0.24, title.upper(), size=8.6, bold=True,
             color=TEAL, spc=1.0)
        text(s, ML + 1.30, y + 0.07, 4.95, 0.52, detail, size=9.6, color=INK,
             line_spacing=1.08)
        y += 0.74

    text(s, 7.15, 1.62, 5.45, 0.24,
         "BUILD STATUS \u2014 WEIGHTED BY PLANNED EFFORT", size=9, bold=True, color=MUTED, spc=1.0)
    text(s, 7.15, 1.86, 2.2, 0.60, "~70%", size=34, bold=True, color=GREEN,
         font=FONT_LIGHT)
    text(s, 9.05, 1.94, 3.55, 0.60,
         "of the planned engineering scope is complete at this review; the remainder is the "
         "escalation layer and field validation.",
         size=9.5, color=GREY, line_spacing=1.10)

    mods = [("Data validation and preprocessing", 100), ("Model training and evaluation", 100),
            ("TFLite export and parity", 100), ("Compose UI and navigation", 90),
            ("Room, DataStore, Hilt", 90), ("Foreground sensor service", 75),
            ("CNN inference inside the app", 25), ("SMS, GPS and incident logging", 10),
            ("Field testing and validation", 20)]
    yy = 2.62
    for name, pct in mods:
        text(s, 7.15, yy, 3.05, 0.22, name, size=9.4, color=INK)
        progress(s, 10.30, yy + 0.055, 1.55, pct, h=0.11,
                 color=GREEN if pct >= 90 else (ORANGE if pct >= 40 else RED))
        text(s, 11.95, yy, 0.65, 0.22, f"{pct}%", size=9, bold=True,
             color=GREY, align=PP_ALIGN.RIGHT)
        yy += 0.40

    text(s, ML, 6.10, CW, 0.70,
         "Weighting: data and models 35%, UI and persistence 20%, detection service 20%, escalation 20%, "
         "testing 5%. A debug build is available and the sensor-to-alert path currently runs on a "
         "heuristic classifier; wiring the exported CNN and the escalation path is the immediate next step.",
         size=9.6, italic=True, color=GREY, line_spacing=1.12)

    footer(s, 17)
    s.notes_slide.notes_text_frame.text = (
        "The app is a clean layered Android build: Compose UI, Hilt, Room, DataStore, and a "
        "foreground service that samples at 50 Hz behind a wake lock with the stage-1 gate. "
        "Around seventy percent of the planned engineering is done: all of the data and modelling "
        "work and most of the app shell. The honest gaps are the CNN binding - the mock classifier "
        "is what is currently bound - and the SMS, GPS and incident-logging path.")


# ------------------------------------------------------------------ 18 alert workflow
def slide_workflow(prs):
    s = new_slide(prs)
    header(s, 18, "Implementation", "The ten seconds that decide whether we call for help",
           "Verification is the feature that keeps a phone-only system trusted \u2014 and it is already built.")

    steps = [("T + 0", "Impact detected", "Stage 1 gate confirms free-fall then impact"),
             ("T + 0.3 s", "CNN confirms", "Window scored on device, no network"),
             ("T + 0.4 s", "Overlay + siren", "Full screen over the lock screen"),
             ("T + 10 s", "No response", "SMS to primary and secondary carers"),
             ("T + 11 s", "Auto-call", "Primary caretaker dialled (optional)"),
             ("T + 12 s", "Logged", "Incident stored with time and location")]
    x = ML
    w, gap = 1.85, 0.13
    for i, (t, title, detail) in enumerate(steps):
        fill = GREEN_SOFT if i < 3 else ORANGE_SOFT
        edge = GREEN if i < 3 else ORANGE
        rect(s, x, 1.72, w, 1.36, fill=fill, line=None)
        rect(s, x, 1.72, w, 0.05, fill=edge, shape=MSO_SHAPE.RECTANGLE)
        text(s, x + 0.14, 1.84, w - 0.24, 0.22, t, size=9.5, bold=True, color=edge)
        text(s, x + 0.14, 2.10, w - 0.22, 0.24, title, size=10.8, bold=True, color=INK)
        text(s, x + 0.14, 2.38, w - 0.22, 0.62, detail, size=8.6, color=GREY,
             line_spacing=1.06)
        if i < 5:
            arrow(s, x + w + 0.005, 2.32, 0.11, 0.16)
        x += w + gap

    text(s, ML, 3.28, 5.7, 0.24, "WHAT THE USER EXPERIENCES", size=9, bold=True,
         color=GREEN, spc=1.1)
    paragraphs(s, ML, 3.56, 5.60, 1.55, [
        P("Screen wakes with a full-width \u201cI\u2019m OK\u201d button, 80 dp tall, red on white.",
          bullet=True, size=10.2, sa=7),
        P("Siren and vibration start immediately; the countdown is visible and audible.",
          bullet=True, size=10.2, sa=7),
        P("A single tap cancels everything and records the event as a false alarm.",
          bullet=True, size=10.2, sa=7),
    ])
    text(s, 6.78, 3.28, 5.7, 0.24, "WHAT THE CAREGIVER RECEIVES", size=9, bold=True,
         color=ORANGE, spc=1.1)
    paragraphs(s, 6.78, 3.56, 5.70, 1.55, [
        P("SMS: name, \u201cpossible fall detected\u201d, timestamp and a Google Maps link.",
          bullet=True, size=10.2, sa=7),
        P("Delivered over the carrier network \u2014 no internet, no app, no account needed.",
          bullet=True, size=10.2, sa=7),
        P("Optional automatic call so the caregiver hears the situation directly.",
          bullet=True, size=10.2, sa=7),
    ])

    text(s, ML, 5.24, 4.0, 0.24, "EDGE CASES HANDLED", size=9, bold=True,
         color=MUTED, spc=1.1)
    edge_cases = ["Locked screen", "No internet", "No SIM", "False alarm", "Repeated falls"]
    for i, label in enumerate(edge_cases):
        chip(s, ML + i * 2.36, 5.52, 2.24, 0.44, label, fill=MIST, color=INK, size=9.5)
    text(s, ML, 6.06, CW, 0.72,
         "Locked screen: showWhenLocked and full-screen intent. No internet: SMS still delivers. "
         "No SIM: siren plus local log. False alarm: cancel is recorded for accuracy review. "
         "Repeated falls: 5 s cooldown prevents duplicate alerts from one event.",
         size=9.8, color=GREY, line_spacing=1.14)

    footer(s, 18)
    s.notes_slide.notes_text_frame.text = (
        "This is the user-facing behaviour. The overlay takes over the screen, sounds the siren and "
        "shows a large cancel button for ten seconds. If the user does not respond, we send an SMS "
        "with a Maps link and optionally place a call. The escalation path deliberately uses SMS "
        "rather than a push notification so it works with no internet and no app on the caregiver's "
        "side. The edge cases in the bottom strip are the ones that decide whether the system is "
        "usable in practice.")


def build(prs):
    slide_model_unimib(prs)
    slide_protocol(prs)
    slide_results_sisfall(prs)
    slide_results_unimib(prs)
    slide_compare(prs)
    slide_limits(prs)
    slide_deploy(prs)
    slide_android(prs)
    slide_workflow(prs)
