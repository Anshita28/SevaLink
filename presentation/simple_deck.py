"""SevaLink - simple 10-slide deck for Final Major Project Presentation 2.

Plain language, but slides 6 and 7 carry the real evaluation metrics.
"""

import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck_lib import (  # noqa: E402
    CW, GREY, GREEN, GREEN_SOFT, INK, LINE, MIST, ML, MUTED, ORANGE,
    ORANGE_SOFT, SW, TEAL, TEAL_DARK, TEAL_SOFT, WHITE,
    P, card, chip, footer, header, kpi, new_slide, paragraphs, rect,
    table, text,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "SevaLink_Presentation_2.pptx")

BODY = 15.5


def notes(slide, s):
    slide.notes_slide.notes_text_frame.text = s


# ------------------------------------------------------------------ 1 title
def s01(prs):
    s = new_slide(prs, bg=INK)
    rect(s, 0, 0, 0.30, 7.5, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)

    text(s, 1.15, 1.35, 8.0, 0.30, "FINAL MAJOR PROJECT  \u00b7  PRESENTATION 2",
         size=12, bold=True, color=ORANGE, spc=1.6)
    text(s, 1.10, 1.80, 9.4, 1.15, "SevaLink", size=66, bold=True,
         color=WHITE)
    text(s, 1.15, 3.02, 9.6, 0.85,
         "A phone app that notices a fall and calls for help",
         size=27, color=WHITE)

    rect(s, 1.15, 3.98, 3.0, 0.035, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)

    text(s, 1.15, 4.22, 8.6, 0.95,
         "Fall detection and emergency alerts for senior citizens,\n"
         "using the phone they already own.",
         size=16.5, color=MUTED, line_spacing=1.25)

    for i, (label, x) in enumerate(
            [("Fall detection", 1.15), ("15-second check", 3.72), ("Alert to family", 6.18)]):
        chip(s, x, 5.45, 2.30, 0.42, label, fill=TEAL, color=WHITE, size=11.5)

    text(s, 1.15, 6.30, 8.6, 0.28, "Team  \u00b7  Bhumika Rajoria  \u00b7  Anshita Singh",
         size=12, color=WHITE)
    text(s, 1.15, 6.60, 8.6, 0.28, "31 October 2026", size=11, color=MUTED)
    notes(s, "Start with one sentence: SevaLink is an Android app that uses the "
             "phone in a person's pocket to detect a fall and call the family if "
             "the person does not respond. Today we will show why we built it, "
             "how it works, what we measured, and what is left to finish. "
             "Keep this opening to about 40 seconds.")


# ---------------------------------------------------------------- 2 problem
def s02(prs):
    s = new_slide(prs)
    header(s, 2, "The problem", "Falls are common, and help often comes late",
           kicker="Why this project matters")
    footer(s, 2)

    paragraphs(s, ML, 1.80, 6.55, 4.30, [
        P([("Falls are the second biggest cause of accidental death in the "
            "world.", {})], size=BODY, bullet=True, sa=16),
        P([("Many happen at home, when the person is alone. It can be hours "
            "before anyone finds out.", {})], size=BODY, bullet=True, sa=16),
        P([("Wearable alarms work, but they cost money, need charging, and are "
            "easy to forget.", {})], size=BODY, bullet=True, sa=16),
        P([("Almost everyone already carries a phone.", {})], size=BODY,
          bold=True, bullet=True, sa=16),
        P([("That is the gap SevaLink fills: safety with no extra device and "
            "no monthly fee.", {})], size=BODY, color=TEAL, sa=0),
    ])

    card(s, 7.62, 1.80, 4.98, 2.62, fill=TEAL_SOFT, line=None)
    text(s, 7.95, 2.02, 4.35, 0.28, "OUR GOAL", size=10.5, bold=True, color=TEAL, spc=1.2)
    text(s, 7.95, 2.36, 4.35, 1.90,
         "Notice a fall within seconds, check with the person, and tell the "
         "family automatically \u2014 with the location.",
         size=18, color=INK, line_spacing=1.22)

    card(s, 7.62, 4.62, 4.98, 1.58, fill=WHITE)
    text(s, 7.95, 4.80, 4.35, 0.28, "IN ONE LINE", size=10.5, bold=True, color=ORANGE, spc=1.2)
    text(s, 7.95, 5.14, 4.35, 0.95,
         "\u201cA fall alarm that lives in the phone you already carry.\u201d",
         size=14.5, italic=True, color=INK, line_spacing=1.15)

    notes(s, "Explain the problem in human terms first: an elderly parent falls "
             "in the bathroom, cannot get up, and nobody knows for hours. Then "
             "the three existing options: a wearable button (cost, charging, "
             "forgetting it), a paid monitoring service, or nothing. The phone "
             "is the one device that is already there. Our goal is the sentence "
             "on the right.")


