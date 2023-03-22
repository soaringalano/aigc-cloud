from utils.environment_const import *
from task.task_config import *
from task.task_executor import *
import os

os.environ["STABLE_DIFFUSION_HOME"] = "~/workspaces/python/github/stable-diffusion"

s = select_local_executable_shell(StableDiffusionGenerateConfig(task_id=1231412))
print(s)
