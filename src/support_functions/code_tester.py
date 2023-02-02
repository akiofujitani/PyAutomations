# SuperFastPython.com
# example of stopping a custom thread class
from time import sleep
from threading import Thread
from threading import Event
import keyboard

# custom thread class
class CustomThread(Thread):
    # constructor
    def __init__(self, event):
        # call the parent constructor
        super(CustomThread, self).__init__()
        # store the event
        self.event = event
 
    # execute task
    def run(self):
        # execute a task in a loop
        count = 0
        while True:
            # block for a moment
            count += 1
            sleep(1)
            # check for stop
            if self.event.is_set():
                break
            # report a message
            print(f'Worker thread running...{count}')
        print('Worker closing down')
 
# create the event
event = Event()
# create a new thread
thread = CustomThread(event)
# start the new thread
thread.start()
# block for a while
sleep(3)
# stop the worker thread

keyboard.wait('esc')
print('Main stopping thread')
event.set()
thread.join()
# wait for the new thread to finish