# ------------------------------------------------------------------ 3 features
def s03(prs):
    s = new_slide(prs)
    header(s, 3, "What the app does", "Five jobs, all done automatically",
           kicker="No button to press, no extra device to wear")
    footer(s, 3)

    rows = [
        ("1", "Watches movement",
         "Reads the phone's motion sensors 50 times a second, quietly in the background."),
        ("2", "Spots a possible fall",
         "A small AI model scores the last two seconds of movement as fall or no fall."),
        ("3", "Asks \u201cAre you okay?\u201d",
         "A full-screen alert with a 15-second countdown. One tap cancels it."),
        ("4", "Alerts the family",
         "If nobody answers, the app contacts the main caretaker with the location."),
        ("5", "Keeps a record",
         "Every event is saved, so the user can review it or mark it as a false alarm."),
    ]
    y = 1.74
    for num, title, desc in rows:
        card(s, ML, y, CW, 0.90, fill=WHITE)
        chip(s, ML + 0.20, y + 0.22, 0.46, 0.46, num, fill=TEAL, color=WHITE, size=13)
        text(s, ML + 0.86, y + 0.26, 3.55, 0.30, title, size=15.5, bold=True, color=INK)
        text(s, ML + 4.45, y + 0.28, CW - 4.75, 0.62, desc, size=13.2, color=GREY,
             line_spacing=1.12)
        y += 0.99

    notes(s, "Walk through the five jobs in order; each one is one line. The key "
             "idea is the check: the app never sends an alarm silently. It asks "
             "first, so normal life (sitting down hard, dropping the phone) does "
             "not scare the family. The next slide shows what one fall looks "
             "like from the phone's point of view.")


# ------------------------------------------------------------------- 4 moment
def s04(prs):
    s = new_slide(prs)
    header(s, 4, "One fall, step by step", "About twenty seconds, from fall to family",
           kicker="The same sequence every time a fall is suspected")
    footer(s, 4)

    beats = [
        ("0 s", "The fall", "Readings jump far beyond walking, sitting or standing up."),
        ("2 s", "The model checks", "The last two seconds are scored: fall, or not a fall."),
        ("3 s", "The phone asks", "It vibrates and shows the alert: 15 seconds to say \u201cI am okay\u201d."),
        ("18 s", "No answer", "The countdown ends, so the app treats it as a real emergency."),
        ("19 s", "The family hears", "The main caretaker gets the alert, with a map link to the person."),
    ]

    # timeline rule
    rect(s, ML + 0.10, 2.62, CW - 0.20, 0.022, fill=LINE, shape=MSO_SHAPE.RECTANGLE)
    w = 2.22
    gap = 0.16
    x = ML
    for i, (t, title, desc) in enumerate(beats):
        col = ORANGE if i >= 3 else TEAL
        text(s, x, 1.80, w, 0.30, t, size=17, bold=True, color=col)
        rect(s, x + 0.02, 2.56, 0.14, 0.14, fill=col, shape=MSO_SHAPE.OVAL)
        text(s, x, 2.86, w, 0.36, title, size=14, bold=True, color=INK)
        text(s, x, 3.26, w - 0.06, 1.10, desc, size=11.3, color=GREY, line_spacing=1.16)
        x += w + gap

    card(s, ML, 4.62, 5.82, 1.28, fill=GREEN_SOFT, line=None)
    text(s, ML + 0.24, 4.74, 5.30, 0.28, "IF THEY TAP \u201cI AM OKAY\u201d",
         size=9.5, bold=True, color=GREEN, spc=1.0)
    text(s, ML + 0.24, 5.04, 5.30, 0.72,
         "Nothing is sent. The event is saved as a false alarm, and the "
         "sensors keep watching.", size=12.2, color=INK, line_spacing=1.15)

    card(s, ML + 6.03, 4.62, 5.86, 1.28, fill=ORANGE_SOFT, line=None)
    text(s, ML + 6.27, 4.74, 5.34, 0.28, "IF THEY DO NOT ANSWER",
         size=9.5, bold=True, color=ORANGE, spc=1.0)
    text(s, ML + 6.27, 5.04, 5.34, 0.72,
         "The caretaker is alerted with the time, the place, and the "
         "location of the fall.", size=12.2, color=INK, line_spacing=1.15)

    text(s, ML, 6.08, CW, 0.60,
         "The countdown is the part that keeps families calm: an accidental drop of the phone "
         "becomes a question, not a scare.",
         size=11.5, italic=True, color=MUTED, line_spacing=1.18)

    notes(s, "Tell this as one incident, out loud, in order. Zero seconds: the "
             "fall. Two seconds: the model looks at the movement and answers one "
             "question. Three seconds: the phone asks, loudly, with 15 seconds on "
             "the clock. Eighteen seconds: silence is treated as an emergency. "
             "Nineteen seconds: the family knows, with a location. The point of "
             "this slide is the two boxes at the bottom: a false alarm costs one "
             "tap, and a real fall is never silent.")


