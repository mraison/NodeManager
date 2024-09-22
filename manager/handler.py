from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class RequestType(Enum):
    CREATE = 0
    UPDATE = 1
    PATCH = 2
    DELETE = 3


@dataclass
class Request:
    payload: Any
    request_type: RequestType


class RequestHandler:
    def __init__(self):
        self._routes = {}

    def set_routes(self, routes: dict[int, callable]):
        self._routes = routes

    def handle_request(self, req: Request):
        self._routes[req.request_type](req.payload)
