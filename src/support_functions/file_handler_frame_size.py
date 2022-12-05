'''
Build file handler and frame resizer/rebuilder.
'''

import json_config, file_handler, math


def volpe_points_corrector(shape_data_points):
    if len(shape_data_points) == 359:
        temp_shape_data = shape_data_points
        last_point = round(shape_data_points[0] + shape_data_points[358] / 2)
        return temp_shape_data.append(last_point)
    return 


def shape_to_xy(shape_points):
    try:
        x_y_dict_list = []
        angle_unit = 360 / len(shape_points)
        angle_value = angle_unit
        for radius in shape_points:
            x_value = math.cos(math.radians(angle_value)) + radius
            y_value = math.sin(math.radians(angle_value)) + radius
            x_y_dict_list.append({'x' : x_value, 'y' : y_value})
            angle_value += angle_unit
    except Exception as error:
        print(f'Could not convert frame values duue {error}')
        raise error
    return x_y_dict_list


def xy_shape_size(x_y_dict_list):
    frame_size = {}
    frame_size['hor'] = abs(min([angle['x'] for angle in x_y_dict_list])) + abs(max([angle['x'] for angle in x_y_dict_list]))
    frame_size['ver'] = abs(min([angle['y'] for angle in x_y_dict_list])) + abs(max([angle['y'] for angle in x_y_dict_list]))
    return frame_size


def shape_xy_resize(x_y_dict_list, hbox, vbox):
    frame_size = xy_shape_size(x_y_dict_list)

    hbox = frame_size['hor'] if hbox == None else hbox
    vbox = frame_size['ver'] if vbox == None else vbox

    x_scale_factor = frame_size['hor'] - hbox * -1
    y_scale_factor = frame_size['ver'] - vbox * -1

    shape_xy_resized = []
    for x_y_value in x_y_dict_list:
        shape_xy_resized.append({'x' : x_y_value['x'] * x_scale_factor, 'y' : x_y_value['y'] * y_scale_factor})
    return shape_xy_resized


def radius_recalc(shape_xy_resized, angle_count_convert=360):
    shape_in_angle = {}
    angle_unit = 360 / len(shape_xy_resized)

    while len(shape_in_angle.keys()) < angle_count_convert:
        for i in range(len(shape_xy_resized)):
            angle_a = angle_unit * (i + 1)