# -------------------------------------------------------------------- 5 data
def s05(prs):
    s = new_slide(prs)
    header(s, 5, "The data", "We learned from two public fall datasets",
           kicker="Real recordings from real volunteers, not synthetic data")
    footer(s, 5)

    rows = [
        ["Dataset", "Who took part", "What it contains", "Used for"],
        ["SisFall", "38 volunteers,\nyoung and elderly",
         "4,500 recordings of falls and daily activities.\nTwo sensors: accelerometer + gyroscope.",
         "The main test"],
        ["UniMiB SHAR", "30 volunteers",
         "11,771 short clips, phone in the pocket.\nAccelerometer only.",
         "The phone model"],
    ]
    table(s, ML, 1.78, CW, rows, [2.05, 2.70, 5.35, 1.79], fs=12.5, hfs=11,
          rh=0.92, bold_first=True)

    card(s, ML, 4.68, 5.80, 1.62, fill=GREEN_SOFT, line=None)
    text(s, ML + 0.24, 4.84, 5.35, 0.28, "HOW WE TESTED", size=9.8, bold=True, color=GREEN, spc=1.0)
    text(s, ML + 0.24, 5.14, 5.35, 1.05,
         "Some volunteers were kept out of training completely.\n"
         "The model was tested only on those people, so the\n"
         "results are not just memorised answers.",
         size=12.2, color=INK, line_spacing=1.20)

    card(s, ML + 6.00, 4.68, 5.89, 1.62, fill=WHITE)
    text(s, ML + 6.24, 4.84, 5.40, 0.28, "WHY TWO MODELS?", size=9.8, bold=True, color=TEAL, spc=1.0)
    text(s, ML + 6.24, 5.14, 5.40, 1.05,
         "SisFall is the harder, more realistic test.\n"
         "UniMiB matches how a phone is actually used,\n"
         "so that is the version we put in the app.",
         size=12.2, color=INK, line_spacing=1.20)

    notes(s, "Two datasets: SisFall is the well-known benchmark with young and "
             "elderly volunteers and two sensors; UniMiB is recorded with the "
             "phone in the pocket and only an accelerometer. The important point "
             "is the green box: we never tested on a person who was in the "
             "training set. Both models were trained on 24 and 21 volunteers "
             "respectively and tested on people they had never seen.")


