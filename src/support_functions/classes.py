from collections import namedtuple

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


