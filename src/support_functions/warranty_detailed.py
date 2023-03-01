import datetime, file_handler, data_communication, data_organizer, json_config, os, Production_Details, logging
import logger as log
from ntpath import join

logger = logging.getLogger('warranty_detailed')

'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''

def remove_from_dict(values_dict=dict, *args):
    updated_dict = []
    for value in values_dict:
        for arg in args:
            value.pop(arg.upper())
        updated_dict.append(value)
    return updated_dict


def warranty_add_quantity(warranty_list):
    updated_warranty_list = []
    for warranty in warranty_list:
        temp_values = warranty
        temp_values['QUANTITY'] = 2 if warranty['LADO DO OLHO'] == 'AMBOS' else 1
        updated_warranty_list.append(temp_values)
    return updated_warranty_list


if __name__ == '__main__':
    logger = logging.getLogger()
    log.logger_setup(logger)
    
        # volpe_back_to_main()
    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/config_volpe.json')
    except:
        logger.critical('Could not load config file')
        exit()

    # Load config

    logger.info('Load config')
    remove_fields = config['warranty_detailed']['remove_fields']
    path = file_handler.check_create_dir(os.path.normpath(config['warranty_detailed']['path']))
    path_done = file_handler.check_create_dir(os.path.normpath(config['warranty_detailed']['path_done']))
    path_export = [os.path.normpath(path) for path in config['warranty_detailed']['path_export']]
    extension = config['warranty_detailed']['extension']
    file_name_pattern = config['warranty_detailed']['file_name_pattern']
    sheets_name = config['warranty_detailed']['sheets_name']
    sheets_name_date = config['warranty_detailed']['sheets_name_date']
    sheets_date_pos = config['warranty_detailed']['sheets_date_pos']
    sheets_id = config['warranty_detailed']['sheets_id']
    filter_tags_list = config['warranty_detailed']['filter_tags']
    warranty_motives_list = config['warranty_detailed']['warranty_motives']
    warranty_job_fields = config['warranty_detailed']['warranty_job_fields']


    # Get last uploaded date

    try:
        sheets_date_plus_one = data_communication.get_last_date(sheets_name_date, sheets_date_pos, '01/01/2022', sheets_id=sheets_id) + datetime.timedelta(days=1)
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    except Exception as error:
        logger.critical(f'Error loading table {sheets_name_date}')
        quit()


    # Defining start and end date

    if not sheets_date_plus_one == datetime.datetime.now().date():
        try:
            file_date = None
            file_list = file_handler.file_list(path, extension)
            for file in file_list:
                file_date = file_handler.file_contents_last_date(file_handler.CSVtoList(join(path, file)), 'DT.PED GARANTIA')
                if sheets_date_plus_one > file_date:
                    file_handler.file_move_copy(path, path_done, file, False)
            if file_date == None or file_date > sheets_date_plus_one:
                start_date = sheets_date_plus_one
            else:
                start_date = data_organizer.define_start_date(sheets_date_plus_one, file_date)

            logger.info(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
            logger.info(datetime.datetime.strftime(end_date, '%d/%m/%Y'))
        except Exception as error:
            logger.critical(error)
            exit()

        # Data processing
        
        try:
            file_list = file_handler.file_list(path, extension)
            for file in file_list:
                partial_list = file_handler.CSVtoList(join(path, file))
                filtered_list = data_organizer.filter_by_values(partial_list, 'MOTIVO GARANTIA', *warranty_motives_list)
                updated_list = remove_from_dict(filtered_list, *remove_fields)
                sorted_list = warranty_add_quantity(sorted(updated_list, key=lambda value : value['DT.PED GARANTIA']))
                temp_list = []
                if len(filtered_list) > 0:
                    for field_name in warranty_job_fields:
                        temp_list = Production_Details.values_merger(path_export, sorted_list, field_name, *filter_tags_list)
                        logger.info(f'{field_name} filtering terminated')
                    plain_dict_list = data_organizer.dict_list_to_plain_dict(temp_list)
                    filled_dict_list = data_organizer.plain_dict_list_completer(plain_dict_list)
                    # filled_dict_list = data_organizer.convert_to_date(filled_dict_list, '%Y%m%d', '%d/%m/%Y', 'PEDIDO GARANTIA__ENTRYDATE', 'PEDIDO ORIGINAL__ENTRYDATE')
                    sheet = data_communication.transform_in_sheet_matrix(data_organizer.plain_dict_float_format(filled_dict_list))
                    data_communication.data_append_values(sheets_name , f'A:{data_organizer.num_to_col_letters(len(sheet[0]))}', sheet, sheets_id=sheets_id)
                    file_date = file_handler.file_contents_last_date(file_handler.CSVtoList(join(path, file)), 'DT.PED GARANTIA')
                    string_file_date = datetime.datetime.strftime(file_date, '%d/%m/%Y')
                    data_communication.data_update_values(sheets_name_date, sheets_date_pos, [[string_file_date]], sheets_id=sheets_id)
                    logger.info(f'{file} done')
                file_handler.file_move_copy(path, path_done, file, False)
            logger.info("Done")
        except Exception as error:
            logger.error(f'Error in data processing {error}')
