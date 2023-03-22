from task.task_executor import *
from cluster.clustermanager import *
from service.cloud_client import (select_local_executable_shell,
                                  execute_local_task,
                                  execute_cluster_diffuser_task,
                                  execute_node_stable_diffusion_train,
                                  execute_cluster_task,
                                  execute_cluster_stable_diffusion_task)
# from service.cloud_server import *
from utils.environment_const import *
import yaml
import os

os.environ["STABLE_DIFFUSION_HOME"] = "~/workspaces/python/github/stable-diffusion"


with open("test_stable_diffusion_config.yaml") as f:
    yaml_content = yaml.load(stream=f, Loader=yaml.FullLoader)

config = StableDiffusionTrainConfig(
    task_id=123141123,
    cluster_id="testcluster",
    task_type=TaskType.stable_diffusion,
    task_goal=TaskGoal.train,
    environment_variables={"STABLE_DIFFUSION_HOME":"~/workspaces/python/github/stable-diffusion",
                           "MASTER_ADDR":"'localhost'",
                           "MASTER_PORT": 80},
    train_data_dir=os.environ["STABLE_DIFFUSION_HOME"]+"/models",
    task_name="testtask",
    resume="",
    base="models/ldm/cin256/config.yaml",
    yaml_content=yaml_content
)

config[StableDiffusionTrainConfig.master_addr] = "'localhost'"
config[StableDiffusionTrainConfig.master_port] = 80
config[StableDiffusionTrainConfig.accelerator] = "ddp"
config[StableDiffusionTrainConfig.node_rank] = 0
config[StableDiffusionTrainConfig.gpu_count] = "0,1"
config[StableDiffusionTrainConfig.num_nodes] = 1

# shell = select_local_executable_shell(config=config)
# print(shell)

res = execute_local_task(task_config=config)


