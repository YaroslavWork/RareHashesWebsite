import asyncio
import time
import aio_pika
from datetime import datetime

from app.models.hash import Hash
from app.utils.notification import log
from app.utils.uuid_utils import generate_uuid

class TelegramAPI:
    """
    A class to handle communication with the Telegram API using RabbitMQ.
    """

    def __init__(self, rabbit_login: str, rabbit_host: str) -> None:
        """
        Initialize the TelegramAPI instance.
        This constructor sets up the RabbitMQ connection parameters and initializes the queues for incoming and outgoing messages.

        Args:
            rabbit_login (str): RabbitMQ login credentials.
            rabbit_host (str): RabbitMQ host address.
        """

        self.__is_open = False

        self.__rabbit_host = rabbit_host
        self.__rabbit_login = rabbit_login

        self.__connection = None
        self.__channel = None

        self.__queue_income = []
        self.__queue_outcome = []

    async def open_connection(self, rabbit_password: str) -> None:
        """
        Open a connection to the Telegram API using RabbitMQ.

        Description:
            This method establishes a connection to the Telegram API via RabbitMQ.
            It creates a channel and starts two asynchronous tasks: one for handling incoming messages
            and another for sending messages from the outcome queue.
            The connection remains open until manually closed or an error occurs.

        Args:
            rabbit_password (str): The password for the RabbitMQ user to authenticate the connection.
        """

        try:
            self.__connection = await aio_pika.connect_robust(f"amqp://{self.__rabbit_login}:{rabbit_password}@{self.__rabbit_host}/")
            self.__channel = await self.__connection.channel()

            asyncio.create_task(
                self.__handle_incoming(self.__channel)
                )
            asyncio.create_task(
                self.__send_message(self.__channel)
            )
            self.__is_open = True

            # Keep running so the tasks can do their job
            while True:
                await asyncio.sleep(2)
        except:
            log("TelegramAPI", "Connection failed")
            return

    async def __handle_incoming(self, channel: aio_pika.Channel) -> None:
        """
        Handle incoming messages from the Telegram channel (with rabbitmq).

        Description:
            This method listens for incoming messages from the Telegram channel via RabbitMQ.
            It declares a queue named "telegram_to_website" and processes messages as they arrive.
            Each message is decoded and added to the income queue, which can be accessed later.`

        Args:
            channel (aio_pika.Channel): The channel to listen for incoming messages.
        """

        queue = await channel.declare_queue("telegram_to_website", durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    message = message.body.decode()
                    self.__queue_income.append(message)
                    log("TelegramAPI", f"Receive: {message}")

    async def __send_message(self, channel: aio_pika.Channel) -> None:
        """
        Send messages from the outcome queue to the Telegram channel (with rabbitmq).

        Description:
            This method continuously checks the outcome queue for messages and sends them to the Telegram channel.
            It uses a default exchange to publish messages with a routing key of "website_to_telegram".
            It runs indefinitely, sending messages every 2 seconds.

        Args:
            channel (aio_pika.Channel): The channel to send messages through.
        """

        while True:
            for message in self.__queue_outcome:
                msg = aio_pika.Message(body=message.encode())
                await channel.default_exchange.publish(msg, routing_key="website_to_telegram")
                log("TelegramAPI", f"Send: {message}")
            self.__queue_outcome = []
            await asyncio.sleep(2)

    def is_open(self) -> bool:
        """Check if the connection to the Telegram API is open.

        Returns:
            bool: True if the connection is open, False otherwise.
        """

        return self.__is_open

    async def wait_for_matching_message(self, message_uuid: str, timeout: float = 5.0) -> list[str] | None:
        """
        Wait for a message in the income queue that starts with the specified UUID.

        Args:
            message_uuid (str): The UUID to match against the start of the messages in the queue.
            timeout (float, optional): Maximum time to wait for a matching message, in seconds. Defaults to 5.0.

        Returns:
            list[str] | None: A list of strings containing the message parts if a matching message is found, or None if no match is found within the timeout.
        """
        
        timemark: float = time.time()
        while time.time() - timemark < timeout:
            for message in self.__queue_income[:]:  # iterate over a shallow copy
                is_that_message: bool = message.startswith(message_uuid)
                if is_that_message:
                    self.__queue_income.remove(message)  # safe remove
                    return '|'.join(message.split('|')[2:]).split('|NEXT|')  # ex. 'uuid(0)|ADD(1)|suc(2)|NEXT(3)|M25(4)' -> ['suc', 'M25']

            await asyncio.sleep(0.1)

    def add_to_queue(self, message: str) -> str:
        """
        Add a message to the outgoing queue.
        
        Args:
            message (str): The message to be added to the queue.

        Returns:
            str: A unique identifier (UUID) for the message.
        """

        uuid = generate_uuid()
        self.__queue_outcome.append(f'{uuid}{message}')
        return uuid
