from ntpath import join
import data_communication, file_handler


def list_to_dict(values_list, *args):
    values_dict = []
    args_counter = 0
    temp_dict = {}
    for value in values_list:
        temp_dict[args[args_counter]] = value.replace('\n', '')
        args_counter = args_counter + 1
        if args_counter >= len(args):
            args_counter = 0
            values_dict.append(temp_dict)
            temp_dict = {}
    return values_dict




if __name__ == '__main__':
    path = r'C:\Users\Calculo\OneDrive - RENOVATE COM.DE MAT.E PROD OPTICOS LTDA\Documentos\Development\Metaview'
    extension = 'txt'

    txt_list = file_handler.file_list(path, extension)
    txt_contents = []
    for file in txt_list:
        txt_contents = txt_contents + file_handler.file_reader(join(path, file))
    

    values_dict = list_to_dict(txt_contents, 'ID', 'ENTIDADE', 'TIPO', 'DIAS_TESTE')
    base_matrix = data_communication.transform_in_sheet_matrix(values_dict)
    data_communication.data_append_values('LICENSE', 'A:D', base_matrix, '1NGvJLnhTIk3OwLCCdnCLTd25U95KZS_Vc3M2wc4MMnk')
    print('Done')

