#!/usr/bin/python3

import json


def main():
    chat_file = open("result.json", "r")
    chat = json.load(chat_file)
    messages_count_by_sender = dict()
    for message in chat["messages"]:
        sender = message["from"]
        if sender in messages_count_by_sender:
            messages_count_by_sender[sender] += 1
        else:
            messages_count_by_sender[sender] = 1

    for sender in messages_count_by_sender:
        print(f"{sender} wrote {messages_count_by_sender[sender]} message(s)")


if __name__ == "__main__":
    main()
