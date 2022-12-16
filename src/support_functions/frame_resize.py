import file_handler, vca_handler, vca_handler_frame_size, json_config, os

def __resize_both_sides(trcfmt=dict, hbox=int, vbox=int) -> dict:
    resized_trcfrm = {}
    temp_trcfmt = {}
    for side, value in trcfmt.items():
        shape_resized = __frame_resize(value['R'], hbox[side], vbox[side])
        temp_trcfmt['R'] = shape_resized.values()
        temp_trcfmt['TRCFMT'] = ['1', str(len(shape_resized)), 'E', side, 'F']
        resized_trcfrm[side] = temp_trcfmt
        temp_trcfmt = {}
        if len(trcfmt) == 1:
            other_side = 'R' if side == 'R' else 'L'
            temp_trcfmt['R'] = vca_handler_frame_size.shape_mirror(shape_resized).values()
            temp_trcfmt['TRCFMT'] = ['1', len(shape_resized), 'E', other_side, 'F']
            resized_trcfrm[other_side] = temp_trcfmt      
    return resized_trcfrm


def __frame_resize(shape_data=list, vbox=int, hbox=int) -> list:
    shape_to_xy = vca_handler_frame_size.shape_to_xy(shape_data)
    shape_resized_xy = vca_handler_frame_size.shape_xy_resize(shape_to_xy, vbox, hbox)    
    shape_in_radius = vca_handler_frame_size.radius_recalc(shape_resized_xy)
    return shape_in_radius

os.path.join

if __name__ == '__main__':
    try:
        config = json_config.load_json_config('frame_resize.json')
    except Exception as error:
        print(f'Error loading configuration json file due \n{error}')

    path = os.path.normpath(config['path'])
    paht_done = os.path.normpath(config['path_done'])
    path_new = os.path.normpath(config['path_new_file'])

    vca_list = file_handler.file_list(path, config['extension'])
    for vca_file in vca_list:
        vca_data = file_handler.file_reader(os.path.join(path, vca_file))
        job_vca = vca_handler.VCA_to_dict(vca_data)
        trace_format_resized = __resize_both_sides(job_vca['TRCFMT'], job_vca['HBOX'], job_vca['VBOX'])
        job_vca['TRCFMT'] = trace_format_resized
        vca_contents_string = vca_handler.dict_do_VCA(job_vca)
        file_handler.file_move_copy(path, paht_done, vca_file, False)
        file_handler.file_writer(path_new, vca_file, vca_contents_string)
        print(f'Done {job_vca["JOB"]}\n')
        print(vca_contents_string)
        print('\n\n')

