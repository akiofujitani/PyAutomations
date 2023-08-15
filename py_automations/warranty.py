import pyautogui, keyboard, datetime, calendar, os, logging, threading
from data_modules import win_handler, erp_volpe_handler, file_handler, data_communication, data_organizer, json_config, log_builder
from ntpath import join
from time import sleep

logger = logging.getLogger('warranty')


'''
==================================================================================================================================

        Template        Template        Template        Template        Template        Template        Template        Template        

==================================================================================================================================
'''

template = '''
{
    "remove_fields" : [
        "Emp", 
        "Id.Cliente", 
        "N.Fiscal Garantia", 
        "Cobre Garantia", 
        "Dt. Recebimento", 
        "NF. Entrada", 
        "N.Fiscal Original"
        ],
    "path" : "C:/PyAutomations_Reports/Warranty",
    "path_done" : "C:/PyAutomations_Reports/Warranty_Detailed",
    "sheets_name" : "WARRANTY",
    "sheets_date_pos" : "D:D",
    "sheets_id" : "1kpZuId58YFUqHqNPftbkRYbz0AW39F5IDjNHuNFgcC8",
    "extension" : "txt",
    "file_name_pattern" : "WARRANTY_",
    "minimun_date" : "01/06/2022"
}

'''

'''
==================================================================================================================================

        Data Processing     Data Processing     Data Processing     Data Processing     Data Processing     Data Processing

==================================================================================================================================
'''


def add_months_to_date(date=datetime.datetime, num_of_months=int):
    for i in range(num_of_months):
        date = date + datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1])
    return date


def create_update_motive_list(breakage_list):
    print('Creating motive list')
    movite_list = []

    for breakage in breakage_list:
        if not breakage["MOTIVO RETRABALHO"] in [motive[0] for motive in movite_list]:
            movite_list.append([breakage['MOTIVO RETRABALHO'], breakage['SETOR']])
    return movite_list


def add_unique(main_list, sub_list, index_value):
    unique_list = []
    values_by_index = [value[0] for value in main_list]
    for item in sub_list:
        if item[index_value] not in values_by_index:
            unique_list.append(item)
    return unique_list


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


def warranty(event: threading.Event, config: dict):
    path = file_handler.check_create_dir(os.path.normpath(config['path']))
    path_done = file_handler.check_create_dir(os.path.normpath(config['path_done']))
    extension = config['extension']
    file_name_pattern = config['file_name_pattern']
    sheets_name = config['sheets_name']
    sheets_date_pos = config['sheets_date_pos']
    sheets_id = config['sheets_id']

    try:
        sheets_date_plus_one = data_communication.get_last_date(sheets_name, sheets_date_pos, config['minimun_date'], sheets_id)
        sheets_date_plus_one= sheets_date_plus_one + datetime.timedelta(days=1)
        end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    except Exception as error:
        logger.error(f'Error loading table {sheets_name} due {error}')
        return

    if event.is_set():
        return    

    # Defining start and end date
    if not sheets_date_plus_one == datetime.datetime.now().date():
        try:
            temp_list = []
            file_date = None
            file_list = file_handler.file_list(path, extension)
            if len(file_list) > 0:
                for file in file_list:
                    temp_list = temp_list + file_handler.CSVtoList(join(path, file))
                file_date = file_handler.file_contents_last_date(temp_list, 'DT.PED GARANTIA')
                if sheets_date_plus_one > file_date:
                    file_handler.file_move_copy(path, path_done, file, False)
            if file_date == None:
                start_date = sheets_date_plus_one
            else:
                start_date = data_organizer.define_start_date(sheets_date_plus_one, file_date)
            
            logger.info(datetime.datetime.strftime(start_date, '%d/%m/%Y'))
            logger.info(datetime.datetime.strftime(end_date, '%d/%m/%Y'))
        except Exception as error:
            logger.error(error)
            event.set()
            return
            
        # Report extraction automation

        if start_date < end_date:
            erp_volpe_handler.volpe_back_to_main()
            erp_volpe_handler.volpe_load_tab('Tab_Lab', 'Icon_Prod_Unit.png')
            erp_volpe_handler.volpe_open_window('Icon_Warranty_control.png', 'Title_Warranty_Control.png')

            report_date_end = start_date
            while report_date_end < end_date:
                if event.is_set():
                    logger.info('Event set')
                    return
                if end_date > add_months_to_date(start_date, 1):
                    report_start_date = start_date
                    report_date_end = datetime.datetime(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1]).date()
                    start_date = report_date_end + datetime.timedelta(days=1)
                else:
                    report_start_date = start_date
                    report_date_end = end_date
                
                if event.is_set():
                    logger.info('Event set')
                    return    
                # image search for reference position.
                try:
                    erp_volpe_handler.volpe_load_report(report_start_date, report_date_end, None,
                                            'Button_consult.png',
                                            'Date_from.png', 
                                            'Date_until.png', 
                                            'Volpe_Table_selected.png', 
                                            date_from_pos='Front',
                                            date_until_pos='Front', 
                                            load_report_path='Images/Warranty_Control', 
                                            reference_pos_image='Warranty_job.png')
                    erp_volpe_handler.volpe_save_report(f'{file_name_pattern}{datetime.datetime.strftime(report_start_date, "%Y%m%d")}', path)
                except Exception as error:
                    logger.error(error)
                if event.is_set():
                    logger.info('Event set')
                    return

        # Data processing
        try:
            file_list = file_handler.file_list(path, extension)
            if file_list:
                for file in file_list:
                    partial_list = file_handler.CSVtoList(join(path, file))
                    updated_list = remove_from_dict(partial_list, *config['remove_fields'])
                    sorted_list = warranty_add_quantity(sorted(updated_list, key=lambda value : datetime.datetime.strptime(value['DT.PED GARANTIA'], '%d/%m/%Y')))
                    sheet = data_communication.transform_in_sheet_matrix(sorted_list)
                    data_communication.data_append_values(sheets_name ,'A:M', sheet, sheets_id=sheets_id)
                    file_handler.file_move_copy(path, path_done, file, False)
                    logger.info(f'{file} done')
                    if event.is_set():
                        logger.info('Event set')
                        return               
                logger.info("Done")
        except Exception as error:
            logger.error(f'Error in data processing {error}')
            event.set()
            return


def main(event: threading.Event, config: dict) -> None:
    if event.is_set():
        return
    warranty(event, config)
    return


def quit_func():
    logger.info('Quit pressed')
    event.set()
    return

if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)
    
    try:
        config = json_config.load_json_config('C:/PyAutomations_Reports/warranty.json', template)
    except:
        logger.error('Could not load config file')
        exit()


    event = threading.Event()
    keyboard.add_hotkey('esc', quit_func)

    for _ in range(3):
        main(event, config)
        if event.is_set():
            break

    logger.info('Warranty Done')