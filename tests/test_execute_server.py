# from task.task_executor import *
# from cluster.clustermanager import *
# from service.cloud_client import (select_local_executable_shell,
#                                   execute_local_task,
#                                   execute_cluster_diffuser_task,
#                                   execute_node_stable_diffusion_train,
#                                   execute_cluster_task,
#                                   execute_cluster_stable_diffusion_task)
# # from service.cloud_server import *
# from utils.environment_const import *
# import yaml
# import os
#
# os.environ["STABLE_DIFFUSION_HOME"] = "~/workspaces/python/github/stable-diffusion"
#
#
# with open("test_stable_diffusion_config.yaml") as f:
#     yaml_content = yaml.load(stream=f, Loader=yaml.FullLoader)
#
# config = StableDiffusionTrainConfig(
#     task_id=123141123,
#     cluster_id="testcluster",
#     task_type=TaskType.STABLE_DIFFUSION,
#     task_goal=TaskGoal.TRAIN,
#     environment_variables={"STABLE_DIFFUSION_HOME":"~/workspaces/python/github/stable-diffusion",
#                            "MASTER_ADDR":"'localhost'",
#                            "MASTER_PORT": 80},
#     train_data_dir=os.environ["STABLE_DIFFUSION_HOME"]+"/models",
#     task_name="testtask",
#     resume="",
#     base="models/ldm/cin256/config.yaml",
#     yaml_content=yaml_content
# )
#
# config[StableDiffusionTrainConfig.master_addr] = "'localhost'"
# config[StableDiffusionTrainConfig.master_port] = 80
# config[StableDiffusionTrainConfig.accelerator] = "ddp"
# config[StableDiffusionTrainConfig.node_rank] = 0
# config[StableDiffusionTrainConfig.gpu_count] = "0,1"
# config[StableDiffusionTrainConfig.num_nodes] = 1
#
# # shell = select_local_executable_shell(config=config)
# # print(shell)
#
# res = execute_local_task(task_config=config)

#################################################################
import requests
import json


def execute_train():

    url = "http://192.168.1.26:8088/task"

    post_data = "{\"task_type\" : \"stable_diffusion\", \"task_id\" : \"testtask\"," \
                " \"task_goal\": \"train\", \"task_name\": \"testtask\"," \
                " \"cluster_id\": \"docker_cluster_1\", \"dataset_path\": \"runwayml/stable-diffusion-v1-5\"," \
                " \"model_path\": \"/home/ldm/models/\"," \
                " \"envvar\": {\"SOURCE_HOME\": \"/home/ldm/source/stable-diffusion/\"}," \
                " \"base\": \"/home/ldm/source/stable-diffusion/models/ldm/cin256/config.yaml\"," \
                " \"yaml_content\": \"{}\"}"
    print(post_data)
    print(json.loads(post_data))

    headers = {'Content-type': 'application/json'}
    response = requests.post(url=url, data=post_data, params=post_data, headers=headers)

    if response.ok:
        print("all done!")
        print(response.headers, response.content, response.text, response.json())
    else:
        print("error")
        print(response.content)


def execute_generate():

    url = "http://192.168.1.26:8088/newtask"

    post_data = "{\"task_type\" : \"stable_diffusion\", \"task_id\" : \"testtask\"," \
                " \"task_goal\": \"generate\", \"task_name\": \"testtask\", \"user_id\": \"linmao\"," \
                " \"cluster_id\": \"docker_cluster_1\", \"prompt\": \"An astronaut riding a horse on the moon\"," \
                " \"ckpt\": \"/home/ldm/models/ldm/v1/model.ckpt\"," \
                " \"outdir\": \"/home/ldm/source/stable-diffusion/output/\", " \
                " \"envvar\": {\"SOURCE_HOME\": \"/home/ldm/source/stable-diffusion/\"}," \
                " \"n_samples\": \"9\", \"H\": \"512\", \"W\": \"512\", " \
                " \"config\": \"/home/ldm/source/stable-diffusion/models/ldm/cin256/config.yaml\"," \
                " \"yaml_content\": \"{}\"}"
    print(post_data)
    print(json.loads(post_data))

    headers = {'Content-type': 'application/json'}
    response = requests.post(url=url, data=post_data, params=post_data, headers=headers)

    if response.ok:
        print("all done!")
        print(response.headers, response.content, response.text, response.json())
    else:
        print("error")
        print(response.content)


def execute_status():

    url = "http://192.168.1.26:8088/stat"

    post_data = "{\"task_type\" : \"stable_diffusion\", \"task_id\" : \"testtask\"," \
                " \"task_goal\": \"status\", \"task_name\": \"testtask\"," \
                " \"cluster_id\": \"docker_cluster_1\", \"dataset_path\": \"runwayml/stable-diffusion-v1-5\"," \
                " \"model_path\": \"/home/ldm/models/\"," \
                " \"envvar\": {\"SOURCE_HOME\": \"/home/ldm/source/stable-diffusion/\"}," \
                " \"base\": \"/home/ldm/source/stable-diffusion/models/ldm/cin256/config.yaml\"," \
                " \"yaml_content\": \"{}\"}"
    print(post_data)
    print(json.loads(post_data))

    headers = {'Content-type': 'application/json'}
    response = requests.post(url=url, data=post_data, params=post_data, headers=headers)

    if response.ok:
        print("all done!")
        print(response.headers, response.content, response.text, response.json())
    else:
        print("error")
        print(response.content)

def execute_login():
    url = "http://192.168.1.26:8088/login"
    post_data = "{\"username\":\"soaringalano_cx\", \"password\":\"123456\"}"
    response = requests.post(url=url, data=post_data)
    print(response.content, response.headers, response.status_code, response.text)


# execute_login()

# execute_train()

execute_generate()
