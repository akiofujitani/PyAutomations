from time import sleep
import file_handler, json_config, datetime, logger
from dataclasses import dataclass
from os.path import normpath, abspath
from os.path import split as path_split

logger = logger.logger('file_mover_backup')

@dataclass
class Move_Settings:
    source: str
    destination: str
    extention: str
    days_from_today: int
    copy: bool 


@dataclass
class Default_Configuration:
    wait_time: int
    file_per_cicle: int
    month_name_list: list


    def min_to_seconds(self) -> int:
        return self.wait_time * 60


if __name__ == '__main__':
    try:
        config = json_config.load_json_config('file_mover_backup.json')
        default_config = Default_Configuration(int(config['wait_time_min']),
                    int(config['files_per_cicle']),
                    config['month_name'])
    except Exception as error:
        logger.critical('Error loading configuration file.')
        sleep(3)
        quit()


    while True:
        for item in config['directory_list']:
            move_settings = Move_Settings(normpath(item['source']), 
                            normpath(item['destin']), 
                            item['extension'], 
                            int(item['days_from_today']), 
                            eval(item['copy']))
            try:
                file_list = file_handler.listFilesInDirSubDir(move_settings.source, move_settings.extention)
                if len(file_list) > 0:
                    counter = 0
                    for file in file_list:
                        file_last_modification = file_handler.fileCreationDate(file)
                        if datetime.datetime.today().date() - datetime.timedelta(days=move_settings.days_from_today) > file_last_modification:
                            file_destination = f'{move_settings.destination}/{file_last_modification.year}/{default_config.month_name_list[int(file_last_modification.month) - 1]}/{"{:02d}".format(file_last_modification.day)}'
                            file_destination_path = normpath(file_destination)
                            source_path, file_name = path_split(abspath(file))
                            file_handler.file_move_copy(source_path, file_destination_path, file_name, move_settings.copy, True)
                        counter += 1
                        if counter >= default_config.file_per_cicle:
                            logger.info(f'Number {default_config.file_per_cicle} of files per cicle reached.')
                            break
            except Exception as error:
                logger.error(f'Error processing files {error}')
        logger.info(f'Waiting ... {default_config.min_to_seconds()}')
        sleep(default_config.min_to_seconds())
