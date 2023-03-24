from task.task_config import *
from task.task_executor import *
import threading
from typing import Dict, List, Union
import json



class Task:
    def __init__(self,
                 task_id:str=None,
                 task_config:BasicTaskConfig=None,
                 task_result:TaskResult=None):
        self.task_id = task_id
        self.task_config = task_config
        self.task_result = task_result


class TaskManager:
    def __init__(self):
        self.all_tasks = {}