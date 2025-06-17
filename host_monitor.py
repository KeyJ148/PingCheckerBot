import random
import subprocess
import time
import os
import platform
from enum import Enum, auto

class HostState(Enum):
    ONLINE = auto()
    OFFLINE = auto()

class HostMonitor:
    def __init__(self, state_listener):
        self.host = os.environ.get('PING_HOST')
        self.state_listener = state_listener
        self.state = HostState.ONLINE

        self.timeout_on_success = int(os.environ.get('TIMEOUT_ON_SUCCESS'))
        self.timeout_on_fail = int(os.environ.get('TIMEOUT_ON_FAIL'))
        self.retry_on_fail = int(os.environ.get('RETRY_ON_FAIL'))

    def get_state(self):
        return self.state == HostState.ONLINE

    def set_state(self, new_state):
        print("[HostMonitor.set_state] New state: " + str(new_state))
        self.state = new_state
        self.state_listener(self.get_state())

    def ping_host(self):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", self.host]
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0

    def start(self):
        print("[HostMonitor.start] Start...")
        while True:
            success = self.ping_host()

            if self.state != HostState.ONLINE and success:
                self.set_state(HostState.ONLINE)
                time.sleep(self.timeout_on_success)

            elif self.state == HostState.ONLINE and not success:
                for _ in range(self.retry_on_fail):
                    time.sleep(self.timeout_on_fail)
                    if self.ping_host():
                        break
                else:
                    self.set_state(HostState.OFFLINE)
                    time.sleep(self.timeout_on_fail)
                    continue

            elif self.state == HostState.OFFLINE and not success:
                time.sleep(self.timeout_on_fail)

            elif self.state == HostState.OFFLINE and success:
                self.set_state(HostState.ONLINE)
                time.sleep(self.timeout_on_success)

            else:
                time.sleep(self.timeout_on_fail)