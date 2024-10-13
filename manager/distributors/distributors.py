"""
Assume input of form:
[
        {
            "id": 1,
            "name": "panic button",
            "subscribers": [
                {
                    "id": 1,
                    "name": "Matthew Raison",
                    "email": "MatthewRaison@outlook.com"
                }
            ]
        },
        {
            "id": 2,
            "name": "warn button",
            "subscribers": [
                {
                    "id": 1,
                    "name": "Matthew Raison",
                    "email": "MatthewRaison@outlook.com"
                },
                {
                    "id": 2,
                    "name": "mraison",
                    "email": "probablymattraison@gmail.com"
                }
            ]
        }
    ]
"""
from dataclasses import replace

from NodeManager.model import DeviceCollection, Device


def distribute_device_address_book(device_address_book: DeviceCollection, num_nodes: int):
    distributed_chunks: list[dict[int, Device]] = []
    for _ in range(num_nodes):
        distributed_chunks.append({})

    # sort address book into chunks according to the number of node we'll have.
    # this will just round-robin sort them.
    for device in device_address_book.devices:
        for i, address in enumerate(device.subscribers):
            if device.id not in distributed_chunks[i % num_nodes]:
                distributed_chunks[i % num_nodes][device.id] = replace(device, subscribers=[])
            distributed_chunks[i % num_nodes][device.id].subscribers.append(address)

    # remove the unnecessary dict layer mapping device id to device.
    final = []
    for chunk in distributed_chunks:
        final.append(
            DeviceCollection(list(chunk.values()))
        )

    return final



