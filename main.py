#!/usr/bin/python3

import argparse
from load_chat import Chat
import statistics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_file", type=open)
    arg = parser.parse_args()

    chat = Chat.load_chat(arg.chat_file)
    statistics.print_messages_count_by_sender(chat)
    statistics.print_total_messages_length_by_sender(chat)
    statistics.print_average_messages_length_by_sender(chat)
    statistics.print_most_often_replies(chat)
    statistics.print_most_often_replies_to(chat)


if __name__ == "__main__":
    main()
