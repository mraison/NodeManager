from multiprocessing import Process
from kombu.mixins import ConsumerMixin
from kombu import Exchange, Queue
from kombu import Connection

from NodeManager.model import DeviceCollection


class Worker(ConsumerMixin):
    task_queue = Queue(
        'panic_queue',
        Exchange(
            'panic_exchange'
        ),
        'panic_router'
    )

    def __init__(self, connection, devices_config: DeviceCollection):
        self.connection = connection
        self.devices_config = devices_config

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[self.task_queue],
                         callbacks=[self.on_task])]

    def on_task(self, body, message):
        print('Got task: {0!r}'.format(body))
        message.ack()


class WorkerFactory:
    def __init__(self, amqp_cli):
        self._amqp_cli = amqp_cli

    def create(self, devices_config: DeviceCollection):
        conn = self._amqp_cli.get_connection()
        return conn, Worker(
            conn,
            devices_config
        )


class EventConsumerRunner:
    def __init__(
        self,
        devices_config: DeviceCollection,
        worker_factory: WorkerFactory
    ):
        self._devices_config = devices_config
        self._proc = Process(target=self._consume, args=(self._devices_config,))
        self._worker_factory = worker_factory

    def start(self):
        self._proc.start()

    def stop(self):
        if self._proc.is_alive():
            self._proc.close()
            if self._proc.is_alive():
                self._proc.terminate()

    def _consume(self, devices_config: DeviceCollection):
        conn, w = self._worker_factory.create(devices_config)
        w.run()
        conn.close()
