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


class ClusterNode:
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
                 compute_capability: int = 0,
                 region: Union[int, str] = None,
                 attributes: Dict = None) -> None:
        self._node_name = node_name
        self._node_type = node_type
        self._node_address = node_address
        self._node_port = node_port
        self._node_uuid = node_uuid
        self._node_state = node_state
        self._gpu_count = gpu_count
        self._compute_capability = compute_capability
        self._region = region
        self._attributes = attributes
        return

    def node_name(self):
        return self._node_name
    
    def node_type(self):
        return self._node_type

    def node_address(self):
        return self._node_address

    def node_port(self):
        return self._node_port

    def node_uuid(self):
        return self._node_uuid

    def node_state(self):
        return self._node_state

    def gpu_count(self):
        return self._gpu_count

    def compute_capability(self):
        return self._compute_capability

    def region(self):
        return self._region

    def attributes(self):
        return self._attributes

    def get_attribute(self, key):
        return self._attributes[key]


class Cluster:
    
    def __init__(self,
                 cluster_id: Union[int, str] = None,
                 cluster_name: str = None,
                 # master_node: ClusterNode = None,
                 # slave_nodes: Dict[int, ClusterNode] = None,
                 general_nodes: Dict[int, ClusterNode] = None) -> None:
        # self._master_node = master_node
        # self._slave_nodes = slave_nodes
        self._general_nodes = general_nodes
        self._cluster_id = cluster_id
        self._cluster_name = cluster_name
        return

    # def master_node(self) -> ClusterNode:
    #     return self._master_node
    #
    # def slave_nodes(self) -> Dict[int, ClusterNode]:
    #     return self._slave_nodes
    
    def general_nodes(self) -> Dict[int, ClusterNode]:
        return self._general_nodes

    def contains_node(self, node_uuid: int) -> bool:
        # if self._master_node is not None and self._master_node.node_uuid() == node_uuid:
        #     return True
        # if self._slave_nodes is not None and node_uuid in self._slave_nodes.keys():
        #     return True
        if self._general_nodes is not None and node_uuid in self._general_nodes.keys():
            return True
        return False
    
    def cluster_id(self) -> Union[int, str]:
        return self._cluster_id
    
    def cluster_name(self) -> str:
        return self._cluster_name

    def cluster_size(self) -> int:
        # m = 0 if self._master_node is None else 1
        # n = 0 if self._slave_nodes is None else len(self._slave_nodes)
        # k = 0 if self._general_nodes is None else len(self._general_nodes)
        # return m+n+k
        return 0 if self._general_nodes is None else len(self._general_nodes)

    def get_random_node_uuid(self) -> int:
        if self._general_nodes is None:
            return None
        if len(self._general_nodes) == 1:
            return self._general_nodes.values()[0].node_uuid()
        rand = random.Random();
        ret = rand.randint(0, len(self._general_nodes))
        i = 0
        for value in self._general_nodes.values():
            if i == ret:
                return value.node_uuid()
            i = i+1
        return -1


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
        if cluster.contains_node(cluster_node.node_uuid()):
            raise Exception(
                f"the specified cluster: %s already contains the cluster node: %i"
                % cluster_id % cluster_node.node_uuid())
        self._clusters.get(cluster_id)[cluster_node.node_uuid()] = cluster_node

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
