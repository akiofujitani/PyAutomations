import os, logging
from . import file_handler, vca_handler, vca_handler_frame_size, json_config, log_builder
from time import sleep

logger = logging.getLogger('frame_resize')


def __resize_both_sides(trcfmt=dict, hbox=int, vbox=int) -> dict:
    resized_trcfmt = {}
    temp_trcfmt = {}
    for side, value in trcfmt.items():
        shape_resized = vca_handler_frame_size.frame_resize(value['R'], hbox[side], vbox[side])
        temp_trcfmt['R'] = list(shape_resized.values())
        temp_trcfmt['TRCFMT'] = ['1', str(len(shape_resized)), 'E', side, 'F']
        resized_trcfmt[side] = temp_trcfmt
        temp_trcfmt = {}
        if len(trcfmt) == 1:
            other_side = 'R' if side == 'R' else 'L'
            temp_trcfmt['R'] = list(vca_handler_frame_size.shape_mirror(shape_resized).values())
            temp_trcfmt['TRCFMT'] = ['1', len(shape_resized), 'E', other_side, 'F']
            resized_trcfmt[other_side] = temp_trcfmt
        logger.debug(f'Side {side} done')
    logger.debug('Both sizes resized')     
    return resized_trcfmt


if __name__ == '__main__':
    logger = log_builder.logger(logging.getLogger())
    try:
        config = json_config.load_json_config('frame_resize.json')
    except Exception as error:
        print(f'Error loading configuration json file due \n{error}')
        quit()


    path = os.path.normpath(config['path'])
    path_done = os.path.normpath(config['path_done'])
    path_new = os.path.normpath(config['path_new_file'])
    sleep_time = int(config['sleep_time'])


    while True:
        vca_list = file_handler.file_list(path, config['extension'])
        if len(vca_list) > 0:
            for vca_file in vca_list:
                try:
                    vca_data = file_handler.file_reader(os.path.join(path, vca_file))
                    job_vca = vca_handler.VCA_to_dict(vca_data)
                    print(f'{job_vca["JOB"]}\n')
                    if 'TRCFMT' not in job_vca.keys() or not int(job_vca['TRCFMT']['R']['TRCFMT'][1]) == 400:
                        file_handler.file_move_copy(path, path_done, vca_file, True)
                        sleep(0.5)
                        file_handler.file_move_copy(path, path_new, vca_file, False)
                    else:
                        trace_format_resized = __resize_both_sides(job_vca['TRCFMT'], job_vca['HBOX'], job_vca['VBOX'])
                        job_vca['TRCFMT'] = trace_format_resized
                        vca_contents_string = vca_handler.dict_do_VCA(job_vca)
                        file_handler.file_move_copy(path, path_done, vca_file, False)
                        file_handler.file_writer(path_new, vca_file, vca_contents_string)
                        print(vca_contents_string)
                        print('\n\n')
                except Exception as error:
                    print(f'Error {error} in file {vca_file}')
        sleep(sleep_time)
        print(f'Waiting... {sleep_time}')
