import json
import logging
import ssl

from threading import Thread
from time import sleep
from typing import Callable

from websocket import WebSocketApp

logger = logging.getLogger(__name__)


class WsSession(WebSocketApp):
    def __init__(self,
                 url: str,
                 on_message_callback: Callable,
                 on_error_callback: Callable,
                 on_connect_callback: Callable,
                 retry_count: int = 3,
                 timeout: int = 10,
                 **kwargs):
        self.on_message_callback = on_message_callback
        self.on_error_callback = on_error_callback
        self.on_connect_callback = on_connect_callback
        self.retry_count = retry_count
        self.timeout = timeout

        self._connected = False
        self._is_connecting = False
        self._is_error = False

        super().__init__(url=url,
                         on_open=self._on_open,
                         on_message=self._on_message,
                         on_error=self._on_error,
                         on_close=self._on_close,
                         **kwargs)

        self.thread: Thread = None
        self.run()

    def _on_open(self, ws: WebSocketApp):
        logger.info(f"Connected to {self.url}")
        self._is_connecting = False
        self._connected = True

    def _on_error(self, ws: WebSocketApp, error):
        logger.error(f"Error while connecting to {self.url}: {error}")
        self._is_error = True
        self._is_connecting = False
        self._connected = False
        self.on_error_callback()

    def _on_close(self, ws: WebSocketApp, close_status_code, close_msg):
        logger.warning(f"Websocket closed with status {close_status_code} and message {close_msg}")
        self._is_connecting = False
        self._connected = False
        self._is_error = False

    def _on_message(self, ws: WebSocketApp, income_data):
        try:
            self.on_message_callback(json.loads(income_data))
        except Exception as e:
            logger.error(f"Error while processing data {income_data}: {e}")
            ws.close()

    def _run(self):
        self.run_forever(reconnect=self.retry_count, **{"sslopt": {"cert_reqs": ssl.CERT_NONE}})

    @property
    def is_connected(self):
        return self._connected

    @property
    def is_error(self):
        return self._is_error

    def run(self, url: str = None):
        logger.info(f"Connecting websocket to {url or self.url}")

        self.url = url or self.url
        self._is_connecting = True
        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()

        timer = 0
        while self._is_connecting:
            sleep(0.01)
            timer += 0.01
            if timer > self.timeout:
                logger.error(f"Timeout while connecting to {self.url}")
                self._is_connecting = False
                self._is_error = True
                raise ConnectionError(f"Timeout while connecting to WS by url {self.url}")

    def stop(self):
        logger.info(f"Stopping websocket connection to {self.url}")

        self.close()
        if self.thread:
            self.thread.join()
