import os
from flask import Flask, request, Response
from kombu import Connection

from NodeManager.model import DeviceCollection
from NodeManager.node.process import ConsumerRunner
from NodeManager.node.utils import GmailSender

app = Flask(__name__)

global c
c = DeviceCollection([])

rabbit_url = os.environ.get('AMQP_URL', '')
email_publisher = os.environ.get('EMAIL_PUBLISHER', '')
email_token = os.environ.get('EMAIL_TOKEN', '')


@app.route("/config", methods=['GET', 'POST'])
def config():
    global c
    consumer_runner = ConsumerRunner(
        rabbit_url,
        c,
        GmailSender(
            email_publisher,
            email_token,
        )
    )
    if request.method == 'POST':
        c = DeviceCollection.load_from_struct(request.get_json())
        consumer_runner.set_devices_config(c)
        consumer_runner.restart()
        return Response(None, status=200)
    if request.method == 'GET':
        return c.to_struct()
