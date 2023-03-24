import random
import subprocess
import requests
import yaml
import json
from task_config import (TaskType,
                         TaskGoal,
                         BasicTaskConfig,
                         TerminateTaskConfig,
                         DiffusersTrainConfig,
                         StableDiffusionTrainConfig,
                         StableDiffusionGenerateConfig
                         )
from cluster.clustermanager import (Cluster, ClusterNode, ClusterManager)
from utils.environment_const import *
from subprocess import Popen
from typing import Dict
from enum import Enum
import sys
from utils.public_cdn_utils import *


class TaskState(Enum):
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    TERMINATED = "TERMINATED"
    SLEEPING = "SLEEPING"
    KILLED = "KILLED"
    NOTEXIST = "NOTEXIST"
    NORESPONSE = "NORESPONSE"
    FAILED = "FAILED"


class TaskResult:
    state_msg: Dict[TaskState, str] = {
        TaskState.SUBMITTED: "The task {name} is submitted now. {additional_msg}",
        TaskState.RUNNING: "The task {name} is running now. {additional_msg}",
        TaskState.TERMINATED: "The task {name} has been terminated now. {additional_msg}",
        TaskState.SLEEPING: "The task {name} is sleeping now. {additional_msg}",
        TaskState.KILLED: "The task {name} has been killed now. {additional_msg}",
        TaskState.NOTEXIST: "The task {name} does not exist yet. {additional_msg}",
        TaskState.NORESPONSE: "The task {name} does not respond, {additional_msg}"
    }

    def __init__(self,
                 state: TaskState = TaskState.NOTEXIST,
                 process: Popen = None,
                 task_id=None,
                 additional_msg: str = None) -> None:
        self._state = state
        self._process = process
        self._task_id = task_id
        self._additional_msg = additional_msg
        return

    def task_id(self):
        return self._task_id

    def state(self) -> TaskState:
        if self._process is None:
            return TaskState.NOTEXIST
        state = self._process.poll()
        if state is None:
            return TaskState.RUNNING
        elif state == 0:
            return TaskState.TERMINATED
        elif state == 1:
            return TaskState.SLEEPING
        elif state == 2:
            return TaskState.NOTEXIST
        elif state == 5:
            return TaskState.KILLED

        return self._state

    def pid(self) -> int:
        if self._process is None:
            return -1
        return self._process.pid

    def process(self):
        return self._process

    def msg(self) -> str:
        if self._additional_msg is not None:
            return self._additional_msg
        return self.state_msg[self.state()].format(name=self._task_id, additional_msg="")

    def to_dict(self):
        d = {"task_id": self.task_id(),
             "task_state": self.state().value,
             "pid": self.pid(),
             "additional_msg": self.msg()}
        return d

    def to_yaml(self):
        return yaml.dump(self.to_dict())

    def to_json(self):
        return json.dumps(self.to_dict())


def execute_local_task(task_config: BasicTaskConfig = None) -> TaskResult:
    if task_config is None:
        return TaskResult(TaskState.NOTEXIST, task_id="invalid task id")
    envvar = task_config[BasicTaskConfig.environment_variables]
    local_executable_shell = select_local_executable_shell(task_config)
    with subprocess.Popen(args=local_executable_shell,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          env=envvar,
                          cwd=envvar["SOURCE_HOME"]) as proc:

        return TaskResult(TaskState.SUBMITTED,
                          proc,
                          task_config[BasicTaskConfig.task_id],
                          "{\"msg\":\"Task is planned to run, please check the status later.\"")


def execute_post_process(task_config: BasicTaskConfig = None) -> TaskResult:
    if task_config[BasicTaskConfig.task_goal] == TaskGoal.generate.value:
        return __execute_upload_cdn(task_config)


def __execute_upload_cdn(outdir:str, task_id:str):
    ok, succ_fail = store_dir_images_as_nft(outdir)
    if ok:
        success: List[NFT] = succ_fail['success']
        fail: List[str] = succ_fail['fail']




