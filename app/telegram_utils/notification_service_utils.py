import asyncio
import time
import queue

from app.services.telegram_api import TelegramAPI
from app.models.hash import Hash


def add_new_user(telegramAPI: TelegramAPI, telegramID: str, rule: str, minimum_value: str) -> str:
    """
    Adds a new user to the TelegramAPI queue with a rule-based condition.

    Based on the provided rule, the function formats the minimum value and sends it
    to the TelegramAPI using the given Telegram user ID.

    Args:
        telegramAPI (TelegramAPI): Instance of the TelegramAPI used to send user configuration.
        telegramID (str): The Telegram user ID to register.
        rule (str): The rule type for filtering or evaluating values. Accepted values: 'rarity', 'ranking'.
        minimum_value (str): The threshold value for the rule.

    Returns:
        str: A unique identifier (UUID) for the operation, which can be used to track the request.
    """

    uuid = ''
    if rule == 'rarity':
        uuid = telegramAPI.add_to_queue(f'|ADD|{telegramID}|NEXT|M{minimum_value}')
    elif rule == 'ranking':
        uuid = telegramAPI.add_to_queue(f'|ADD|{telegramID}|NEXT|T{minimum_value}')
    
    return uuid


def add_new_hash(telegramAPI: TelegramAPI, hash: Hash, top: int) -> str:
    """
    Adds a new hash to the TelegramAPI queue for notification.

    This function formats the hash data and sends it to the TelegramAPI for processing.

    Args:
        telegramAPI (TelegramAPI): Instance of the TelegramAPI used to send hash notifications.
        hash (Hash): The Hash object containing details about the hash.
        top (int): The top ranking or position of the hash in the context of notifications. (from database)

    Returns:
        str: A unique identifier (UUID) for the operation, which can be used to track the request.
    """

    if not hash.is_complete():
        return ''

    uuid = telegramAPI.add_to_queue(f'|NEW|{hash.word}|NEXT|{hash.isFromBeginning}|NEXT|{hash.hashType}|NEXT|{hash.counts}|NEXT|{hash.user}|NEXT|{hash.createdAt}|NEXT|{top}')
    return uuid


def remove_user(telegramAPI: TelegramAPI, telegramID: str) -> str:
    """
    Removes a user from the TelegramAPI queue.

    This function sends a request to the TelegramAPI to remove a user based on their Telegram ID.

    Args:
        telegramAPI (TelegramAPI): Instance of the TelegramAPI used to send user removal requests.
        telegramID (str): The Telegram user ID to remove.

    Returns:
        str: A unique identifier (UUID) for the operation, which can be used to track the request.
    """

    uuid = telegramAPI.add_to_queue(f'|REM|{telegramID}')
    return uuid


async def wait_until_response(telegramAPI: TelegramAPI, message_uuid: str, max_time_in_seconds: int = 5) -> int:
    """
    Waits for a response from the Telegram queue within a specified timeout period.

    This function checks the TelegramAPI for a response matching the provided UUID.

    Args:
        telegramAPI (TelegramAPI): An instance of the TelegramAPI class used to query the message queue.
        message_uuid (str): The unique identifier for the message to wait for.
        max_time_in_seconds (int, optional): Maximum time in seconds to wait for a response. Defaults to 5.

    Returns:
        str: The error number in case of some errors 0 if everything good, time up return -1.
    """

    if not telegramAPI.is_open():
        return -1
    
    messages = await telegramAPI.wait_for_matching_message(message_uuid, timeout=max_time_in_seconds)
    if messages is None:
        return -1

    if messages[0] == 'suc':
        return 0
    elif messages[0] == 'errno':
        return int(messages[1])

    return -1