# ------------------------------------------------------------- 6 results sisfall
def s06(prs):
    s = new_slide(prs)
    header(s, 6, "Results", "SisFall: the full set of measures",
           kicker="Tested on 7 volunteers the model had never seen")
    footer(s, 6)

    rows = [
        ["Measure", "Score", "What it means"],
        ["Accuracy", "99.63%", "Correct decisions, out of 20,574 moments"],
        ["Precision", "96.28%", "When it said \u201cfall\u201d, it was right"],
        ["Recall (sensitivity)", "90.65%", "Share of fall moments it caught"],
        ["Specificity", "99.89%", "Normal moments correctly left alone"],
        ["F1 score", "93.38%", "Balance of precision and recall"],
        ["PR-AUC", "98.33%", "Confidence across all decision thresholds"],
        ["ROC-AUC", "99.86%", "How well it separates falls from daily life"],
        ["Falls caught (events)", "90.33%", "271 of the 300 real fall trials"],
    ]
    table(s, ML, 1.74, 7.52, rows, [2.05, 1.02, 4.45], fs=11.2, hfs=10.2,
          rh=0.395, bold_first=True, align=[PP_ALIGN.LEFT, PP_ALIGN.CENTER,
                                            PP_ALIGN.LEFT])

    text(s, ML, 5.44, 7.52, 0.62,
         "Held-out set: 7 volunteers (4 young, 3 elderly) \u00b7 20,574 windows \u00b7 "
         "300 real fall trials \u00b7 decision threshold chosen on a separate "
         "validation group, then frozen.",
         size=10.2, italic=True, color=GREY, line_spacing=1.18)

    kpis = [
        ("90.7%", "of falls caught", "the number that matters most", GREEN),
        ("2.8", "false alarms per hour", "6 in 2.2 hours of daily activity", ORANGE),
        ("0.32 s", "to react", "from fall to decision", TEAL_DARK),
    ]
    y = 1.74
    for value, label, sub, col in kpis:
        kpi(s, ML + 7.80, y, 4.34, 1.30, value, label, sub, color=col, value_size=26)
        y += 1.42

    text(s, ML, 6.30, CW, 0.66,
         "Read honestly: the exact moment of each fall was marked automatically from the sensor "
         "data, so these are a first estimate from a strong baseline, not a medical-grade result.",
         size=9.8, italic=True, color=MUTED, line_spacing=1.16)

    notes(s, "Go down the table quickly, in plain words: accuracy 99.63 means almost "
             "every decision was right; precision 96.28 means when it said fall it "
             "was usually right; recall 90.65 means it caught about nine of every "
             "ten fall moments; specificity 99.89 means it almost never disturbed "
             "normal activity; F1 93.38 and PR-AUC 98.33 combine the two; ROC-AUC "
             "99.86 shows the two classes are well separated. At event level it "
             "caught 271 of 300 real falls, 90.33 percent, with 2.8 false alarms "
             "per hour and a third of a second to decide. If someone asks why "
             "precision is lower than accuracy, say it is the price of not missing "
             "falls: we tuned the threshold on validation data to favour catching "
             "them. Then read the note at the bottom yourself before it is asked.")


