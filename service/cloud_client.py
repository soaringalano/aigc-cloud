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

from task.task_executor import *


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

