import os
import subprocess
import json
shell = "python main.py -t true -b models/ldm/cin256/config.yaml --accelerator=\"ddp\" --gpus=\"0,\" --logger=\"true\" --num_nodes=2";
from io import StringIO
# f = open("/home/linmao/workspaces/python/github/stable-diffusion/run_cmd.sh", "w")
# f.write(shell)
# f.close()

# res = subprocess.Popen(["chmod", "+x", "/home/linmao/workspaces/python/github/stable-diffusion/run_cmd.sh"])
from subprocess import Popen, PIPE
import sys

env = os.environ.copy()
env["MASTER_ADDR"] = "localhost"
env["MASTER_PORT"] = "80"
env["NODE_RANK"] = "0"

with Popen("run_cmd.sh",
                       env=env,
                       stderr=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       shell=True, cwd="/home/linmao/workspaces/python/github/stable-diffusion") as process:
    stdout, stderr = process.communicate()
    msg = {"stdout": "", "stderr": ""}
    i = 0
    while process.poll() is not None and i < 3:
        out = StringIO()
        out.write(str(stdout))
        err = StringIO()
        err.write(str(stderr))
        msg["stdout"].join(out.getvalue())
        msg["stderr"].join(err.getvalue())
        i += 1
    print(json.dumps(msg))
    # while process.poll() is not None:
    #     process.wait(1000)
