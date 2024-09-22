from dataclasses import dataclass
from enum import Enum

from NodeManager.chunker.model import Device, DeviceChunkGroup


class RequestType(Enum):
    CREATE = 0
    UPDATE = 1
    PATCH = 2
    DELETE = 3


@dataclass
class DeviceRequest:
    device: Device
    request_type: RequestType


class DeviceRequestHandler:
    def __init__(self, chunk_count):
        self._chunk_group = DeviceChunkGroup(chunk_count=chunk_count)
        self._routes = {
            RequestType.CREATE: self._chunk_group.create_device,
            RequestType.UPDATE: self._chunk_group.update_device,
            RequestType.PATCH: self._chunk_group.patch_device,
            RequestType.DELETE: self._chunk_group.delete_device
        }

    def handle_request(self, req: DeviceRequest):
        self._routes[req.request_type](req.device)