def select_local_executable_shell(config: BasicTaskConfig) -> str:
    execute_sh = None
    if config[BasicTaskConfig.task_type] == TaskType.stable_diffusion.value:
        if config[BasicTaskConfig.task_goal] == TaskGoal.train.value:

            master_addr = config[StableDiffusionTrainConfig.master_addr]
            master_port = config[StableDiffusionTrainConfig.master_port]
            node_rank = config[StableDiffusionTrainConfig.node_rank]
            base = config[StableDiffusionTrainConfig.base]
            gpu_count = config[StableDiffusionTrainConfig.gpu_count]
            num_nodes = config[StableDiffusionTrainConfig.num_nodes]
            accelerator = config[StableDiffusionTrainConfig.accelerator]
            execute_sh = SHELL_STABLE_DIFFUSION_TRAIN.format(master_addr=master_addr,
                                                             master_port=master_port,
                                                             node_rank=node_rank,
                                                             accelerator=accelerator,
                                                             base=base,
                                                             gpu_count=gpu_count,
                                                             num_nodes=num_nodes)

        elif config[StableDiffusionTrainConfig.task_goal] == TaskGoal.generate.value:
            prompt = config[StableDiffusionGenerateConfig.prompt]
            ckpt = config[StableDiffusionGenerateConfig.ckpt]
            outdir = config[StableDiffusionGenerateConfig.outdir]
            n_samples = config[StableDiffusionGenerateConfig.n_samples]
            H = config[StableDiffusionGenerateConfig.H]
            W = config[StableDiffusionGenerateConfig.W]
            config = config[StableDiffusionGenerateConfig.config]
            execute_sh = SHELL_STABLE_DIFFUSION_GENERATE.format(prompt=prompt,
                                                                outdir=outdir,
                                                                n_samples=n_samples,
                                                                H=H,
                                                                W=W,
                                                                config=config,
                                                                ckpt=ckpt)

        else:  # '''terminate task'''

            execute_sh = SHELL_TERMINATE_TASK.format(
                task_id=config[TerminateTaskConfig.task_id])

    elif config[BasicTaskConfig.task_type] == TaskType.diffusers.value:
        if config[BasicTaskConfig.task_goal] == TaskGoal.train.value:

            execute_sh = SHELL_DIFFUSERS_TRAIN

        elif config[BasicTaskConfig.task_goal] == TaskGoal.generate.value:

            execute_sh = SHELL_DIFFUSERS_GENERATE

        else:  # '''terminate task'''

            execute_sh = SHELL_TERMINATE_TASK

    return execute_sh


# we assume that all related environment variables have already been set, so we can execute the shell
def execute_cluster_task(task_config: BasicTaskConfig,
                         cluster_manager: ClusterManager) -> TaskResult:
    print("executing cluster task")
    if task_config is None: return TaskResult(additional_msg="Task config should not be null")
    cluster = cluster_manager.get_cluster(task_config[BasicTaskConfig.cluster_id])
    if cluster is None:
        return TaskResult(additional_msg=f"No such cluster : %s, please check" % task_config.cluster_id())
    res = "Cluster task execution failed."
    if task_config[BasicTaskConfig.task_type] == TaskType.stable_diffusion.value:
        res = execute_cluster_stable_diffusion_task(task_config, cluster)
    elif task_config[BasicTaskConfig.task_type] == TaskType.diffusers.value:
        res = execute_cluster_diffuser_task(task_config, cluster)
    return res


