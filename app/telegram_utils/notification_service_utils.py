import asyncio
import time
import queue

from app.services.telegram_api import TelegramAPI


def add_new_user(telegramAPI: TelegramAPI, telegramID: str, rule: str, minimum_value: str) -> None:
    """
    Adds a new user to the TelegramAPI queue with a rule-based condition.

    Based on the provided rule, the function formats the minimum value and sends it
    to the TelegramAPI using the given Telegram user ID.

    Args:
        telegramAPI (TelegramAPI): Instance of the TelegramAPI used to send user configuration.
        telegramID (str): The Telegram user ID to register.
        rule (str): The rule type for filtering or evaluating values. Accepted values: 'rarity', 'ranking'.
        minimum_value (str): The threshold value for the rule.
    """

    if rule == 'rarity':
        telegramAPI.add_new_user(telegramID, f'M{minimum_value}')
    elif rule == 'ranking':
        telegramAPI.add_new_user(telegramID, f'T{minimum_value}')


async def wait_until_response(telegramAPI: TelegramAPI, operation_type: str, max_time_in_seconds: int = 5) -> int:
    """_
    Waits for a response from the Telegram queue within a specified timeout period.

    Continuously checks the message queue of the provided TelegramAPI instance for a specific 
    type of operation (e.g., 'add'). If a message matching the criteria is found before the 
    timeout, it returns the first message found. Otherwise, returns None after the timeout.

    Args:
        telegramAPI (TelegramAPI): An instance of the TelegramAPI class used to query the message queue.
        operation_type (str): The type of operation to wait for. Currently supports 'add'.
        max_time_in_seconds (int, optional): Maximum time in seconds to wait for a response. Defaults to 5.

    Returns:
        str: The error number in case of some errors 0 if everything good, time up return -1.
    """

    if not telegramAPI.is_open():
        return -1

    if operation_type == 'add':
        messages = await telegramAPI.wait_for_matching_message('|ADD|', max_time_in_seconds)
        if messages is None:
            return -1

        if messages[0] == 'suc':
            return 0
        elif messages[0] == 'errno':
            return int(messages[1])

    return -1