# -------------------------------------------------------------- 7 results unimib
def s07(prs):
    s = new_slide(prs)
    header(s, 7, "Results", "UniMiB: the light model chosen for the phone",
           kicker="Accelerometer only \u2014 no gyroscope needed")
    footer(s, 7)

    rows = [
        ["Measure", "Score", "What it means"],
        ["Accuracy", "97.82%", "Correct decisions, out of 1,975 clips"],
        ["Precision", "94.96%", "When it said \u201cfall\u201d, it was right"],
        ["Recall (sensitivity)", "98.42%", "Falls caught: 622 of 632"],
        ["Specificity", "97.54%", "Daily activities correctly left alone"],
        ["F1 score", "96.66%", "Balance of precision and recall"],
        ["PR-AUC", "99.04%", "Confidence across all decision thresholds"],
    ]
    table(s, ML, 1.74, 7.52, rows, [2.05, 1.02, 4.45], fs=11.8, hfs=10.2,
          rh=0.40, bold_first=True, align=[PP_ALIGN.LEFT, PP_ALIGN.CENTER,
                                           PP_ALIGN.LEFT])

    card(s, ML, 4.72, 7.52, 1.34, fill=WHITE)
    text(s, ML + 0.24, 4.85, 7.05, 0.28, "WHY THIS ONE GOES INTO THE APP",
         size=9.5, bold=True, color=TEAL, spc=1.0)
    paragraphs(s, ML + 0.24, 5.16, 3.40, 0.85, [
        P([("No gyroscope needed", {"b": True})], size=11.6, bullet=True, sa=5),
        P([("Only 68 KB, so it lives on the phone", {"b": True})], size=11.6, bullet=True, sa=0),
    ])
    paragraphs(s, ML + 3.90, 5.16, 3.40, 0.85, [
        P([("Trained on pocket data, like real use", {"b": True})], size=11.6, bullet=True, sa=5),
        P([("Same 2-second window the app records", {"b": True})], size=11.6, bullet=True, sa=0),
    ])

    kpis = [
        ("12,432", "learned parameters", "a very small network", TEAL),
        ("68 KB", "model file", "smaller than one photo", TEAL_DARK),
        ("5", "volunteers held out", "1,975 clips they never trained on", GREEN),
    ]
    y = 1.74
    for value, label, sub, col in kpis:
        kpi(s, ML + 7.80, y, 4.34, 1.30, value, label, sub, color=col, value_size=25)
        y += 1.42

    text(s, ML, 6.22, CW, 0.72,
         "Being fair: these clips are already cut around each event, so this test is easier than "
         "real life. SisFall is the harder test, and it is the one we quote first.",
         size=9.8, italic=True, color=MUTED, line_spacing=1.16)

    notes(s, "Same order as the previous slide: accuracy 97.82, precision 94.96, "
             "recall 98.42, specificity 97.54, F1 96.66, PR-AUC 99.04. Recall is "
             "slightly higher than precision here because the network was trained "
             "and selected on PR-AUC, which favours catching falls. Then the reason "
             "this is the model in the app, which is fit, not score: accelerometer "
             "only, 68 kilobytes, pocket data, the same two-second window. Say the "
             "caveat yourself: the clips are pre-cut, so the task is easier, which "
             "is why SisFall stays our main evidence.")


