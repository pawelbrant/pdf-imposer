from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.pdf import PageObject
import math, sys


'''
takes pdf file as input and genrates pdf with four pages from original
pdf per output page;
half of the pages are to be printed on one side of paper
other half on the other side;
'''
def manage_pages(input_path, output_path='new_pdf_document.pdf'):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_path)
    number_of_pages = pdf_reader.getNumPages()
    page = pdf_reader.getPage(0)
    dims_A6 = page.trimBox.getWidth(), page.trimBox.getHeight()
    dims_A4 = dims_A6[0] * 2, dims_A6[1] * 2
    offset = 8 - number_of_pages % 8

    page_list = []

    for i in range(0, math.ceil(number_of_pages/2), 4):
        newPage = PageObject.createBlankPage(None, dims_A4[0], dims_A4[1])

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

        newPage.mergeTranslatedPage(p1, 0, dims_A6[1])
        newPage.mergeTranslatedPage(p2, dims_A6[0], dims_A6[1])
        newPage.mergeRotatedTranslatedPage(p3, 180, dims_A6[0]/2, dims_A6[1]/2)
        newPage.mergeRotatedTranslatedPage(p4, 180, dims_A6[0], dims_A6[1]/2)
        pdf_writer.addPage(newPage)


        newPage = PageObject.createBlankPage(None, dims_A4[0], dims_A4[1])

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

        newPage.mergeTranslatedPage(p1, 0, dims_A6[1])
        newPage.mergeTranslatedPage(p2, dims_A6[0], dims_A6[1])
        newPage.mergeRotatedTranslatedPage(p3, 180, dims_A6[0]/2, dims_A6[1]/2)
        newPage.mergeRotatedTranslatedPage(p4, 180, dims_A6[0], dims_A6[1]/2)
        page_list.append(newPage)

    for page in page_list:
        pdf_writer.addPage(page)

    with open(output_path, 'wb') as output:
        pdf_writer.write(output)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        manage_pages(sys.argv[1], sys.argv[2])
    else:
        manage_pages(sys.argv[1])
