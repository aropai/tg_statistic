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

    def get_user(self, user_id, user_name):
        user = None
        for other_user in self.users:
            if other_user.id == user_id:
                user = other_user
                break
        if not user:
            user = User(name=user_name, id=user_id)
            self.users.append(user)
        return user


    @staticmethod
    def load_chat(chat_file):
        parsed_chat = json.load(chat_file)
        chat = Chat(name=parsed_chat["name"], users=[], messages=[])
        for message in parsed_chat["messages"]:
            if "from" not in message:
                continue
            sender = chat.get_user(int(message["from_id"]), message["from"])
            chat.messages.append(Message(sender=sender, text=message["text"]))
        return chat
