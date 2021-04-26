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


def _get_replies_by_users(chat: Chat) -> Dict[User, Dict[User, int]]:
    replies_by_users: Dict[User, Dict[User, int]] = dict()
    for message in chat.messages:
        if not message.reply_to_message_id:
            continue
        sender = message.sender
        replied_message = chat.get_message(message.reply_to_message_id)
        if sender not in replies_by_users:
            replies_by_users[sender] = dict()
        if replied_message.sender not in replies_by_users[sender]:
            replies_by_users[sender][replied_message.sender] = 0
        replies_by_users[sender][replied_message.sender] += 1

    return replies_by_users


@statistic(name="most often replies")
def print_most_often_replies(chat: Chat) -> None:
    replies_by_users = _get_replies_by_users(chat)
    for sender in replies_by_users:
        first_replied_name = second_replied_name = third_replied_name = ""
        first_number_of_replies = second_number_of_replies = third_number_of_replies = 0
        for replied_user in replies_by_users[sender]:
            if replies_by_users[sender][replied_user] > first_number_of_replies:
                first_number_of_replies = replies_by_users[sender][replied_user]
                first_replied_name = replied_user.name
            elif replies_by_users[sender][replied_user] > second_number_of_replies:
                second_number_of_replies = replies_by_users[sender][replied_user]
                second_replied_name = replied_user.name
            elif replies_by_users[sender][replied_user] > third_number_of_replies:
                third_number_of_replies = replies_by_users[sender][replied_user]
                third_replied_name = replied_user.name
        if first_number_of_replies == 0:
            print(f"{sender.name} replies nobody", end="")
        else:
            print(f"{sender.name} most often replies {first_replied_name} ({first_number_of_replies} times)", end="")
        if second_number_of_replies > 0:
            print(f", {second_replied_name} ({second_number_of_replies} times)", end="")
        if third_number_of_replies > 0:
            print(f", {third_replied_name} ({third_number_of_replies} times)", end="")
        print()


@statistic(name="most often replied by")
def print_most_often_replies_to(chat: Chat) -> None:
    replies_by_users = _get_replies_by_users(chat)
    replies_to: Dict[User, List[Tuple[User, int]]] = dict()
    for sender in replies_by_users:
        for replied_user in replies_by_users[sender]:
            if replied_user not in replies_to:
                replies_to[replied_user] = []
            for i in range(3):
                if len(replies_to[replied_user]) == i:
                    replies_to[replied_user].append((sender, replies_by_users[sender][replied_user]))
                    break
                elif replies_by_users[sender][replied_user] > replies_to[replied_user][i][1]:
                    replies_to[replied_user][i] = (sender, replies_by_users[sender][replied_user])
                    break
    for replied_user in replies_by_users:
        if replied_user not in replies_to:
            print(f"Nobody replied to {replied_user.name}")
        else:
            print(f"{replied_user.name} was most often replied by ", end="")
            for (sender, number_of_replies) in replies_to[replied_user][:-1]:
                print(f"{sender.name} ({number_of_replies} times), ", end="")
            print(f"{replies_to[replied_user][-1][0].name} ({replies_to[replied_user][-1][1]} times)")