from task.task_config import *
from task.task_executor import *
import threading
from typing import Dict, List, Union
import json

user_task_suffix = ".usr"
id_task_suffix = ".idx"


class Task:
    def __init__(self,
                 user_id: str = None,
                 task_id: str = None,
                 task_config: BasicTaskConfig = None,
                 task_result: TaskResult = None):
        self.__user_id = user_id
        self.__task_id = task_id
        self.__task_config = task_config
        self.__task_result = task_result.to_dict()
        return

    def user_id(self) -> str:
        return self.__user_id

    def task_id(self) -> str:
        return self.__task_id

    def task_config(self) -> BasicTaskConfig:
        return self.__task_config

    def task_result(self) -> TaskResult:
        return self.__task_result

    def to_json(self) -> str:
        return json.dumps(
            {
                "user_id": self.__user_id,
                "task_id": self.__task_id,
                "task_config": self.__task_config,
                "task_result": self.__task_result
            }
        )


class TaskManager:
    def __init__(self,
                 task_file_prefix: str = None):
        # key:task id, value:task
        self.__all_tasks = {}
        # key:user id, value:list of task id
        self.__user_tasks = {}
        self.task_file_prefix = task_file_prefix
        self.load_from_file(task_file_prefix)
        return

    def load_from_file(self,
                       task_file_prefix: str) -> None:
        if task_file_prefix is None:
            return

        # key : user_id, value : list of tasks that belong to the user
        with open(task_file_prefix + user_task_suffix) as user_file:
            self.__user_tasks = json.load(user_file)

        # key : task_id, value : task object
        with open(task_file_prefix + id_task_suffix) as all_tasks_file:
            self.__all_tasks = json.load(all_tasks_file)

    def save_to_file(self,
                     task_file_prefix: str) -> None:
        # key : user_id, value : list of tasks that belong to the user
        with open(task_file_prefix + user_task_suffix, "w") as user_file:
            json.dumps(self.__user_tasks, user_file, indent=4)

        # key : task_id, value : task object
        with open(task_file_prefix + id_task_suffix, "w") as all_tasks_file:
            json.dumps(self.__all_tasks, all_tasks_file, indent=4)

    def add_task(self,
                 task_config: BasicTaskConfig,
                 task_result: TaskResult = None):
        task_id = task_config[BasicTaskConfig.task_id]
        user_id = task_config[BasicTaskConfig.user_id]
        task: Task = Task(task_id=task_id,
                          user_id=user_id,
                          task_config=task_config,
                          task_result=task_result)
        self.__all_tasks[task_id] = task
        if user_id in self.__user_tasks.keys():
            self.__user_tasks[user_id].append(task_id)
        else:
            self.__user_tasks[user_id] = [task_id]

    def __del__(self):
        self.save_to_file(self.task_file_prefix)
        self.__all_tasks = None
        self.__user_tasks = None
