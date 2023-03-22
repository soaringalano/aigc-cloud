from cluster.clustermanager import NodeType, NodeState, Cluster, ClusterNode, ClusterManager
from utils.environment_const import *
import pika
from pika.exchange_type import ExchangeType
from pika import PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika import BlockingConnection
from service.consumer_callback import (BasicConsumerCallback,
                                       InvokeMethodConsumerCallback,
                                       DisplayStdOutConsumerCallback,
                                       DisplayStdErrConsumerCallback)

from flask import Flask, request
from task.task_executor import *
import time
from io import StringIO


# def init_client_info(self) -> Dict:
#     hostname = socket.gethostname()
#     ip = socket.gethostbyname(self.hostname)
#     gpu_count = 0 if not torch.cuda.is_available() else torch.cuda.device_count()
#     uuid = hash(self.ip)
#     return {
#         GLOBAL_HOST_NAME: hostname,
#         GLOBAL_HOST_ADDRESS: ip,
#         GLOBAL_UUID: uuid,
#         GLOBAL_GPU_COUNT: gpu_count
#     }


def _init_client_rabbitmq(credentials: PlainCredentials,
                          msg_center_ip: str,
                          msg_center_port: int,
                          cluster_id: str,
                          invoke_callback: BasicConsumerCallback) -> (BlockingChannel, BlockingConnection):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=msg_center_ip, port=msg_center_port, credentials=credentials))
    channel = connection.channel()

    client_exchange = os.environ[ENVKEY_SYSTEM_CLIENT_EXCHANGE_NAME]
    stdout = os.environ[ENVKEY_SYSTEM_QUEUE_STDOUT]
    stderr = os.environ[ENVKEY_SYSTEM_QUEUE_STDERR]
    invoke = os.environ[ENVKEY_SYSTEM_QUEUE_INVOKE]

    channel.exchange_declare(exchange=client_exchange, durable=True, exchange_type=ExchangeType.direct.name)

    channel.queue_declare(queue=stdout)
    channel.queue_bind(exchange=client_exchange, queue=stdout, routing_key=stdout)

    channel.queue_declare(queue=stderr)
    channel.queue_bind(exchange=client_exchange, queue=stderr, routing_key=stderr)

    if invoke_callback is not None:
        channel.basic_consume(queue=invoke,
                              on_message_callback=invoke_callback.on_message_callback,
                              auto_ack=False)

    return channel, connection


def _init_invoker_rabbitmq(credentials: PlainCredentials,
                           localhost_port: int,
                           stdout_callback: BasicConsumerCallback,
                           stderr_callback: BasicConsumerCallback) -> (BlockingChannel, BlockingConnection):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=localhost_port, credentials=credentials))
    channel = connection.channel()

    invoker_exchange = os.environ[ENVKEY_SYSTEM_INVOKER_EXCHANGE_NAME]
    stdout = os.environ[ENVKEY_SYSTEM_QUEUE_STDOUT]
    stderr = os.environ[ENVKEY_SYSTEM_QUEUE_STDERR]
    invoke = os.environ[ENVKEY_SYSTEM_QUEUE_INVOKE]

    channel.exchange_declare(exchange=invoker_exchange, durable=True, exchange_type=ExchangeType.direct.name)

    channel.queue_declare(queue=invoke)
    channel.queue_bind(exchange=invoker_exchange, queue=invoke, routing_key=invoke)

    if stdout_callback is not None:
        channel.basic_consume(queue=stdout,
                              on_message_callback=stdout_callback.on_message_callback,
                              auto_ack=False)

    if stderr_callback is not None:
        channel.basic_consume(queue=stderr,
                              on_message_callback=stderr_callback.on_message_callback,
                              auto_ack=False)

    return channel


class ClusterNodeClient:

    def __init__(self,
                 cluster_id: str,
                 node_type: NodeType,
                 credentials: PlainCredentials,
                 msg_center_ip: str,
                 msg_center_port: int = 5672,
                 active_process: Popen = None) -> None:
        self._process = active_process
        self._cluster_id = cluster_id
        self._node_type = node_type
        client_info = init_local_info()
        if node_type is NodeType.MSG_EXCHANGE_NODE:
            self._channel, self.connection = \
                _init_invoker_rabbitmq(credentials=credentials,
                                       localhost_port=msg_center_port,
                                       stdout_callback=DisplayStdOutConsumerCallback(),
                                       stderr_callback=DisplayStdErrConsumerCallback())
        else:
            self._channel, self.connection = \
                _init_client_rabbitmq(credentials=credentials,
                                      msg_center_ip=msg_center_ip,
                                      msg_center_port=msg_center_port,
                                      cluster_id=cluster_id,
                                      invoke_callback=InvokeMethodConsumerCallback())

        self._cluster_node = ClusterNode(
            node_name=client_info[GLOBAL_HOST_NAME] + "@" + client_info[GLOBAL_HOST_ADDRESS],
            node_uuid=client_info[GLOBAL_UUID],
            node_type=node_type,
            node_state=NodeState.AVAILABLE,
            node_address=client_info[GLOBAL_HOST_ADDRESS],
            gpu_count=client_info[GLOBAL_GPU_COUNT],
            cluster_id=cluster_id)

        return

    def cluster_node(self) -> ClusterNode:
        return self._cluster_node

    def run_task(self, params: Dict):
        config = BasicTaskConfig()
        config.set_params(params)
        res = execute_local_task(task_config=config)
        return res.to_json()

    def set_active_process(self, process: Popen = None):
        self._process = process

    def get_active_process(self):
        return self._process

    def terminate(self):
        if self._process is None:
            return yaml.dump({"state": True, "msg": "currently there's no active process running"})
        try:
            self._process.terminate()
            return yaml.dump({"state": True, "msg": f"active process %i is terminated" % self._process.pid})
        except PermissionError:
            return yaml.dump({"state": False,
                              "msg": f"unable to terminate active process %i due to permission error" % self._process.pid})


cloud_client = Flask(__name__)

current_proc:Popen = None

current_task:str = None


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
