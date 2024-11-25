import os
from flask import Flask, request, Response

from NodeManager.manager.__main__ import service_command_map, service

app = Flask(__name__)

node_web = os.environ.get('NODE_WEB', 'http://127.0.0.1:8000/data/device')

@app.route("/config", methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        payload = request.get_json()
        if 'node_count' not in payload:
            raise Exception("node count not passed in post.")

        node_count = payload['node_count']
        # reset service
        service_command_map(
            [
                'reset'
            ]
        )
        # set device source
        service_command_map(
            [
                'device', 'source', node_web
            ]
        )
        # pull configuration
        service_command_map(
            [
                'device', 'pull'
            ]
        )
        # add nodes
        for _ in range(node_count):
            service_command_map(
                [
                    'node', 'add'
                ]
            )
        # distribute config
        service_command_map(
            [
                'node', 'send-conf'
            ]
        )

        return Response(None, status=200)
    if request.method == 'GET':
        return {
            'node_configs': service._conf.node_configs.to_struct(),
            'device_configs': service._conf.device_configs.to_struct(),
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
