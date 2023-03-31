import random
from enum import Enum
from typing import List, Union, Dict
from pymongo import MongoClient
import os
from utils.environment_const import (ENVKEY_SYSTEM_CONNECTION_STRING, ENVKEY_SYSTEM_DATABASE_NAME, ENVKEY_SYSTEM_CLUSTER_COLLECTION)


def _init_database():
    connection_string = os.environ[ENVKEY_SYSTEM_CONNECTION_STRING]
    client = MongoClient(connection_string)
    db = client[ENVKEY_SYSTEM_DATABASE_NAME]
    col = db[ENVKEY_SYSTEM_CLUSTER_COLLECTION]
    return db, col


class NodeType(Enum):
    # MASTER_NODE = "MASTER_NODE"
    # SLAVE_NODE = "SLAVE_NODE"
    GENERAL_NODE = "GENERAL_NODE"
    MSG_EXCHANGE_NODE = "MSG_EXCHANGE_NODE"


class NodeState(Enum):
    BUSY = "BUSY"
    AVAILABLE = "AVAILABLE"
    NA = "NOT APPLICABLE"
    EXCEPTION = "HALTED"


class ClusterNode(Dict):

    node_name = 'node_name'
    node_type = 'node_type'
    node_address = 'node_address'
    node_port = 'node_port'
    node_uuid = 'node_uuid'
    node_state = 'node_state'
    gpu_count = 'gpu_count'
    computility = 'compute_capability'
    region = 'region'
    gpu_usage = 'gpu_usage'

    r"""
    Base class for cluster nodes, includes all basic attributes
    """
    def __init__(self,
                 cluster_id: str,
                 node_name: str = "default",
                 node_type: NodeType = NodeType.GENERAL_NODE,
                 node_address: str = "0.0.0.0",
                 node_port: int = 8081,
                 node_uuid: int = 0,
                 node_state: NodeState = NodeState.AVAILABLE,
                 gpu_count: int = 0,
                 computility: int = 0,
                 region: Union[int, str] = None) -> None:
        super().__init__()
        self[self.node_name] = node_name
        self[self.node_type] = node_type
        self[self.node_address] = node_address
        self[self.node_port] = node_port
        self[self.node_uuid] = node_uuid
        self[self.node_state] = node_state
        self[self.gpu_count] = gpu_count
        self[self.computility] = computility
        self[self.region] = region
        return

    def get_node_name(self):
        return self[self.node_name]
    
    def get_node_type(self):
        return self[self.node_type]

    def get_node_address(self):
        return self[self.node_address]

    def get_node_port(self):
        return self[self.node_port]

    def get_node_uuid(self):
        return self[self.node_uuid]

    def get_node_state(self):
        return self[self.node_state]

    def get_gpu_count(self):
        return self[self.gpu_count]

    def get_computbility(self):
        return self[self.computility]

    def get_region(self):
        return self[self.region]

    def set_gpu_usage(self, gpu_usage:Dict[int, float]):
        self[self.gpu_usage] = gpu_usage

    def get_gpu_usage(self) -> Dict[int, float]:
        return self[self.gpu_usage]


class Cluster:
    
    def __init__(self,
                 cluster_id: Union[int, str] = None,
                 cluster_name: str = None,
                 general_nodes: Dict[int, ClusterNode] = None) -> None:
        self._general_nodes:Dict[int, ClusterNode] = general_nodes
        self._cluster_id:str = cluster_id
        self._cluster_name:str = cluster_name
        return

    def get_cluster_node(self, node_uuid:int=-1):
        return self._general_nodes.get(node_uuid)

    def general_nodes(self) -> Dict[int, ClusterNode]:
        return self._general_nodes

    def contains_node(self, node_uuid: int) -> bool:
        if self._general_nodes is not None and node_uuid in self._general_nodes.keys():
            return True
        return False
    
    def cluster_id(self) -> Union[int, str]:
        return self._cluster_id
    
    def cluster_name(self) -> str:
        return self._cluster_name

    def cluster_size(self) -> int:
        return 0 if self._general_nodes is None else len(self._general_nodes)

    def get_random_node_uuid(self) -> int:
        if self._general_nodes is None:
            return -1
        if len(self._general_nodes) == 1:
            nodes = self._general_nodes.values()
            return List[ClusterNode](nodes)[0].get_node_uuid()
        rand = random.Random()
        ret = rand.randint(0, len(self._general_nodes))
        i = 0
        for value in self._general_nodes.values():
            if i == ret:
                return value.get_node_uuid()
            i = i+1
        return -1

    def get_cluster_nodes_usage(self) -> Dict[int, Dict[int, float]]:
        usage:Dict[int, Dict[int, float]] = {}
        for uuid in self._general_nodes.keys():
            use = self._general_nodes.get(uuid).get_gpu_usage()
            usage[uuid] = use
        return usage


class ClusterManager:

    def __init__(self) -> None:
        self._clusters: Dict[str, Cluster] = {}
        # self.database, self.table_clusters = _init_database()
        return

    def __load_database(self) -> None:
        return

    def add_cluster(self, cluster: Cluster) -> None:
        if cluster.cluster_id() in self._clusters.keys():
            raise Exception(f"the specified cluster: %s already exists, please check your input" % cluster.cluster_id())
        self._clusters[cluster.cluster_id()] = cluster

    def del_cluster(self, cluster_id: Union[int, str]) -> None:
        if cluster_id not in self._clusters.keys():
            raise Exception(f"the specified cluster: %s does not exist, please check your input" % cluster_id)
        self._clusters.pop(cluster_id)

    def add_cluster_node(self, cluster_id: Union[int, str], cluster_node:ClusterNode) -> None:
        if cluster_id not in self._clusters.keys():
            raise Exception(f"the specified cluster: %s does not exist, please check your input" % cluster_id)
        cluster: Cluster = self._clusters.get(cluster_id)
        if cluster.contains_node(cluster_node.get_node_uuid()):
            raise Exception(
                f"the specified cluster: %s already contains the cluster node: %i"
                % cluster_id % cluster_node.get_node_uuid())
        self._clusters.get(cluster_id)[cluster_node.get_node_uuid()] = cluster_node

    def del_cluster_node(self, cluster_id: Union[int, str], node_uuid: int) -> None:
        if cluster_id not in self._clusters.keys():
            raise Exception(f"the specified cluster: %s does not exist, please check your input" % cluster_id)
        cluster: Cluster = self._clusters.get(cluster_id)
        if not cluster.contains_node(node_uuid):
            raise Exception(
                f"the specified cluster: %s doesn't contain the cluster node: %i"
                % cluster_id % node_uuid)
        cluster.pop(node_uuid)
        return

    def get_cluster(self, cluster_id: Union[int, str]) -> Cluster:
        if cluster_id not in self._clusters.keys():
            raise Exception(f"the specified cluster: %s does not exist, please check your input" % cluster_id)
        return self._clusters[cluster_id]
    
    def get_cluster_node(self, cluster_id: Union[int, str], node_uuid: int) -> ClusterNode:
        if cluster_id not in self._clusters.keys():
            raise Exception(f"the specified cluster: %s does not exist, please check your input" % cluster_id)
        cluster: Cluster = self._clusters.get(cluster_id)
        if not cluster.contains_node(node_uuid):
            raise Exception(
                f"the specified cluster: %s doesn't contain the cluster node: %i"
                % cluster_id % node_uuid)
        return cluster[node_uuid]


if __name__ == "__main__":
    # print(NodeType.MASTER_NODE.value)
    # print(NodeType.SLAVE_NODE.value)
    print(NodeType.GENERAL_NODE.value)
