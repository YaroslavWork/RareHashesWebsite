import asyncio
import time
import aio_pika
from datetime import datetime

from app.models.hash import Hash
from app.utils.notification import log

class TelegramAPI:

    def __init__(self, rabbit_login: str, rabbit_host: str):
        self.__is_open = False

        self.__rabbit_host = rabbit_host
        self.__rabbit_login = rabbit_login

        self.__connection = None
        self.__channel = None

        self.__queue_income = []
        self.__queue_outcome = []

    async def open_connection(self, rabbit_password):
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
            log("TelegramAPI5", "Connection failed")
            return

    async def __handle_incoming(self, channel):
        queue = await channel.declare_queue("telegram_to_website", durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    message = message.body.decode()
                    self.__queue_income.append(message)
                    log("TelegramAPI1", f"Receive: {message}")
                    log("TelegramAPI2", "something")

    async def __send_message(self, channel):
        while True:
            for message in self.__queue_outcome:
                msg = aio_pika.Message(body=message.encode())
                await channel.default_exchange.publish(msg, routing_key="website_to_telegram")
                log("TelegramAPI3", f"Send: {message}")
            self.__queue_outcome = []
            await asyncio.sleep(2)

    def is_open(self) -> bool:
        return self.__is_open

    async def wait_for_matching_message(self, expected_prefix: str, timeout: float = 5.0) -> list[str] | None:
        timemark = time.time()
        while time.time() - timemark < timeout:
            for message in self.__queue_income[:]:  # iterate over a shallow copy
                log("Telegram API (wait for matching message)", message)
                if message.startswith(expected_prefix):
                    self.__queue_income.remove(message)  # safe remove
                    return message.split(expected_prefix)[1].split('|NEXT|')

            await asyncio.sleep(0.1)
             
    def add_new_user(self, user_id:str, user_instruction: str='M25') -> None:
        self.__queue_outcome.append(f'|ADD|{user_id}|NEXT|{user_instruction}')

    def notify(self, hash: Hash, top: int):
        if hash.is_complete():
            self.__queue_outcome.append(f'|NEW|{hash.word}|NEXT|{hash.isFromBeginning}|NEXT|{hash.hashType}|NEXT|{hash.counts}|NEXT|{hash.user}|NEXT|{hash.createdAt}|NEXT|{top}')
        else:
            log("TelegramAPI", "Hash is not complete")