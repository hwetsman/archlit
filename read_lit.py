from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os


def pdf_to_txt(pdf_file, txt_file, password=None):
    # Open the PDF file
    with open(pdf_file, 'rb') as f:
        # Create resource manager
        rsrcmgr = PDFResourceManager()
        if password:
            rsrcmgr.add_password(password)
        # Set parameters for analysis.
        laparams = LAParams()
        # Create a StringIO object for text extraction
        outfp = StringIO()
        # Create a PDF page aggregator object.
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
        # Get text from StringIO
        text = outfp.getvalue()
    # close open handles
    device.close()
    outfp.close()
    # Write the text to a text file
    with open(txt_file, 'w') as f:
        f.write(text)


pdf_file = 'ExcavationReportTombNo1.pdf'
txt_file = 'ExcavationReportTombNo1.txt'
pdf_to_txt(pdf_file, txt_file)
with open(txt_file, 'r') as f:
    print(f.readlines())
