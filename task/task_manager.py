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
        self.__task_id = task_id
        self.__task_config = task_config
        self.__task_result = task_result
        return

    def task_id(self) -> str:
        return self.__task_id

    def task_config(self) -> BasicTaskConfig:
        return self.__task_config

    def task_result(self) -> TaskResult:
        return self.__task_result


class TaskManager:
    def __init__(self,
                 saved_tasks_file:str):
        self.all_tasks = {}