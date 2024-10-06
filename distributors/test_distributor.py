from .distributors import distribute_device_address_book
from NodeManager.model import DeviceCollection

def get_dummy_devices_config():
    return [
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


def get_dummy_node_distribution_of_2():
    return [
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
                ],
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
                ]
            }
        ],
        [
            {
                "id": 2,
                "name": "warn button",
                "subscribers": [
                    {
                        "id": 2,
                        "name": "mraison",
                        "email": "probablymattraison@gmail.com"
                    }
                ]
            }
        ]
    ]


def test_distribute_device_address_book():
    input = get_dummy_devices_config()
    input_obj = DeviceCollection.load_from_struct(input)
    expected = get_dummy_node_distribution_of_2()
    expected_obj = [DeviceCollection.load_from_struct(ex) for ex in expected]
    assert distribute_device_address_book(input_obj, 2) == expected_obj