# ------------------------------------------------------------- 8 what is built
def s08(prs):
    s = new_slide(prs)
    header(s, 8, "Implementation", "What is working in the app today",
           kicker="A real Android app in Kotlin, not a mock-up")
    footer(s, 8)

    w = 2.853
    screens = [
        ("Dashboard", "Start / stop monitoring\nLive sensor readings\nClear status line"),
        ("Fall alert", "Full-screen warning\n15-second countdown\n\u201cI am okay\u201d cancels"),
        ("Caretakers", "Name, phone, relation\nOne main contact\nEdit or remove"),
        ("History & settings", "Every incident saved\nMark a false alarm\nAlert delay setting"),
    ]
    x = ML
    for title, body in screens:
        card(s, x, 1.72, w, 1.26, fill=WHITE)
        text(s, x + 0.18, 1.84, w - 0.32, 0.28, title, size=12.8, bold=True, color=INK)
        text(s, x + 0.18, 2.14, w - 0.30, 0.80, body, size=10.2, color=GREY,
             line_spacing=1.18)
        x += w + 0.16

    text(s, ML, 3.12, 6.0, 0.26, "UNDER THE HOOD", size=9.5, bold=True, color=TEAL, spc=1.2)
    parts = [
        ("Kotlin + Compose", "Four screens, one app, Material 3 design. All state held in ViewModels."),
        ("Background service", "Reads the accelerometer 50 times a second and keeps the last 2 seconds."),
        ("Room database", "Caretakers and every incident stored on the phone. No cloud account."),
        ("Model slot ready", "The classifier sits behind one interface, so the 68 KB file drops straight in."),
    ]
    x = ML
    for title, body in parts:
        card(s, x, 3.41, w, 1.24, fill=MIST, line=None)
        text(s, x + 0.18, 3.53, w - 0.32, 0.28, title, size=11.8, bold=True, color=TEAL_DARK)
        text(s, x + 0.18, 3.83, w - 0.30, 0.76, body, size=10.2, color=GREY,
             line_spacing=1.16)
        x += w + 0.16

    card(s, ML, 4.82, 5.82, 1.20, fill=GREEN_SOFT, line=None)
    text(s, ML + 0.24, 4.94, 5.30, 0.26, "BUILT AND RUNNING ON A PHONE",
         size=9.5, bold=True, color=GREEN, spc=1.0)
    text(s, ML + 0.24, 5.24, 5.34, 0.70,
         "Sensor service \u00b7 navigation \u00b7 alert screen \u00b7 caretaker records \u00b7 "
         "incident history \u00b7 settings", size=11.5, color=INK, line_spacing=1.14)

    card(s, ML + 6.03, 4.82, 5.86, 1.20, fill=ORANGE_SOFT, line=None)
    text(s, ML + 6.27, 4.94, 5.34, 0.26, "STILL BEING CONNECTED",
         size=9.5, bold=True, color=ORANGE, spc=1.0)
    text(s, ML + 6.27, 5.24, 5.38, 0.70,
         "Model inference \u00b7 SMS sending \u00b7 live location in the alert \u00b7 "
         "opening the alert from the service", size=11.5, color=INK, line_spacing=1.14)

    text(s, ML, 6.12, CW, 0.44,
         "So the app, the screen and the database are real and tested by hand; the model plug-in and "
         "the messaging are the last two pieces, and today's numbers come from the model tested on its own.",
         size=10.2, color=GREY, line_spacing=1.16)

    text(s, ML, 6.66, CW, 0.26,
         "Android 8.0 and above  \u00b7  Kotlin  \u00b7  Jetpack Compose  \u00b7  Room  \u00b7  "
         "foreground service  \u00b7  works offline",
         size=9.5, color=MUTED)

    notes(s, "Be straightforward: this is a working app, not a mock-up. Name the "
             "four screens and what each one does. Then the four moving parts: the "
             "Kotlin and Compose front end, the background service that samples the "
             "accelerometer fifty times a second and keeps a two-second buffer, the "
             "Room database that stores caretakers and incidents locally, and the "
             "classifier interface that the model file plugs into. Then say the "
             "honest part before anyone asks: model inference, SMS and the live "
             "location are still being connected, so today's numbers come from the "
             "model evaluated separately. Examiners reward that clarity far more "
             "than an overclaim.")


# --------------------------------------------------------- 9 cost, scale, safety
def s09(prs):
    s = new_slide(prs)
    header(s, 9, "Cost, scale and safety", "Cheap to run, easy to grow, careful with people",
           kicker="A short look beyond the code")
    footer(s, 9)

    cols = [
        ("WHAT IT COSTS", TEAL, [
            "The app itself is free.",
            "One SMS costs about \u20b90.15\u20130.25.",
            "No server to rent: detection runs on the phone.",
            "Works on a \u20b98,000\u201310,000 Android phone.",
        ], "In short: the cost is a few SMS per user, not a subscription."),
        ("CAN IT GROW?", GREEN, [
            "Runs on any Android phone, version 8.0 and above.",
            "One small model file serves every user.",
            "Adding a new user costs nothing extra.",
            "Easy to add Hindi and other languages.",
        ], "In short: from one family to many, with no new infrastructure."),
        ("SAFETY & PRIVACY", ORANGE, [
            "The user can always cancel before an alert.",
            "Location is shared only during a real alert.",
            "Contacts are added with their knowledge.",
            "Sensor data stays on the phone.",
        ], "In short: help, without watching anyone."),
    ]
    x = ML
    w = 3.83
    for title, col, items, footer_line in cols:
        card(s, x, 1.80, w, 3.72, fill=WHITE)
        rect(s, x, 1.80, w, 0.055, fill=col, shape=MSO_SHAPE.RECTANGLE)
        text(s, x + 0.22, 2.00, w - 0.40, 0.30, title, size=10, bold=True, color=col, spc=1.0)
        paragraphs(s, x + 0.22, 2.42, w - 0.42, 2.15,
                   [P([(i, {})], size=12.0, bullet=True, sa=13) for i in items])
        text(s, x + 0.22, 4.62, w - 0.42, 0.68, footer_line, size=10.2,
             italic=True, color=GREY, line_spacing=1.12)
        x += w + 0.22

    card(s, ML, 5.74, CW, 0.84, fill=MIST, line=None)
    text(s, ML + 0.26, 5.90, CW - 0.52, 0.58,
         "And one honest limit: SevaLink calls family, not an ambulance. It is an early warning, "
         "not a medical device, and it does not replace medical care.",
         size=11.6, color=INK, line_spacing=1.15)

    notes(s, "Keep this light and confident, about 45 seconds. Cost: the app is "
             "free, there is no server bill because everything runs on the phone, "
             "and the only real cost is a few rupees of SMS. Scale: one model file, "
             "any Android phone, zero cost per extra user, so it can move from a "
             "pilot with five families to a village without new infrastructure. "
             "Safety: the cancel step, location only on a real alert, consent from "
             "contacts, data staying on the device. End on the honest limit at the "
             "bottom \u2014 do not call it a medical device.")


