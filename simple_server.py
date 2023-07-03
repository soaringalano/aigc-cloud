import os

from cluster.clustermanager import (ClusterManager, ClusterNode, Cluster, NodeType, NodeState)
import flask
from task.task_executor import *
from task.task_manager import *

from flask import Flask, render_template, redirect, url_for, request


with open('user_config.yaml') as f:
    users = yaml.load(stream=f, Loader=yaml.FullLoader)


cloudservice = Flask(__name__)

cluster_node_0 = ClusterNode(cluster_id='docker_cluster_0',
                             node_type=NodeType.GENERAL_NODE,
                             node_port=80,
                             node_name='docker_cluster_0_node_1',
                             node_state=NodeState.AVAILABLE,
                             node_address='172.17.0.2',
                             node_uuid=10000,
                             gpu_count=1)

cluster_node_1 = ClusterNode(cluster_id='docker_cluster_0',
                             node_type=NodeType.GENERAL_NODE,
                             node_port=80,
                             node_name='docker_cluster_0_node_2',
                             node_state=NodeState.AVAILABLE,
                             node_address='172.17.0.3',
                             node_uuid=10001,
                             gpu_count=1)

docker_cluster_0 = Cluster(cluster_id='docker_cluster_0',
                         general_nodes={10000: cluster_node_0,
                                        10001: cluster_node_1},
                         cluster_name='docker_cluster_0')

docker_cluster_1 = Cluster(cluster_id='docker_cluster_1',
                         general_nodes={10001: cluster_node_1},
                         cluster_name='docker_cluster_1')

docker_cluster_2 = Cluster(cluster_id='docker_cluster_2',
                         general_nodes={10000: cluster_node_0},
                         cluster_name='docker_cluster_2')

os.environ['SOURCE_HOME'] = '/home/linmao/workspaces/python/soaringalano/cloudservice'
os.environ['SERVER_ADDR'] = '192.168.1.28'
os.environ['SERVER_PORT'] = '8088'

clusterMan = ClusterManager()

clusterMan.add_cluster(docker_cluster_0)
clusterMan.add_cluster(docker_cluster_1)
clusterMan.add_cluster(docker_cluster_2)

source_root = os.environ[SYSTEM_SOURCE_HOME]
taskMan = TaskManager(source_root + SYSTEM_SERVER_TASK_FILE_PREFIX)


@cloudservice.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            content = request.json()
        else:
            content = flask.json.loads(request.data)
        print(users['users'])
        username = content['username']
        password = content['password']
        if username in users['users'] and users['users'][username]['password'] == password:
            msg = "{'msg':'user credential is valid, you can continue.}"
        else:
            msg = "{'exception':'Invalid credentials, please try again.'}"
    else:
        msg = "{'exception':'Only accept POST request, please check your code'}"
    return msg, 200


@cloudservice.route('/newtask', methods=['POST'])
def execute_task():
    error = None
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        content = request.data
        print(f"===content %s ========json====" % content)
        if content_type == 'application/json':
            content = request.json
        else:
            content = flask.json.loads(request.data)

        task_id = content[BasicTaskConfig.task_id]
        user_id = content[BasicTaskConfig.user_id]

        # task_type = TaskType(_task_type)
        # if task_type not in TaskType:
        #     error = f"{'exception':'unknown task type %s, please check your selection'}" % _task_type;
        #     return error, 200

        config = BasicTaskConfig()
        config.set_params(content)

        code, res = execute_cluster_task(task_config=config, cluster_manager=clusterMan)
        print(code, res)
        taskMan.add_task(config, res)
        print(code, res)
        return json.dumps(res), 200
    else:
        return "{\"error msg\": \"only post request will be treated\"}", 400


@cloudservice.route('/listtask', methods=['POST'])
def execute_listtask():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        content = request.data
        print(f"===content %s ========json====" % content)
        if content_type == 'application/json':
            content = request.json
        else:
            content = flask.json.loads(request.data)

        user_id = content[BasicTaskConfig.user_id]
        task_ids = taskMan.list_user_tasks(user_id)
        if task_ids is None:
            return json.dump(
                    "{errmsg: \"No task for user %s, please check your input\"}" % user_id),\
                    200
        return json.dumps(task_ids), 200
    else:
        return "{\"error msg\": \"only post request will be treated\"}", 400


@cloudservice.route('/gettask', methods=['POST'])
def execute_gettask():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        content = request.data
        print(f"===content %s ========json====" % content)
        if content_type == 'application/json':
            content = request.json
        else:
            content = flask.json.loads(request.data)

        task_id = content[BasicTaskConfig.task_id]
        task = taskMan.get_task(task_id)
        if task is None:
            return json.dump(
                    "{errmsg: \"No such task with id %s, please check your input\"}" % task_id),\
                    200
        return json.dumps(task), 200
    else:
        return "{\"error msg\": \"only post request will be treated\"}", 400


@cloudservice.route('/taskstat', methods=['POST'])
def execute_status_task():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        content = request.data
        print(f"===content %s ========json====" % content)
        if content_type == 'application/json':
            content = request.json
        else:
            content = flask.json.loads(request.data)

        task_id = content[BasicTaskConfig.task_id]
        task = taskMan.get_task(task_id)
        if task is None:
            return json.dump(
                    "{errmsg: \"No such task with id %s, please check your input\"}" % task_id),\
                    200
        print(task)
        return json.dump(task), 200
    else:
        return "{\"error msg\": \"only post request will be treated\"}", 400


@cloudservice.route('/clusterstat', methods=['POST'])
def execute_status_cluster():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        content = request.data
        print(f"===content %s ========json====" % content)
        if content_type == 'application/json':
            content = request.json
        else:
            content = flask.json.loads(request.data)

        cluster_id = content[BasicTaskConfig.cluster_id]
        cluster = clusterMan.get_cluster(cluster_id=cluster_id)
        if cluster is None:
            return json.dump(
                    "{errmsg: \"No such cluster with id %s, please check your input\"}" % cluster_id),\
                    200
        usage = cluster.get_cluster_nodes_usage()
        return json.dumps(usage), 200
    else:
        return "{\"error msg\": \"only post request will be treated\"}", 400


if __name__ == "__main__":
    addr = os.environ['SERVER_ADDR']
    port = os.environ['SERVER_PORT']
    cloudservice.run(host=addr, port=int(port), debug=True)





