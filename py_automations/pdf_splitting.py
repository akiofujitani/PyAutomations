import logging
from data_modules import file_handler, log_builder
from ntpath import join
from PyPDF2 import PdfFileReader, PdfFileWriter


logger = logging.getLogger('pdf_splitting')


def pdf_split(file_path, destin_path, name_of_split):
    pdf = PdfFileReader(file_path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        file_name = file_handler.fileNameDefiner(destin_path, f'{name_of_split}_{page}', 'pdf')
        output = join(destin_path, f'{file_name}.pdf')
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
            logger.info(f'{file_name} done')
    return


if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)

    file_extention = 'pdf'
    path = "C:/Users/Calculo/OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA/Documentos/Development/Maintenance_Auto/pdf"

    pdf_list = file_handler.file_list(path, file_extention)


    for file in pdf_list:
        pdf_split(join(path, file), 'OS')