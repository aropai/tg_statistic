from load_chat import Chat, User
from typing import Dict, Callable


def statistic(name: str) -> Callable[[Callable[[Chat], None]], Callable[[Chat], None]]:
    def decorator(function: Callable[[Chat], None]) -> Callable[[Chat], None]:
        def wrapper(chat: Chat) -> None:
            number_of_eq = (80 - len(name) - 4) // 2
            print(("=" * number_of_eq + "  " + name.upper() + "  " + number_of_eq * "=").center(80))
            function(chat)
            print("=" * 80, "\n")

        return wrapper

    return decorator


def _get_messages_count_by_sender(chat: Chat) -> Dict[User, int]:
    messages_count_by_sender: Dict[User, int] = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in messages_count_by_sender:
            messages_count_by_sender[sender] = 0
        messages_count_by_sender[sender] += 1

    return messages_count_by_sender


def _get_total_messages_length_by_sender(chat: Chat) -> Dict[User, int]:
    total_messages_length_by_sender: Dict[User, int] = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in total_messages_length_by_sender:
            total_messages_length_by_sender[sender] = 0
        total_messages_length_by_sender[sender] += len(message.text)

    return total_messages_length_by_sender


@statistic(name="number of messages")
def print_messages_count_by_sender(chat: Chat) -> None:
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    for sender in messages_count_by_sender:
        print(f"{sender.name} wrote {messages_count_by_sender[sender]} message(s)")


@statistic(name="total length of messages")
def print_total_messages_length_by_sender(chat: Chat) -> None:
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    for sender in total_messages_length_by_sender:
        print(f"{sender.name} wrote {total_messages_length_by_sender[sender]} symbol(s)")


@statistic(name="average len of message")
def print_average_messages_length_by_sender(chat: Chat) -> None:
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    for sender in messages_count_by_sender:
        average_message_length = round(
            total_messages_length_by_sender[sender] / messages_count_by_sender[sender], 2
        )
        print(f"The average len of {sender.name}'s message is {average_message_length} symbols")
