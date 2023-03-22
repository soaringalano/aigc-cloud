import os
import json
import time
from flask import Flask, request
from io import StringIO
from subprocess import Popen
from task.task_executor import execute_local_task
from task.task_config import BasicTaskConfig


cloud_client = Flask(__name__)

current_proc: Popen = None

current_task: str = None


@cloud_client.route('/', methods=['POST', 'GET'])
def cloud_home():
    return "welcome to soaringalano_cloud home", 200


@cloud_client.route('/task', methods=['POST', 'GET'])
def execute_task(self) -> (str, int):
    print("executing local task for remote request")
    if request.data is None:
        return "no argument found", 400
    if request.method not in ['POST', 'GET']:
        error = "{'exception':'Only accept POST request, please check your code'}"
        return error, 400
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        content = request.json
    else:
        # content = flask.json.loads(request.data)
        content = request.data
    config = BasicTaskConfig()
    config.set_params(content)
    res = execute_local_task(config)
    self.current_proc = res.process()
    self.current_task = res.task_id()
    return res.to_json(), 200


@cloud_client.route('/stat', methods=['POST', 'GET'])
def check_state() -> (str, int):
    print("checking local task state for remote request")
    if request.data is None:
        return "no argument found", 400
    if request.method not in ['POST', 'GET']:
        error = "{'exception':'Only accept POST request, please check your code'}"
        return error, 400
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        content = request.json
    else:
        content = request.data
    task_id = content[BasicTaskConfig.task_id]
    period = int(content['period'])
    msg = {"task_id": task_id, "stdout": "", "stderr": ""}
    # stdout = self.current_proc.stdout
    # stderr = self.current_proc.stderr
    outbuf = None if current_proc.stdout is None else StringIO(current_proc.stdout)
    errbuf = None if current_proc.stderr is None else StringIO(current_proc.stderr)
    now = time.time()
    while round(1000*(time.time() - now)) <= period:
        if outbuf is not None:
            outbuf.readlines();
        if errbuf is not None:
            errbuf.readlines();
    msg['stdout'] = "std out is null" if outbuf is None else outbuf.getvalue()
    msg['stderr'] = "std err is null" if errbuf is None else errbuf.getvalue()
    return json.dumps(msg), 200


if __name__ == "__main__":
    address = os.environ['CLIENT_ADDR']
    port = os.environ['CLIENT_PORT']
    cloud_client.run(host=address, port=int(port), debug=True)
