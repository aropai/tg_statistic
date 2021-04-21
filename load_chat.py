from __future__ import annotations
from dataclasses import dataclass
import json
from typing import IO, List


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
    users: List[User]
    messages: List[Message]

    def get_user(self, user_id: int, user_name: str) -> User:
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
    def load_chat(chat_file: IO) -> Chat:
        parsed_chat = json.load(chat_file)
        chat = Chat(name=parsed_chat["name"], users=[], messages=[])
        for message in parsed_chat["messages"]:
            if "from" not in message:
                continue
            sender = chat.get_user(int(message["from_id"]), message["from"])
            chat.messages.append(Message(sender=sender, text=message["text"]))
        return chat
