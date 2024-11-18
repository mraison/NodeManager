from threading import Thread
import logging
import uuid
from pathlib import Path
from kombu.mixins import ConsumerMixin
from kombu import Exchange, Queue
from kombu import Connection

from NodeManager.model import DeviceCollection
from NodeManager.node.utils import GmailSender


class Worker(ConsumerMixin):
    uid = uuid.uuid4()
    task_queue = Queue(
        f'panic_queue-{str(uid)}',
        Exchange(
            'panic_ex',
            type='direct',
        ),
        'panic_key'
    )

    def __init__(self, connection, devices_config: DeviceCollection, mail_sender: GmailSender):
        self.connection = connection
        self._device_config_map = {device_config.id: device_config for device_config in devices_config.devices}
        self._mail_sender = mail_sender

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[self.task_queue],
                         callbacks=[self.on_message])]

    def on_message(self, body, message):
        device_id = body.get('device_id', None)
        device_state = body.get('state', None)
        if device_id:
            device_conf = self._device_config_map.get(device_id, None)
            if device_conf:
                for address in device_conf.subscribers:
                    self._mail_sender.send(
                        subject=f"{device_conf.name}: {'healthy' if device_state else 'panic'}",
                        body=(
                            f"Device \"{device_conf.name}\" is in a {'healthy' if device_state else 'panic'} state"
                            f" at {body.get('check_time', None)}."
                        ),
                        recipients=[address.email]
                    )
        message.ack()


class ConsumerRunner:
    def __init__(
        self,
        amqp_url: str,
        devices_config: DeviceCollection,
        mail_sender: GmailSender
    ):
        self._amqp_url = amqp_url
        self._devices_config = devices_config
        self._thread = None
        self._mail_sender = mail_sender

    def set_devices_config(self, devices_config: DeviceCollection):
        self._devices_config = devices_config

    @staticmethod
    def _run_thread(amqp_url, devices_config, mail_sender):
        with Connection(amqp_url) as conn:
            Worker(conn, devices_config, mail_sender).run()

    def start(self):
        if self._thread:
            raise Exception("Thread already running.")
        self._thread = Thread(
            target=self._run_thread,
            args=(
                self._amqp_url,
                self._devices_config,
                self._mail_sender
            )
        )
        self._thread.start()

    def restart(self):
        if self._thread:
            self.stop()
        self.start()

    def stop(self):
        if not self._thread:
            raise Exception("Thread not running.")
        Worker.should_stop = True
        self._thread.join(0.1)
        if self._thread.is_alive():
            raise Exception("Consumer thread didn't close")
