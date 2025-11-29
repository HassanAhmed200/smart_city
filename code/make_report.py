# make_report.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os, pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(BASE, "output")
CHARTS = os.path.join(OUT, "charts")
DOC = os.path.join(OUT, "smart_city_final_report.pdf")
styles = getSampleStyleSheet()
story = []
def add(text, style='Normal', space=12):
    story.append(Paragraph(text, styles[style] if style in styles else styles['Normal']))
    story.append(Spacer(1, space))

add("<b>Smart City – Real-Time Traffic & Pollution Analytics</b>", 'Title', 24)
add("Generated report for Cairo - simulated real-time streams.", space=18)
# Key findings placeholder
add("<b>Key Findings</b>", space=10)
add("• Real-time correlation between vehicle count and PM2.5 observed.", space=6)
add("• Top congested periods identified; see charts.", space=6)

# insert charts if exist
for fname in ['cars_count.png','pm25.png','cars_vs_pm25.png']:
    p = os.path.join(CHARTS, fname)
    if os.path.exists(p):
        story.append(Image(p, width=500, height=200))
        story.append(Spacer(1,12))

add("End of report.", space=12)
doc = SimpleDocTemplate(DOC, pagesize=A4)
doc.build(story)
print("Report saved to", DOC)
