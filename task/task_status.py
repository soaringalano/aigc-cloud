import subprocess
import traceback
import threading
from typing import Union, List
from abc import ABC


class CMDProcess(threading.Thread):

    def __init__(self, args: Union[str, List[str]], callback):
        threading.Thread.__init__(self)
        self.proc = None
        self.args: Union[str, List[str]] = args
        self.callback = callback

    def run(self):
        shell = isinstance(self.args, str)
        self.proc = subprocess.Popen(
            args=self.args,
            bufsize=0,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        while self.proc.poll() is None:
            print("start readline")
            out = self.proc.stdout.readline()
            err = self.proc.stderr.readline()
            print("end readline")
            out = out.decode("utf8")
            err = err.decode("utf8")

            # with open("cmdlog.txt",'a+') as cmdlog:
            #    cmdlog.write(line)

            if self.callback is not None:
                self.callback(out, err)


class TaskOutputConsumer(ABC):
    def __init__(self):
        pass

    def consume(self, stdout, stderr):
        pass

    def close(self, closed):
        pass


class TaskLoggingConsumer(TaskOutputConsumer):
    def __init__(self, period=60000):
        super().__init__()
        self._is_closed = False
        self._period = 60000

    def consume(self, stdout=None, stderr=None, period: int = 60000):
        if self.is_closed:
            return

        return

    def close(self, closed:bool):
        self._is_closed = closed
