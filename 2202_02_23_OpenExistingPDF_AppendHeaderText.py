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
import pandas as pd


doc_details = [[17,17],[18,18],[19,19],[],[20,38],
                [39,48],[49,51],[53,56],[57,58],[59,60],
                [61,61],[62,63],[64,64],[65,66],[],[67,67],[68,100]]
docdf = pd.DataFrame(doc_details,columns=['start','end'],
                     dtype='int')
docdf['Appendix'] = docdf.index+1
docdf.dropna(subset=['start','end'],inplace=True)
docdf['start'] = docdf['start'].astype('int')
docdf['end'] = docdf['end'].astype('int')
# read your existing PDF
file_loc = 'C:\\Users\\MMatam\\Downloads'
file_name = '2022_02_23_NIT_Jamshedpur_AsstProf_SubmittedApplication_AllDocumentsFIT'
existing_pdf = PdfFileReader(open(file_loc+"\\"+file_name+".pdf", "rb"))
output = PdfFileWriter()

## Total pages in the PDF
tp = existing_pdf.getNumPages()
# add the "watermark" (which is the new pdf) on the existing page
for i in range(1,tp+1):
    if i in docdf['start'].values:
        j  = docdf[docdf['start'].values==i].index[0]
        adx_pages = (docdf['end'].loc[j] - docdf['start'].loc[j])+1
        for k in range(0,adx_pages):
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont('Helvetica-Bold', 18)
            can.drawString(460,730, "Appendix-%d.%d"%(docdf['Appendix'].loc[j],k+1))
            can.save()
            #move to the beginning of the StringIO buffer
            packet.seek(0)
            # create a new PDF with Reportlab
            new_pdf = PdfFileReader(packet)
            # print(i+k-1)
            page = existing_pdf.getPage(i+k-1)
            page.mergePage(new_pdf.getPage(0)) #.mergePage(*text*.getPage(0))
            output.addPage(page)
    else:
        page = existing_pdf.getPage(i-1)
        output.addPage(page)
# finally, write "output" to a real file
outputStream = open(file_loc+"\\"+file_name+"Appedix2.pdf", "wb")
output.write(outputStream)
outputStream.close()
subprocess.Popen([file_loc+"\\"+file_name+"Appedix2.pdf"], shell=True)