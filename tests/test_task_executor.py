from ..task.task_executor import *
from ..task.task_config import *
import json
import requests
import yaml

def test_execute_local_generate():
    config = BasicTaskConfig()
    task_type = TaskType.stable_diffusion
    task_goal = TaskGoal.generate
    config[BasicTaskConfig.task_id] = "test_generate_task"
    config[BasicTaskConfig.cluster_id] = ""
    config[BasicTaskConfig.user_id] = "soaringalano_lm"
    config[StableDiffusionGenerateConfig.outdir] = "/home/ldm/source/stable-diffusion/output"
    config[StableDiffusionGenerateConfig.config] = "/home/ldm/source/stable-diffusion/models/ldm/cin256/config.yaml"
    config[StableDiffusionGenerateConfig.H] = 512
    config[StableDiffusionGenerateConfig.W] = 512
    config[StableDiffusionGenerateConfig.ckpt] = "/home/ldm/models/ldm/v1/model.ckpt"
    config[StableDiffusionGenerateConfig.n_sample] = 9
    config[StableDiffusionGenerateConfig.prompt] = "A horse rides an astronaut on Mars"

    execute_local_task(config)


if __name__ == "__main__":
    test_execute_local_generate()




