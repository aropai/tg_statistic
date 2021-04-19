#!/usr/bin/python3


def _get_messages_count_by_sender(chat):
    messages_count_by_sender = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in messages_count_by_sender:
            messages_count_by_sender[sender] = 0
        messages_count_by_sender[sender] += 1

    return messages_count_by_sender


def _get_total_messages_length_by_sender(chat):
    total_messages_length_by_sender = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in total_messages_length_by_sender:
            total_messages_length_by_sender[sender] = 0
        total_messages_length_by_sender[sender] += len(message.text)

    return total_messages_length_by_sender


def print_messages_count_by_sender(chat):
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    for sender in messages_count_by_sender:
        print(f"{sender.name} wrote {messages_count_by_sender[sender]} message(s)")


def print_total_messages_length_by_sender(chat):
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    for sender in total_messages_length_by_sender:
        print(f"{sender.name} wrote {total_messages_length_by_sender[sender]} symbol(s)")


def print_average_messages_length_by_sender(chat):
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    for sender in messages_count_by_sender:
        average_message_length = round(
            total_messages_length_by_sender[sender] / messages_count_by_sender[sender], 2
        )
        print(f"The average len of {sender.name}'s message is {average_message_length} symbols")
