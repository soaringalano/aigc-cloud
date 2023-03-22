from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from abc import ABC


class BasicConsumerCallback(ABC):

    def on_message_callback(
            self,
            channel: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes) -> None:
        pass

class InvokeMethodConsumerCallback(BasicConsumerCallback):

    def __init__(self) -> None:
        return

    def on_message_callback(
            self,
            channel: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes) -> None:
        pass


class DisplayStdOutConsumerCallback(BasicConsumerCallback):

    def __init__(self) -> None:
        return

    def on_message_callback(
            self,
            channel: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes) -> None:
        pass


class DisplayStdErrConsumerCallback(BasicConsumerCallback):

    def __init__(self) -> None:
        return

    def on_message_callback(
            self,
            channel: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes) -> None:
        pass