from time import sleep
from data_modules import file_handler, config_loader, classes


def load_config():
    count = config_loader.section_key_loader('LOOP', 'COUNT', 2)
    sleep_time = config_loader.section_key_loader('SLEEP', 'TIME_IN_SEC', 10)
    print(f'count: {count} sleep time: {sleep_time}')
    group_list = []
    for i in range(int(count)):
        range_count = i + 1
        source = config_loader.section_key_loader(f'GROUP_{range_count}', 'SOURCE')
        destin = config_loader.section_key_loader(f'GROUP_{range_count}', 'DESTIN')
        extension = config_loader.section_key_loader(f'GROUP_{range_count}', 'EXTENSION')
        copy_bool = config_loader.section_key_loader(f'GROUP_{range_count}', 'COPY', 0)
        group_list.append(classes.DirectoryGroup(source, destin, extension, bool(int(copy_bool))))
        print(f'GROUP_{range_count} \nsource: {source} \ndestin: {destin} \nextension: {extension} \ncopy {copy_bool}')
    return classes.Config(int(sleep_time), int(count), group_list)


if __name__ == '__main__':
    try:
        config = load_config()
    except Exception as error:
        print('Error loading configuration file.')
        sleep(3)
        quit()


    while True:
        for i in range(config.group_count):
            directory_group = config.source_destin_extention[i]
            try:
                file_list = file_handler.file_list(directory_group.source_directory, directory_group.file_extension)
                if len(file_list) > 0:
                    for file in file_list:
                        file_handler.file_move_copy(directory_group.source_directory, directory_group.destin_directory, file, directory_group.copy)
                        sleep(0.1)
            except Exception as error:
                print(f'Error processing files {error}')
        print(f'Wait {config.sleep_time_in_sec}')
        sleep(config.sleep_time_in_sec)
