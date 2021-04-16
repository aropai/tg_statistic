#!/usr/bin/python3

import json
import argparse
from load_chat import Chat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_file", type=open)
    arg = parser.parse_args()

    chat = Chat.load_chat(arg.chat_file)
    messages_count_by_sender = dict()
    for message in chat.messages:
        name = message.sender.name
        if name in messages_count_by_sender:
            messages_count_by_sender[name] += 1
        else:
            messages_count_by_sender[name] = 1

    for name in messages_count_by_sender:
        print(f"{name} wrote {messages_count_by_sender[name]} message(s)")


if __name__ == "__main__":
    main()
