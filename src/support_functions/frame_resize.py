import file_handler, vca_handler, vca_handler_frame_size, json_config





def frame_resize(shape_data=list, vbox=int, hbox=int) -> list:
    shape_to_xy = vca_handler_frame_size.shape_to_xy(shape_data)
    shape_resized_xy = vca_handler_frame_size.shape_xy_resize(shape_to_xy, vbox, hbox)    
    shape_in_radius = vca_handler_frame_size.radius_recalc(shape_resized_xy)
    return shape_in_radius



if __name__ == '__main__':
    try:
        config = json_config.load_json_config('frame_resize.json')
    except Exception as error:
        print(f'Error loading configuration json file due \n{error}')


    vca_list = file_handler.fileListFullPath(config['path'], config['extension'])
    for vca_file in vca_list:
        vca_data = file_handler.file_reader(vca_file)
        job_vca = vca_handler.VCA_to_dict(vca_data)
        test = frame_resize(job_vca['TRCFMT']['R']['R'], job_vca['HBOX']['R'], job_vca['VBOX']['R'])
        print(job_vca['JOB'])
        vca_handler_frame_size.draw_points(test)
        print('Done')
