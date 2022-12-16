import file_handler, vca_handler, vca_handler_frame_size, json_config
from time import sleep
from tkinter import messagebox
from ntpath import join
from os.path import normpath


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
    return resized_trcfmt


if __name__ == '__main__':
    try:
        config = json_config.load_json_config('config.json')
    except Exception as error:
        messagebox.showerror('VCA Bot Volpe/Middleware', f'Error loading configuration json file due \n{error}')
        quit()


    path = normpath(config['path'])
    path_done = normpath(config['path_done'])
    path_new = normpath(config['path_new_file'])
    sleep_time = int(config['sleep_time'])


    try:
        while True:
            vca_list = file_handler.file_list(path, config['extension'])
            if len(vca_list) > 0:
                for vca_file in vca_list:
                    try:
                        vca_data = file_handler.file_reader(join(path, vca_file))
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

            if len(config['move_groups']) > 0:
                for move_group in config['move_groups']:
                    extension = normpath(move_group['source_destin_extention'])
                    source_directory = normpath(move_group['source_directory'])
                    destin_directory = normpath(move_group['destin_directory'])
                    file_copy = eval(move_group['copy'])
                    try:
                        file_list = file_handler.file_list(source_directory, extension)
                        if len(file_list) > 0:
                            for file in file_list:
                                file_handler.file_move_copy(source_directory, destin_directory, file, file_copy)
                                sleep(0.1)
                    except Exception as error:
                        print(f'Error processing files {error}')

            print(f'Waiting... {sleep_time} seconds')
            sleep(sleep_time)
    except Exception as error:
        messagebox.showerror('VCA Bot Volpe/Middleware', f'Error in routine execution\n{error}')
        quit()
