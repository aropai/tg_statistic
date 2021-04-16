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
    users: [User]
    messages: [Message]


def load_chat(chat_file):
    parsed_chat = json.load(chat_file)
    chat = Chat(name=parsed_chat["name"], users=[], messages=[])
    for message in parsed_chat["messages"]:
        if "from" not in message:
            continue
        sender = None
        for user in chat.users:
            if user.id == int(message["from_id"]):
                sender = user
                break
        if not sender:
            sender = User(name=message["from"], id=int(message["from_id"]))
            chat.users.append(sender)
        chat.messages.append(Message(sender=sender, text=message["text"]))
    return chat
