from subprocess import Popen
from time import sleep
import schedule, datetime

'''
Execute script
'''




def __execute_python_file(file_path=str) -> None:
    try:
        print("\nStarting " + file_path)
        process = Popen("python " + file_path, shell=True)
        process.wait()
        sleep(2.0)
        return True
    except Exception as error:
        print(f'Error in {file_path} execution')
        raise(error)



def volpe_automation_executer(path_list=list) -> None:
    print('Starting volpe automation list')
    while True:
        done_list = []
        while not len(done_list) == len(path_list):
            for file_path in path_list:
                try:
                    if __execute_python_file(file_path):
                        done_list.append(file_path)
                except Exception as error:
                    print(f'Error: {error}')
        return


def print_test():
    print('test')
    return




if __name__ == '__main__':
    time_in_hours = 24
    start_time = '01:00'
    wait_time = 1600
    path_list = ['./src/support_functions/warranty.py', 
                './src/support_functions/heat_map.py', 
                './src/support_functions/Breakages_detailed.py',  
                './src/support_functions/rework.py',
                './src/support_functions/warranty_detailed.py']


    schedule.every(1).days.at(start_time).do(volpe_automation_executer, path_list=path_list) 
    while True:
        try:
            schedule.run_pending()
            print(datetime.datetime.now())
            print(f'Waiting {wait_time} s')
            sleep(wait_time)
        except Exception as error:
            print(f'Error {error}')
            quit()