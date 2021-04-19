#!/usr/bin/python3

import json
import argparse
from load_chat import Chat
import statistics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_file", type=open)
    arg = parser.parse_args()

    chat = Chat.load_chat(arg.chat_file)
    statistics.amount_of_messages(chat)
    statistics.full_len_of_messages(chat)
    statistics.average_len_of_message(chat)


if __name__ == "__main__":
    main()
