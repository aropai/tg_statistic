#!/usr/bin/python3

from dataclasses import dataclass
import json


@dataclass(frozen=True)
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
        found_user = None
        for user in self.users:
            if user.id == user_id:
                found_user = user
                break
        if not found_user:
            found_user = User(name=user_name, id=user_id)
            self.users.append(found_user)
        return found_user

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
