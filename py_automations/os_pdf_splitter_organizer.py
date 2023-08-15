import os, pdf_splitting, pytesseract_image
from ntpath import join
from data_modules import file_handler
'''
List pdf files in folder
> loop through and split all pages
    > Save pages to temp directory
> List pdf pages splitted
    > loop through list reading each pdf file
    > rename based on contents read
    > move to final destination 
    if Error
        > Move without rename to error directory
> End

'''

def create_check_dir(path, dir_list):
    for dir_name in dir_list:
        file_handler.creatDir(path, dir_name)
    return


if __name__ == '__main__':

    # paths define
    root = os.path.dirname(__file__)
    source = join(root, 'pdf')
    splitted_destin = join(root, 'temp')
    done = join(root, 'done')
    error = join(root, 'error')

    # check create paths
    create_check_dir(root, ['pdf', 'temp', 'done', 'error'])

    # split pdf file into pages
    pdf_list = file_handler.fileList(source, 'pdf')
    for file in pdf_list:
        pdf_splitting.pdf_split(join(source, file), splitted_destin, 'OS')
    
    # create list of splitted pages
    pdf_pages_list = file_handler.fileList(splitted_destin, 'pdf')

    # list files, rename and move
    for pdf_file in pdf_pages_list:
        os_number = pytesseract_image.get_os_number(splitted_destin, pdf_file)
        if os_number.__eq__('Not found'):
            file_handler.fileMoveRename(splitted_destin, error, pdf_file, pdf_file)
        else:
            file_handler.fileMoveRename(splitted_destin, done, pdf_file, f'{os_number}.pdf')

