#!/usr/bin/python3


def count_messages(chat):
    count_messages_by_sender = dict()
    for message in chat.messages:
        user = message.sender
        if user in count_messages_by_sender:
            count_messages_by_sender[user] += 1
        else:
            count_messages_by_sender[user] = 1

    return count_messages_by_sender


def count_len_of_messages(chat):
    count_len_by_sender = dict()
    for message in chat.messages:
        user = message.sender
        if user in count_len_by_sender:
            count_len_by_sender[user] += len(message.text)
        else:
            count_len_by_sender[user] = len(message.text)

    return count_len_by_sender


def amount_of_messages(chat):
    count_messages_by_sender = count_messages(chat)
    for user in count_messages_by_sender:
        print(f"{user.name} wrote {count_messages_by_sender[user]} message(s)")


def full_len_of_messages(chat):
    count_len_by_sender = count_len_of_messages(chat)
    for user in count_len_by_sender:
        print(f"{user.name} wrote {count_len_by_sender[user]} symbol(s)")


def average_len_of_message(chat):
    count_len_by_sender = count_len_of_messages(chat)
    count_messages_by_sender = count_messages(chat)
    for user in count_messages_by_sender:
        print(f"The average len of {user.name}'s message is {round(count_len_by_sender[user] / count_messages_by_sender[user], 2)} symbols")
