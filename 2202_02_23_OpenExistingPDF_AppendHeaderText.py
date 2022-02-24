# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 20:17:40 2022

@author: MMatam
"""

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import subprocess

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(500,750, "Appendix")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfFileReader(packet)
# read your existing PDF
file_loc = 'C:\\Users\\MMatam\\Downloads'
file_name = '2022_02_23_NIT_Jamshedpur_AsstProf_SubmittedApplication_AllDocumentsFIT'
existing_pdf = PdfFileReader(open(file_loc+"\\"+file_name+".pdf", "rb"))
output = PdfFileWriter()
## Total pages in the PDF
tp = existing_pdf.getNumPages()
# add the "watermark" (which is the new pdf) on the existing page
for i in range(0,tp):
    page = existing_pdf.getPage(i)
    page.mergePage(new_pdf.getPage(0)) #.mergePage(*text*.getPage(0))
    output.addPage(page)
# finally, write "output" to a real file
outputStream = open(file_loc+"\\"+file_name+"NEW.pdf", "wb")
output.write(outputStream)
outputStream.close()
subprocess.Popen([file_loc+"\\"+file_name+"NEW.pdf"], shell=True)