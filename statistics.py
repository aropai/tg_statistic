from load_chat import Chat, User
from typing import Dict, Callable, List, Tuple

BORDERS_LENGTH = 80


def statistic(name: str) -> Callable[[Callable[[Chat], None]], Callable[[Chat], None]]:
    def decorator(statistic_function: Callable[[Chat], None]) -> Callable[[Chat], None]:
        def wrapper(chat: Chat) -> None:
            print(f" {name.upper()} ".center(BORDERS_LENGTH, "="))
            statistic_function(chat)
            print("=" * BORDERS_LENGTH)
            print()

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


def _sorted_by_value(messages_by_sender: Dict[User, int]) -> List[User]:
    return sorted(messages_by_sender, key=lambda sender: -messages_by_sender[sender])


@statistic(name="number of messages")
def print_messages_count_by_sender(chat: Chat) -> None:
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    for sender in _sorted_by_value(messages_count_by_sender):
        print(f"{sender.name} wrote {messages_count_by_sender[sender]} message(s)")


@statistic(name="total length of messages")
def print_total_messages_length_by_sender(chat: Chat) -> None:
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    for sender in _sorted_by_value(total_messages_length_by_sender):
        print(f"{sender.name} wrote {total_messages_length_by_sender[sender]} symbol(s)")


@statistic(name="average len of message")
def print_average_messages_length_by_sender(chat: Chat) -> None:
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    average_messages_length_by_sender: Dict[User, int] = dict()
    for sender in total_messages_length_by_sender:
        average_messages_length_by_sender[sender] = int(100 * total_messages_length_by_sender[sender] / messages_count_by_sender[sender])
    for sender in _sorted_by_value(average_messages_length_by_sender):
        print(f"The average len of {sender.name}'s message is {average_messages_length_by_sender[sender] / 100} symbols")


def _get_replies_count_by_users(chat: Chat) -> Dict[User, Dict[User, int]]:
    replies_count_by_users: Dict[User, Dict[User, int]] = dict()
    for message in chat.messages:
        if not message.reply_to_message_id or message.reply_to_message_id not in chat.message_by_id:
            continue
        sender = message.sender
        replied_message = chat.message_by_id[message.reply_to_message_id]
        if sender not in replies_count_by_users:
            replies_count_by_users[sender] = dict()
        if replied_message.sender not in replies_count_by_users[sender]:
            replies_count_by_users[sender][replied_message.sender] = 0
        replies_count_by_users[sender][replied_message.sender] += 1

    return replies_count_by_users


def _get_replies_count_to_users(chat: Chat) -> Dict[User, Dict[User, int]]:
    replies_count_to_users: Dict[User, Dict[User, int]] = dict()
    for message in chat.messages:
        if not message.reply_to_message_id or message.reply_to_message_id not in chat.message_by_id:
            continue
        sender = message.sender
        replied_message = chat.message_by_id[message.reply_to_message_id]
        if replied_message.sender not in replies_count_to_users:
            replies_count_to_users[replied_message.sender] = dict()
        if sender not in replies_count_to_users[replied_message.sender]:
            replies_count_to_users[replied_message.sender][sender] = 0
        replies_count_to_users[replied_message.sender][sender] += 1

    return replies_count_to_users


def _get_top_replies(replies_count: Dict[User, int]) -> List[Tuple[User, int]]:
    top_replies = list(replies_count.items())
    top_replies.sort(key=lambda x: -x[1])
    top_replies = top_replies[:3]
    return top_replies


@statistic(name="most often replies")
def print_most_often_replies(chat: Chat) -> None:
    replies_count_by_users = _get_replies_count_by_users(chat)
    for sender in replies_count_by_users:
        top_replies = _get_top_replies(replies_count_by_users[sender])
        if len(top_replies) == 0:
            print(f"{sender.name} replies nobody", end="")
        else:
            print(
                f"{sender.name} most often replies",
                ", ".join([f"{entry[0].name} ({entry[1]} times)" for entry in top_replies])
            )


@statistic(name="most often replied by")
def print_most_often_replies_to(chat: Chat) -> None:
    replies_count_to_users = _get_replies_count_to_users(chat)
    for replied_sender in replies_count_to_users:
        top_replies = _get_top_replies(replies_count_to_users[replied_sender])
        if len(top_replies) == 0:
            print(f"Nobody replies to {replied_sender.name}", end="")
        else:
            print(
                f"{replied_sender.name} was most often replied by",
                ", ".join([f"{entry[0].name} ({entry[1]} times)" for entry in top_replies])
            )
