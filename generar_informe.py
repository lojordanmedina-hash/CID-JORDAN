from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generar_informe(nombre, mbti, impedimento, referencias):
    os.makedirs("informes", exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"informes/{nombre}_{fecha}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)

    text = c.beginText(40, 800)
    text.setFont("Helvetica", 12)

    text.textLine("INFORME DE EVALUACIÓN DEL CANDIDATO")
    text.textLine("")
    text.textLine(f"Nombre del candidato: {nombre}")
    text.textLine(f"Tipo de personalidad (MBTI): {mbti}")
    text.textLine(f"Impedimento legal: {'Sí' if impedimento else 'No'}")
    text.textLine(f"Referencias laborales verificadas: {'Sí' if referencias else 'No'}")

    c.drawText(text)
    c.showPage()
    c.save()

    return filename