# --------------------------------------------------------------------- 10 next
def s10(prs):
    s = new_slide(prs, bg=INK)
    rect(s, 0, 0, 0.30, 7.5, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)

    text(s, 1.05, 0.78, 8.0, 0.28, "10  \u00b7  WHAT'S NEXT", size=10.5, bold=True,
         color=ORANGE, spc=1.4)
    text(s, 1.00, 1.10, 10.6, 0.75, "Three steps to finish", size=34, bold=True,
         color=WHITE)

    steps = [
        ("1", "Connect the trained model", "Put the 68 KB model file into the app and run it live on a phone."),
        ("2", "Add SMS and location", "Send the alert and a map link when the countdown runs out."),
        ("3", "Test with real people", "A small trial with 3\u20135 volunteers, and record what happens."),
    ]
    y = 2.20
    for num, title, desc in steps:
        rect(s, 1.02, y, 6.55, 0.95, fill=TEAL_DARK, line=None, radius=0.10)
        chip(s, 1.22, y + 0.24, 0.46, 0.46, num, fill=ORANGE, color=WHITE, size=13)
        text(s, 1.88, y + 0.14, 5.45, 0.30, title, size=14.5, bold=True, color=WHITE)
        text(s, 1.88, y + 0.46, 5.45, 0.40, desc, size=11.0, color=MUTED, line_spacing=1.1)
        y += 1.08

    text(s, 8.35, 2.20, 4.35, 0.30, "THE ONE SENTENCE TO REMEMBER",
         size=9.5, bold=True, color=ORANGE, spc=1.2)
    text(s, 8.35, 2.58, 4.30, 2.05,
         "\u201cAn affordable fall alarm, using the phone people already carry.\u201d",
         size=18, italic=True, color=WHITE, line_spacing=1.28)

    rect(s, 1.02, 5.62, 11.55, 0.018, fill=TEAL_DARK, shape=MSO_SHAPE.RECTANGLE)
    text(s, 1.02, 5.82, 7.6, 0.45, "Thank you  \u00b7  questions welcome", size=20,
         bold=True, color=WHITE)
    text(s, 1.02, 6.42, 9.0, 0.30,
         "Bhumika Rajoria  \u00b7  Anshita Singh  \u00b7  31 October 2026",
         size=11, color=MUTED)

    notes(s, "Finish positively and concretely: three steps, all already under way, "
             "with the model connection being the immediate one. Then say the one "
             "sentence on the right and stop talking \u2014 do not add a summary "
             "slide. Invite questions. Likely questions and short answers: why two "
             "models (fit for real phones, SisFall as the harder benchmark); how "
             "many false alarms (about three per hour, each just a 15-second "
             "prompt); is it medical (no, it is an early warning); what is left "
             "(model wiring, SMS and location, a small trial).")


# ---------------------------------------------------------------------- build
def main():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(7.5)
    for fn in (s01, s02, s03, s04, s05, s06, s07, s08, s09, s10):
        fn(prs)

    prs.core_properties.title = "SevaLink - Final Major Project Presentation 2"
    prs.core_properties.author = "Bhumika Rajoria, Anshita Singh"
    prs.core_properties.subject = ("Smartphone-based fall detection and emergency "
                                   "alert system for senior citizens")
    prs.save(OUT)
    print(f"saved {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
