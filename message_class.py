#!/usr/bin/python3

from dataclasses import dataclass
import json

@dataclass
class Message:
    sender: str
    text: str


def parse_chat(chat_file):
    chat = json.load(chat_file)
    messages = []
    for message in chat["messages"]:
        if "from" not in message:
            continue
        messages.append(Message(message["from"], message["text"]))
    return messages