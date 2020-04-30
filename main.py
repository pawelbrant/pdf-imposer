from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.pdf import PageObject
import math
import sys
import getopt


'''
takes pdf file as input and genrates pdf with four pages from original
pdf per output page;
half of the pages are to be printed on one side of paper
other half on the other side;
'''


def a6(input_path, output_path='new_pdf_document.pdf'):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_path)
    number_of_pages = pdf_reader.getNumPages()
    page = pdf_reader.getPage(0)
    dims_A6 = page.trimBox.getWidth(), page.trimBox.getHeight()
    dims_A4 = dims_A6[0] * 2, dims_A6[1] * 2
    offset = number_of_pages % 8
    if offset != 0:
        offset = 8 - offset

    page_list = []

    for i in range(0, math.ceil(number_of_pages/2), 4):
        new_page = PageObject.createBlankPage(None, dims_A4[0], dims_A4[1])

        p2 = pdf_reader.getPage(i)
        p4 = pdf_reader.getPage(i+3)
        try:
            p1 = pdf_reader.getPage(number_of_pages-1-i+offset)
        except IndexError:
            p1 = PageObject.createBlankPage(None, dims_A6[0], dims_A6[1])
        try:
            p3 = pdf_reader.getPage(number_of_pages-4-i+offset)
        except IndexError:
            p3 = PageObject.createBlankPage(None, dims_A6[0], dims_A6[1])

        new_page.mergeTranslatedPage(p1, 0, dims_A6[1])
        new_page.mergeTranslatedPage(p2, dims_A6[0], dims_A6[1])
        new_page.mergeRotatedTranslatedPage(p3, 180, dims_A6[0]/2, dims_A6[1]/2)
        new_page.mergeRotatedTranslatedPage(p4, 180, dims_A6[0], dims_A6[1]/2)
        pdf_writer.addPage(new_page)

        new_page = PageObject.createBlankPage(None, dims_A4[0], dims_A4[1])

        p1 = pdf_reader.getPage(i+1)
        p3 = pdf_reader.getPage(i+2)
        try:
            p2 = pdf_reader.getPage(number_of_pages-2-i+offset)
        except IndexError:
            p2 = PageObject.createBlankPage(None, dims_A6[0], dims_A6[1])
        try:
            p4 = pdf_reader.getPage(number_of_pages-3-i+offset)
        except IndexError:
            p4 = PageObject.createBlankPage(None, dims_A6[0], dims_A6[1])

        new_page.mergeTranslatedPage(p1, 0, dims_A6[1])
        new_page.mergeTranslatedPage(p2, dims_A6[0], dims_A6[1])
        new_page.mergeRotatedTranslatedPage(p3, 180, dims_A6[0]/2, dims_A6[1]/2)
        new_page.mergeRotatedTranslatedPage(p4, 180, dims_A6[0], dims_A6[1]/2)
        page_list.append(new_page)

    for page in page_list:
        pdf_writer.addPage(page)

    with open(output_path, 'wb') as output:
        pdf_writer.write(output)


def a5(input_path, output_path='new_pdf_document'):
    pdf_writer_A = PdfFileWriter()
    pdf_writer_B = PdfFileWriter()
    pdf_reader = PdfFileReader(input_path)
    number_of_pages = pdf_reader.getNumPages()
    page = pdf_reader.getPage(0)
    dims_A5 = page.trimBox.getWidth(), page.trimBox.getHeight()
    dims_A4 = dims_A5[0] * 2, dims_A5[1]
    offset = number_of_pages % 4
    if offset != 0:
        offset = 4 - offset
    print(offset)

    page_list_A = []
    page_list_B = []

    for i in range(0, math.ceil(number_of_pages/2), 2):
        new_page = PageObject.createBlankPage(None, dims_A4[0], dims_A4[1])
        
        p2 = pdf_reader.getPage(i)
        try:
            p1 = pdf_reader.getPage(number_of_pages-1-i+offset)
        except IndexError:
            p1 = PageObject.createBlankPage(None, dims_A5[0], dims_A5[1])

        new_page.mergeTranslatedPage(p1, 0, 0)
        new_page.mergeTranslatedPage(p2, dims_A5[0], 0)
        page_list_A.append(new_page)

        new_page = PageObject.createBlankPage(None, dims_A4[0], dims_A4[1])
        p1 = pdf_reader.getPage(i+1)
        try:
            p2 = pdf_reader.getPage(number_of_pages-2-i+offset)
        except IndexError:
            p2 = PageObject.createBlankPage(None, dims_A5[0], dims_A5[1])
        new_page.mergeTranslatedPage(p1, 0, 0)
        new_page.mergeTranslatedPage(p2, dims_A5[0], 0)
        page_list_B.append(new_page)

    for page in page_list_A:
        pdf_writer_A.addPage(page)

    for page in page_list_B:
        pdf_writer_B.addPage(page)
    
    with open(output_path + '_A.pdf', 'wb') as output:
        pdf_writer_A.write(output)
    with open(output_path + '_B.pdf', 'wb') as output:
        pdf_writer_B.write(output)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'o:s:', ['ofile=', 'size='])
    except getopt.GetoptError:
        print('main.py -s <A6/A5> -o <outputfile> <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-o', '--ofile'):
            output = arg
        elif opt in ('-s', '--size'):
            if arg in ('A5, A6'):
                size = arg
            else:
                sys.exit(2)

    if size == 'A5':
        a5(args[0])
    elif size == 'A6':
        a6(args[0])
