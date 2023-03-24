from task.task_config import *
import threading
from typing import Dict, List, Union
import json


class Task:
    def __init__(self,
                 task_id:str=None):
        self.task_id = task_id


class TaskManager:
    def __init__(self):
        self.all_tasks = {}