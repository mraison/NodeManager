from dataclasses import dataclass
from enum import Enum
import heapq


@dataclass
class Address:
    id: int
    name: str
    email: str

    def __eq__(self, other):
        return self.__key() == self.__key()

    def __key(self):
        return self.id, self.name, self.email

    def __hash__(self):
        return hash(self.__key())


@dataclass
class Device:
    id: int
    name: str
    subscribers: list[Address]


@dataclass
class AddressChunk:
    subscribers: set[Address]

    def __eq__(self, other):
        return len(self.subscribers) == len(other.subscribers)

    def __gt__(self, other):
        return len(self.subscribers) > len(other.subscribers)

    def __lt__(self, other):
        return len(self.subscribers) < len(other.subscribers)

    def __ge__(self, other):
        len(self.subscribers) >= len(other.subscribers)

    def __le__(self, other):
        len(self.subscribers) <= len(other.subscribers)


class AddressChunker:
    '''
    Composes a collection of address chunks
    '''
    def __init__(self, chunk_count):
        self._chunk_count = chunk_count
        self._chunks = []
        self._chunk_index_priority_queue = []
        self.clear_chunks()

    def get_chunks(self) -> list[AddressChunk]:
        return self._chunks

    def distribute_addresses(self, addresses: list[Address]):
        for address in addresses:
            _, chunk_index = heapq.heappop(self._chunk_index_priority_queue)
            self._chunks[chunk_index].subscribers.add(address)
            heapq.heappush(
                self._chunk_index_priority_queue,
                (
                    len(self._chunks[chunk_index].subscribers),
                    chunk_index
                )
            )

    def clear_chunks(self):
        self._chunks = []
        self._chunk_index_priority_queue = []
        for i in range(self._chunk_count):
            self._chunks.append(
                AddressChunk(
                    subscribers=set()
                )
            )
            self._chunk_index_priority_queue.append(
                (
                    0,
                    i
                )
            )


class DeviceChunkGroup:
    def __init__(self, chunk_count):
        self._chunk_count = chunk_count
        self._data: dict[int, AddressChunker] = {}

    def get_chunk_group(self, device_id: int) -> AddressChunker:
        return self._data.get(device_id, None)

    def create_device(self, device: Device):
        if device.id not in self._data:
            self._data[device.id] = AddressChunker(self._chunk_count)
            self.patch_device(device)
        else:
            raise Exception(f"Device {device.id} already in chunk group.")

    def delete_device(self, device: Device):
        if device.id in self._data:
            del self._data[device.id]

    def update_device(self, device: Device):
        if device.id not in self._data:
            raise Exception(f"{device.id} not found in chunk group.")

        self._data[device.id].clear_chunks()
        self._data[device.id].distribute_addresses(device.subscribers)

    def patch_device(self, device: Device):
        if device.id not in self._data:
            raise Exception(f"{device.id} not found in chunk group.")

        # we're not going to worry about repeats for now.
        self._data[device.id].distribute_addresses(device.subscribers)