def execute_cluster_stable_diffusion_task(task_config: BasicTaskConfig,
                                          cluster: Cluster) -> (bool, str):
    print("executing cluster stable diffusion task")
    task_id = task_config[BasicTaskConfig.task_id]
    task_goal = task_config[BasicTaskConfig.task_goal]
    cluster_id = task_config[BasicTaskConfig.cluster_id]
    envvar = task_config[BasicTaskConfig.environment_variables]
    if cluster.cluster_size() == 0:  # if no available node exists
        return TaskResult(task_id=task_id,
                          state=TaskState.NOTEXIST,
                          process=None,
                          additional_msg=f"No available node to execute task %s on cluster %s"
                                         % (task_id, cluster_id))
    if cluster.cluster_size() == 1:  # if the cluster contains only one node
        print("executing cluster size 1 stable diffusion task")
        node = list(cluster.general_nodes().values())[0]
        print(task_goal)
        if task_goal == TaskGoal.train.value:
            # print("starts to execute stable diffusion train task")
            success, response = execute_node_stable_diffusion_train(rank=0,
                                                                    num_nodes=1,
                                                                    base=task_config[StableDiffusionTrainConfig.base],
                                                                    cluster_node=node,
                                                                    master_node=node,
                                                                    config=task_config,
                                                                    is_master=True)
            return success, response
        elif task_goal == TaskGoal.generate.value:
            success, response = execute_node_stable_diffusion_generate(task_config, node)
            return success, response

        elif task_goal == TaskGoal.suspend.value:
            pass
        elif task_goal == TaskGoal.terminate.value:
            pass
        elif task_goal == TaskGoal.status.value:
            pass
        else:
            pass
    else:  # if multi nodes exist
        print("executing cluster size > 1 stable diffusion task")
        rand = random.Random()
        nodes = list(cluster.general_nodes().values())
        rand_node: ClusterNode = rand.choice(seq=nodes)
        counter = 1
        for node in nodes:
            master = False
            if node.node_uuid() == rand_node.node_uuid():
                master = True
            else:
                counter += 1
            task_goal = task_config[BasicTaskConfig.task_goal]
            if task_goal == TaskGoal.train:
                success, response = execute_node_stable_diffusion_train(rank=0 if master else counter,
                                                                        num_nodes=len(nodes),
                                                                        base=task_config[
                                                                            StableDiffusionTrainConfig.base],
                                                                        cluster_node=node,
                                                                        master_node=rand_node,
                                                                        config=task_config,
                                                                        is_master=master)
                return success, response
            elif task_goal == TaskGoal.generate.value:  # break loop when finished since generate won't need parallel task
                success, response = execute_node_stable_diffusion_generate(task_config, node)

                return success, response
            elif task_goal == TaskGoal.suspend.value:
                pass
            elif task_goal == TaskGoal.terminate.value:
                pass
            else:
                pass
    return False, TaskResult(task_id=task_config[BasicTaskConfig.task_id],
                             state=TaskState.NOTEXIST,
                             process=None,
                             additional_msg="Task execution failed due to unknown cause").to_json()


def execute_node_stable_diffusion_train(rank: int,
                                        num_nodes: int,
                                        base: str,
                                        cluster_node: ClusterNode,
                                        master_node: ClusterNode,
                                        config: BasicTaskConfig,
                                        is_master: bool = False) -> (bool, str):
    print("executing node stable diffusion train task")
    host_address = cluster_node.node_address()
    host_port = cluster_node.node_port()
    accelerator = ENVKEY_ACCELERATOR_AUTO if rank < 0 else ENVKEY_ACCELERATOR_DDP
    if rank == -1 or is_master and master_node is not None:
        master_addr = master_node.node_address()
        master_port = master_node.node_port()
    else:
        master_addr = cluster_node.node_address()
        master_port = cluster_node.node_port()
    gpu_count = cluster_node.gpu_count()
    restful_url = CLUSTER_RESTFUL_API_TEMPLATE
    params = {
        StableDiffusionTrainConfig.master_addr: master_addr,
        StableDiffusionTrainConfig.master_port: master_port,
        StableDiffusionTrainConfig.base: base,
        StableDiffusionTrainConfig.node_rank: rank,
        StableDiffusionTrainConfig.gpu_count: gpu_count,
        StableDiffusionTrainConfig.num_nodes: num_nodes,
        StableDiffusionTrainConfig.accelerator: accelerator
    }
    for key in config.keys():
        params[key] = config[key]

    restful_url = restful_url.format(host_address=host_address,
                                     host_port=host_port)
    print(f"restful-url is %s" % restful_url)
    print(f"data is %s" % json.dumps(params))
    param_str = json.dumps(params)
    response = requests.post(restful_url,
                             data=param_str,
                             params=param_str,
                             headers=JSON_HEADERS)
    status_code = response.status_code
    content = response.content
    print(content)
    success = status_code == 200
    return success, "{\"content\": %s}" % content


def execute_node_stable_diffusion_generate(config: BasicTaskConfig,
                                           node: ClusterNode) -> (bool, str):
    print("executing cluster stable diffusion generate task")
    host_address = node.node_address()
    host_port = node.node_port()
    restful_url = CLUSTER_RESTFUL_API_TEMPLATE

    restful_url = restful_url.format(host_address=host_address,
                                     host_port=host_port)
    param_str = json.dumps(config)
    response = requests.post(restful_url,
                             params=param_str,
                             data=param_str,
                             headers=JSON_HEADERS)
    status_code = response.status_code
    content = response.content
    success = status_code == 200
    return success, "{\"content\": %s}" % content


def execute_cluster_diffuser_task(task_config: BasicTaskConfig,
                                  cluster: Cluster) -> TaskResult:
    return TaskResult(additional_msg="Task execution failed due to unknown cause")
