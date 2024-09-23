from unittest.mock import patch, MagicMock

from NodeManager.model import DeviceCollection
from NodeManager.manager.model import Node
from NodeManager.manager.controller import NodeManager


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

class TestManager:
    @patch('NodeManager.manager.dao.NodeDAO')
    @patch('NodeManager.dao.DeviceDAO')
    def test_load_devices(self, mock_devices_dao, mock_node_dao):
        mock_devices_dao.get = MagicMock(return_value=get_dummy_devices_config())
        mock_node_dao.get = MagicMock(return_value=[])
        mock_node_dao.post = MagicMock(return_value=True)

        m = NodeManager(
            [Node('0.0.0.0', '1234', mock_node_dao)],
            DeviceCollection(mock_devices_dao)
        )
        assert m.devices.data == []
        m.load_devices()
        assert len(m.devices.data) == 2
        assert m.devices.data[0].to_dict() == get_dummy_devices_config()[0]
        assert m.devices.data[1].to_dict() == get_dummy_devices_config()[1]

        assert len(m.device_chunk_groups.get_chunk_groups(1)[0].subscribers) == 1
        assert len(m.device_chunk_groups.get_chunk_groups(2)[0].subscribers) == 2

    @patch('NodeManager.manager.dao.NodeDAO')
    @patch('NodeManager.dao.DeviceDAO')
    def test_configure_nodes(self, mock_devices_dao, mock_node_dao):
        mock_devices_dao.get = MagicMock(return_value=get_dummy_devices_config())
        mock_node_dao.get = MagicMock(return_value=[])
        mock_node_dao.post = MagicMock(return_value=True)

        m = NodeManager(
            [Node('0.0.0.0', '1234', mock_node_dao)],
            DeviceCollection(mock_devices_dao)
        )
        assert m.devices.data == []
        m.load_devices()
        m.configure_nodes()

        assert mock_node_dao.post.called
