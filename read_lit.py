from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import re


def pdf_to_txt(pdf_file, password=None):  # txt_file
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
    return text
    # Write the text to a text file
    # with open(txt_file, 'w') as f:
    #     f.write(text)


def return_pages(text):
    starts = [m.start() for m in re.finditer('\x0c', text)]
    pages = []
    # print(starts)
    if starts[0] != 0:
        print(f'starts[0] = {starts[0]}')
        page = text[0:starts[0]]
        print(page, '\n\n\n\n')
        pages.append(page)
        for i in range(len(starts)-1):
            start = starts[i]
            end = starts[i+1]-1
            print(f'starts[i] at {start} and goes to {end}')
            page = text[start:end]
            print(page, '\n\n\n\n')
            pages.append(page)
    else:
        for i in range(len(starts)):
            page = text[starts[i]:starts[i+1]-1]
            pages.append(page)
    print(pages)
    return pages


def get_OIG_ref(text):
    map_ref = r"(?:m\.?a\.?p|M\.?A\.?P|map|Map|MAP|r\.?e\.?f|R\.?E\.?F|ref|Ref|REF)[\s,](\d{3,4}[, ]){2}"
    numbers = r"(\d{3,4}[, ]){2}"
    if re.search(map_ref, text):
        print('Map Ref is found')
    else:
        print('Map Ref is not found')
    if re.search(numbers, text):
        print('Numbers matching OIG pattern are found')
    else:
        print('Numbers matching OIG pattern are not found')


pdf_file = 'The_1974_excavation_of_Hayonim_terrace_Israel_A_br.pdf'
txt_file = 'The_1974_excavation_of_Hayonim_terrace_Israel_A_br.txt'
# pdf_file = 'Adler_2017_The Decline.pdf'
# txt_file = 'Adler_2017_The Decline.txt'
# pdf_file = 'ExcavationReportTombNo1.pdf'
# txt_file = 'ExcavationReportTombNo1.txt'
papers = ['The_1974_excavation_of_Hayonim_terrace_Israel_A_br.pdf', 'ExcavationReportTombNo1.pdf']
for paper in papers:
    print('\n', paper)
    text = pdf_to_txt(paper, password=None)
    # print(text[0:200])
    get_OIG_ref(text)
# pdf_to_txt(pdf_file, txt_file)
# with open(txt_file, 'r') as f:
#     text = f.read()
# print(text)
#
# pages = return_pages(text)
# print(len(pages))
# for page in pages:
#     print(pages, '\n\n\n\n')
#
# new_page = '\x0c'
# new_line = '\n'

# get_OIG_ref(text)
