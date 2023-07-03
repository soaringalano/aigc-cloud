import yaml

from task.task_config import *
from task.task_executor import *
import threading
from typing import Dict, List, Union
import json
import os

_user_task_suffix = ".usr"
_id_task_suffix = ".idx"


class TaskManager:
    def __init__(self,
                 task_file_prefix: str = None):
        # key:task id, value:task
        self.__all_tasks: Dict[str, Dict] = {}
        # key:user id, value:list of task id
        self.__user_tasks: Dict[str, List[str]] = {}
        self.task_file_prefix = task_file_prefix
        self.load_from_file(task_file_prefix)
        return

    def load_from_file(self,
                       task_file_prefix: str) -> None:
        if task_file_prefix is None:
            return

        # key : user_id, value : list of tasks that belong to the user
        uf: str = task_file_prefix + _user_task_suffix
        if os.path.isfile(uf):
            with open(uf, "r") as user_file:
                self.__user_tasks = yaml.load(user_file, yaml.FullLoader)

        # key : task_id, value : task object
        idxf: str = task_file_prefix + _id_task_suffix
        if os.path.isfile(idxf):
            with open(idxf, "r") as all_tasks_file:
                self.__all_tasks = yaml.load(all_tasks_file, yaml.FullLoader)

    def save_to_file(self,
                     task_file_prefix: str) -> None:
        # key : user_id, value : list of tasks that belong to the user
        jo = json.dumps(self.__user_tasks, indent=4)
        uf: str = task_file_prefix + _user_task_suffix
        mode = "w" if os.path.isfile(uf) else "a+"
        with open(uf, mode) as user_file:
            user_file.write(yaml.dump(self.__user_tasks))

        # key : task_id, value : task object
        jo = json.dumps(self.__all_tasks, indent=4)
        idxf: str = task_file_prefix + _id_task_suffix
        mode = "w" if os.path.isfile(idxf) else "a+"
        with open(idxf, mode) as all_tasks_file:
            all_tasks_file.write(yaml.dump(self.__all_tasks))

    def list_user_tasks(self, user_id: str) -> List[str]:
        if user_id in self.__user_tasks.keys():
            return self.__user_tasks[user_id]
        return []

    def get_task(self, task_id: str) -> Dict:
        if task_id in self.__all_tasks.keys():
            return self.__all_tasks[task_id]
        return []

    def add_task(self,
                 task_config: BasicTaskConfig,
                 task_result: str = None):
        task_id = task_config[BasicTaskConfig.task_id]
        user_id = task_config[BasicTaskConfig.user_id]
        task: Dict = {'task_id': task_id,
                      'user_id': user_id,
                      'task_config': task_config,
                      'task_result': task_result}
                      # 'task_result': yaml.load(task_result, yaml.FullLoader)}
        self.__all_tasks[task_id] = yaml.dump(task)
        if user_id in self.__user_tasks.keys():
            self.__user_tasks[user_id].append(task_id)
        else:
            self.__user_tasks[user_id] = [task_id]
        self.save_to_file(self.task_file_prefix)

    def remove_task(self,
                    user_id: str,
                    task_id: str):
        if user_id in self.__user_tasks.keys():
            if task_id in self.__user_tasks[user_id]:
                self.__user_tasks[user_id].remove(task_id)

        if task_id in self.__all_tasks.keys():
            self.__all_tasks.pop(task_id)
        self.save_to_file(self.task_file_prefix)

    def clear(self):
        self.__user_tasks.clear()
        self.__all_tasks.clear()

    def __del__(self):
        # self.save_to_file(self.task_file_prefix)
        self.__all_tasks = None
        self.__user_tasks = None
