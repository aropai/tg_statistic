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
    users: list
    messages: list


def load_chat(chat_file):
    parsed_chat = json.load(chat_file)
    chat = Chat(name=parsed_chat["name"], users=[], messages=[])
    for message in parsed_chat["messages"]:
        if "from" not in message:
            continue
        sender = None
        sender_id = int(message["from_id"])
        for user in chat.users:
            if user.id == sender_id:
                sender = user
                break
        if not sender:
            sender = User(name=message["from"], id=sender_id)
            chat.users.append(sender)
        chat.messages.append(Message(sender=sender, text=message["text"]))
    return chat
