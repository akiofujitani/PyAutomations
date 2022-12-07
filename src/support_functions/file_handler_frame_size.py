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
    angle = 0

    while len(shape_in_angle.keys()) < angle_count_convert:
        angle += 1
        for i in range(len(shape_xy_resized)):
            x_y_values_a = shape_xy_resized[i]
            values_b_number = i if len(shape_xy_resized) < i else 0
            x_y_values_b = shape_xy_resized[values_b_number + 1]
            angle_a = math.atan(x_y_values_a['y'] / x_y_values_a['x'])
            angle_b = math.atan(x_y_values_b['y'] / x_y_values_b['x'])
            angle_diff = abs(abs(angle_a) - abs(angle_b))
            if angle_diff < 1:
                x_y_values_b = shape_xy_resized[values_b_number + 2]
                angle_b = math.atan(x_y_values_b['y'] / x_y_values_b['x'])
                angle_diff = abs(abs(angle_a) - abs(angle_b))
            

