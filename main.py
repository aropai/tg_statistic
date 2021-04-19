#!/usr/bin/python3

import argparse
from load_chat import Chat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_file", type=open)
    arg = parser.parse_args()

    chat = Chat.load_chat(arg.chat_file)
    messages_count_by_sender = dict()
    for message in chat.messages:
        user = message.sender
        if user in messages_count_by_sender:
            messages_count_by_sender[user] += 1
        else:
            messages_count_by_sender[user] = 1

    for user in messages_count_by_sender:
        print(f"{user.name} wrote {messages_count_by_sender[user]} message(s)")


if __name__ == "__main__":
    main()
