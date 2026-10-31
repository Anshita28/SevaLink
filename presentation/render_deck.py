import os, sys
import win32com.client

HERE = os.path.dirname(os.path.abspath(__file__))
pptx = os.path.join(HERE, "SevaLink_Presentation_2.pptx")
out = os.path.join(HERE, "_render_simple")
os.makedirs(out, exist_ok=True)

app = win32com.client.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(pptx, ReadOnly=True, WithWindow=False)
for i, slide in enumerate(pres.Slides, 1):
    slide.Export(os.path.join(out, f"Slide{i}.PNG"), "PNG", 1600, 900)
print("exported", len(pres.Slides), "slides")
pres.Close()
app.Quit()
