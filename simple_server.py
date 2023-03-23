import os

from cluster.clustermanager import (ClusterManager, ClusterNode, Cluster, NodeType, NodeState)
import flask
from task.task_executor import *

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

clusterMan = ClusterManager()

clusterMan.add_cluster(docker_cluster_0)
clusterMan.add_cluster(docker_cluster_1)
clusterMan.add_cluster(docker_cluster_2)


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


@cloudservice.route('/task', methods=['POST'])
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
        # if 'task_id' in content:
        #     _task_id = content['task_id']
        # if 'task_name' in content:
        #     _task_name = content['task_name']
        # if 'task_type' in content:
        #     _task_type = content['task_type']
        # if 'cluster_id' in content:
        #     _cluster_id = content['cluster_id']
        # if 'dataset_path' in content:
        #     _dataset_path = content['dataset_path']
        # if 'model_path' in content:
        #     _model_path = content['model_path']
        # if 'base' in content:
        #     _base = content['base']
        # if 'yaml_content' in content:
        #     _yaml_content = content['yaml_content']
        #
        # if _task_type is None or _task_name is None or _cluster_id is None or \
        #     _dataset_path is None or _model_path is None or _base is None:
        #     error = f"there are one or more error in the parameters, please check again"
        #
        # task_type = TaskType(_task_type)
        # if task_type not in TaskType:
        #     error = f"{'exception':'unknown task type %s, please check your selection'}" % _task_type;
        #     return error, 200

        config = BasicTaskConfig()
        config.set_params(content)

        res = execute_cluster_task(task_config=config, cluster_manager=clusterMan)
        print(res)
        return json.dumps(res), 200
    else:
        return "{\"error msg\": \"only post request can be responded\"}", 400



if __name__ == "__main__":
    addr = os.environ['SERVER_ADDR']
    port = os.environ['SERVER_PORT']
    cloudservice.run(host=addr, port=int(port), debug=True)





