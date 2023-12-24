import queue
from enum import Enum
from process_impl import Process
import multiprocessing
import time


tasks_list = [
["ls -l","echo 'Hello'"],
["touch newfile.txt","rm newfile.txt"],
["mkdir something","rmdir something"]
]
RUNNNING = False

disk = tasks_list #this list is acting like a disk
memory = [] # this list is acting like a memory

class SCHEDULER_TYPE(Enum):
    SHORT = "SHORT"
    LONG = "LONG"
    MID = "MID"


class Scheduler:
    def __init__(self,type:SCHEDULER_TYPE) -> None:
        self.type = type
        self.scheduler_queue = queue.Queue()
        self.duration = None
         

    def add_process(self,process:Process):
        self.scheduler_queue.put(process)

    def wait(self):
        time.sleep(self.duration)


class LongTermScheduler(Scheduler):
    def __init__(self) -> None:
        super().__init__(SCHEDULER_TYPE.LONG)
        super().duration = 10 # Long scheduler runs in every 10 seconds
        self.multiprocessing_limit  = 2 #only 2 processes will be processed at a time, yes it is a fucking dumb ass scheduler

    def get_all_process(self):
        for i in disk:
            super().add_process(i)
    def put_task_in_ready_queue(self):
        RUNNNING = True
        while(not super().scheduler_queue.empty()):
            memory.extend([ super().scheduler_queue.get() for i in range(self.multiprocessing_limit)])
            self.wait()
        RUNNNING = False
class ShortTermScheduler(Scheduler):
    def __init__(self) -> None:
        super().__init__(SCHEDULER_TYPE.SHORT)
        super().duration = 1 #long scheduler runs every 1 sec in real world it is way faster but who cares this is a demo idiot

    def allocate_resorces(self):
        print(f"Allocating resorces to")

        
    def get_process_from_ready_queue(self):
        while(RUNNNING):
            super().scheduler_queue.put(memory.pop() if len(memory)>0 else None)
            super.wait()
            exec()
            
    
    
    