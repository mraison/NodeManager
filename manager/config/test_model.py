import json
import tempfile
from pathlib import Path

from NodeManager.manager.config.model import Config


class TestConfig:
    def test_struct(self):
        conf_d = {"nodes": [], "devices": {"source": "", "devices": []}}
        with tempfile.TemporaryDirectory() as d:
            tmp_f = Path(d) / 'conf.json'
            tmp_f.write_text(
                json.dumps(conf_d)
            )

            c = Config(
                config_file=tmp_f
            )
            c.load()

            assert c.node_configs.nodes == []
            assert c.device_configs.source == ""
            assert c.device_configs.devices.devices == []
