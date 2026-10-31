"""Build the SevaLink Presentation 2 deck."""

import os
import sys

from pptx import Presentation
from pptx.util import Inches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import slides_a  # noqa: E402
import slides_b  # noqa: E402
import slides_c  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "SevaLink_Presentation_2.pptx")


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slides_a.build(prs)
    slides_b.build(prs)
    slides_c.build(prs)

    prs.core_properties.title = "SevaLink - Final Major Project Presentation 2"
    prs.core_properties.author = "Bhumika Rajoria, Anshita Singh"
    prs.core_properties.subject = ("Smartphone-based fall detection and emergency alert "
                                   "system for senior citizens")
    prs.save(OUT)
    print(f"saved {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
