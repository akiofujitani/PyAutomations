from dataclasses import dataclass
from os.path import normpath, abspath

class Config:
    def __init__(self, sleep_time_in_sec=int, group_count=int, source_destin_extention=list):
        self.__sleep_time_in_sec = sleep_time_in_sec
        self.__group_count = group_count
        self.__source_destin_extention = source_destin_extention


    @property
    def sleep_time_in_sec(self):
        return self.__sleep_time_in_sec


    @property
    def group_count(self):
        return self.__group_count


    @property
    def source_destin_extention(self):
        return self.__source_destin_extention


class DirectoryGroup:
    def __init__(self, source_directory=str, destin_directory=str, file_extension=str, copy=bool):
        self.__source_directory = source_directory
        self.__destin_directory = destin_directory
        self.__file_extension = file_extension
        self.__copy = copy


    @property
    def source_directory(self):
        return self.__source_directory


    @property
    def destin_directory(self):
        return self.__destin_directory


    @property
    def file_extension(self):
        return self.__file_extension


    @property
    def copy(self):
        return self.__copy


@dataclass
class JobFilter:
    source: list
    extension: str
    sheets_id: str
    sheets_name: str
    sheets_range: str


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    

    @classmethod
    def check_type_insertion(cls, values_dict=dict):
        try:
            source = [normpath(abspath(value)) for value in values_dict['source']]
            extension = values_dict['extension']
            sheets_id = values_dict['sheets_id']
            sheets_name = values_dict['sheets_name']
            sheets_range = values_dict['sheets_range']
            return cls(source, extension, sheets_id, sheets_name, sheets_range)
        except Exception as error:
            raise error


