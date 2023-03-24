import os
from typing import Dict
import socket
import torch

GLOBAL_HOST_NAME = "hostname";
GLOBAL_HOST_ADDRESS = "hostaddress"
GLOBAL_GPU_COUNT = "gpucount"
GLOBAL_UUID = "uuid"

ENVKEY_SYSTEM_CLIENT_EXCHANGE_NAME = "CLIENT_EXCHANGE_NAME"
ENVKEY_SYSTEM_INVOKER_EXCHANGE_NAME = "INVOKER_EXCHANGE_NAME"
ENVKEY_SYSTEM_QUEUE_STDOUT = "QUEUE_STDOUT"
ENVKEY_SYSTEM_QUEUE_STDERR = "QUEUE_STDERR"
ENVKEY_SYSTEM_QUEUE_INVOKE = "QUEUE_INVOKE"
ENVKEY_SYSTEM_CONNECTION_STRING = "MONGODB_CONNECTION_STRING"
ENVKEY_SYSTEM_DATABASE_NAME = "DATABASE_NAME"
ENVKEY_SYSTEM_CLUSTER_COLLECTION = "CLUSTER_COLLECTION"

# please set home before starting the program
ENVKEY_STABLE_DIFFUSION_HOME = "STABLE_DIFFUSION_HOME"
ENVKEY_DIFFUSERS_HOME = "DIFFUSERS_HOME"


PARAMS_STABLE_DIFFUSION_HOST_ADDR = "host_address"
PARAMS_STABLE_DIFFUSION_HOST_PORT = "host_port"
PARAMS_STABLE_DIFFUSION_API_CMD = "api_cmd"


# PARAMS_STABLE_DIFFUSION_ACCELERATE = "accelerate"
ENVKEY_DDP_MASTER_ADDR = "master_addr"
ENVKEY_DDP_MASTER_PORT = "master_port"
ENVKEY_DDP_NODE_RANK = "node_rank"
# PARAMS_STABLE_DIFFUSION_MODEL_PATH = "base"
# PARAMS_STABLE_DIFFUSION_GPU_COUNT = "gpu_count"
# PARAMS_STABLE_DIFFUSION_NUM_NODES = "num_nodes"

SHELL_STABLE_DIFFUSION_TRAIN = \
    "export MASTER_ADDR=\"{master_addr}\"\nexport MASTER_PORT=\"{master_port}\"\n" \
    "export NODE_RANK=\"{node_rank}\"\npython -u main.py -t true " \
    "-b {base} --accelerator=\"{accelerator}\" --gpus=\"{gpu_count}\" " \
    "--logger=\"true\" --num_nodes=\"{num_nodes}\""
SHELL_STABLE_DIFFUSION_GENERATE = "python -u scripts/txt2img.py " \
                                  "--prompt \"{prompt}\" --outdir \"{outdir}\" --n_sample \"{n_sample}\" " \
                                  "--H \"{H}\" --W \"{W}\" --config \"{config}\" --ckpt \"{ckpt}\"\n" \
                                  ""
SHELL_DIFFUSERS_TRAIN = ""
SHELL_DIFFUSERS_GENERATE = ""
SHELL_DALLE_TRAIN = ""
SHELL_DALLE_GENERATE = ""
SHELL_CHATGPT_TRAIN = ""
SHELL_CHATGPT_GENERATE = ""
SHELL_TERMINATE_TASK = "kill -n {pid}}"

ENVKEY_LOCAL_ADDRESS = "IP"
ENVKEY_LOCAL_PORT = "PORT"
ENVKEY_LOCAL_GPU_COUNT = "GPU_COUNT"
ENVKEY_LOCAL_HOSTNAME = "HOSTNAME"
ENVKEY_LOCAL_UUID = "UUID"

ENVKEY_ACCELERATOR_DDP = "ddp"
ENVKEY_ACCELERATOR_GPU = "gpu"
ENVKEY_ACCELERATOR_TPU = "tpu"
ENVKEY_ACCELERATOR_AUTO = "auto"

SYSTEM_STABLE_DIFFUSION_PATH = "/home/soaringalano/source/stable-diffusion/"
SYSTEM_DIFFUSERS_PATH = "/home/soaringalano/source/diffusers/"


CLUSTER_RESTFUL_API_TEMPLATE = "http://{host_address}:{host_port}/task"

JSON_HEADERS = {'Content-type': 'application/json'}

def init_local_info(self) -> Dict:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(self.hostname)
    gpu_count = 0 if not torch.cuda.is_available() else torch.cuda.device_count()
    uuid = hash(self.ip)
    return {
        GLOBAL_HOST_NAME: hostname,
        GLOBAL_HOST_ADDRESS: ip,
        GLOBAL_UUID: uuid,
        GLOBAL_GPU_COUNT: gpu_count
    }


def set_environment(environment_variables: Dict) -> Dict:
    if environment_variables is not None:
        my_env = os.environ.copy()
        for key, value in environment_variables.keys(), environment_variables.values():
            my_env.environ[key] = value
        return my_env
    return None

