#!/usr/bin/python3

from dataclasses import dataclass
import json

@dataclass
class User:
    name: str
    id: int

@dataclass
class Message:
    sender: User
    text: str

@dataclass
class Chat:
    name: str
    users: []
    messages: []


def load_chat(chat_file):
    parsed_chat = json.load(chat_file)
    chat = Chat(parsed_chat["name"], [User(parsed_chat["name"], int(parsed_chat["id"]))], [])
    for message in parsed_chat["messages"]:
        if "from" not in message:
            continue
        sender = User(message["from"], int(message["from_id"]))
        if sender not in chat.users:
            chat.users.append(sender)
        if sender == chat.users[0]:
            chat.messages.append(Message(chat.users[0], message["text"]))
        else:
            chat.messages.append(Message(chat.users[1], message["text"]))
    return chat
