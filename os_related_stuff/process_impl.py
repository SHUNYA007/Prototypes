from enum import Enum
from typing import Optional


class PROCESS_STATE(Enum):
    NEW="NEW"
    READY="READY"
    RUNNING="RUNNING"
    WAITING="WAITING"
    TERMINATED="TERMINATED"

class SCHEDULE_INFO(Enum):
    PRIORITY = "PRIORITY"
    POINTER = "POINTER"

class ACCOUNTING_INFO(Enum):
    PROCESS_NUMBER = "PROCESS_NUMBER"
    ACCOUNT_NUMBER = "ACCOUNT_NUMBER"
    TIME_LIMIT = "TIME_LIMIT"
    TIME_USED = "TIME_USED"
    

class Process:
    def __init(self, name:str, duration:float, parent: Optional['Process'] = None,priority = None):
        self.name = name
        self.duration = duration
        self.state = PROCESS_STATE.NEW
        self.memory_limit_in_mb = 200
        self.open_files = None
        self.parent = parent
        self.tasks = []
        self.sceduling_info = { 
            SCHEDULE_INFO.PRIORITY : priority if priority is not None else 0,
            SCHEDULE_INFO.POINTER:None,
            }
        self.accounting_info = {
            ACCOUNTING_INFO.PROCESS_NUMBER : None,
            ACCOUNTING_INFO.ACCOUNT_NUMBER : None,
            ACCOUNTING_INFO.TIME_LIMIT : None,
            ACCOUNTING_INFO.TIME_USED : None,

        }

    def add_tasks(self,task:str):
        self.tasks.append(task)
    