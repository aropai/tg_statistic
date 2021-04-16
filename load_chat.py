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

    def find_sender(self, sender_id, sender_name):
        sender = None
        for user in self.users:
            if user.id == sender_id:
                sender = user
                break
        if not sender:
            sender = User(name=sender_name, id=sender_id)
            self.users.append(sender)
        return sender


    @staticmethod
    def load_chat(chat_file):
        parsed_chat = json.load(chat_file)
        chat = Chat(name=parsed_chat["name"], users=[], messages=[])
        for message in parsed_chat["messages"]:
            if "from" not in message:
                continue
            sender = chat.find_sender(int(message["from_id"]), message["from"])
            chat.messages.append(Message(sender=sender, text=message["text"]))
        return chat
