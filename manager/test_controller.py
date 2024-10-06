from unittest.mock import patch, MagicMock

from NodeManager.model import DeviceCollection, ConfigModel
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
            ConfigModel(mock_devices_dao)
        )
        assert m.central_config.get().devices == []
        m.load_central_config()
        expected_config = DeviceCollection.load_from_struct(get_dummy_devices_config())
        assert m.central_config.get() == expected_config

    @patch('NodeManager.manager.dao.NodeDAO')
    @patch('NodeManager.dao.DeviceDAO')
    def test_configure_nodes(self, mock_devices_dao, mock_node_dao):
        mock_devices_dao.get = MagicMock(return_value=get_dummy_devices_config())
        mock_node_dao.get = MagicMock(return_value=[])
        mock_node_dao.post = MagicMock(return_value=True)

        m = NodeManager(
            [Node('0.0.0.0', '1234', mock_node_dao)],
            ConfigModel(mock_devices_dao)
        )
        assert m.central_config.get().devices == []
        m.load_central_config()
        m.configure_nodes()

        assert mock_node_dao.post.called
        expected_node_config = DeviceCollection.load_from_struct(get_dummy_devices_config())
        m.nodes[0].get_config() == expected_node_config
