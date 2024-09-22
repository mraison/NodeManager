from dataclasses import dataclass

from NodeManager.model import Device

@dataclass
class Node:
    ip: str
    port: str

    def configure(self, device: Device):
        pass
