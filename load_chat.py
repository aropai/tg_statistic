from __future__ import annotations
from dataclasses import dataclass
import json
from typing import IO, List, Optional


@dataclass(frozen=True)
class User:
    name: str
    id: int


@dataclass
class Message:
    sender: User
    id: int
    reply_to_message_id: Optional[int]
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

    def get_message(self, message_id: int) -> Message:
        left_border = 0
        right_border = len(self.messages)
        while right_border - left_border != 1:
            m = (right_border + left_border) // 2
            if self.messages[m].id <= message_id:
                left_border = m
            else:
                right_border = m
        return self.messages[left_border]


    @staticmethod
    def load_chat(chat_file: IO) -> Chat:
        parsed_chat = json.load(chat_file)
        chat = Chat(name=parsed_chat["name"], users=[], messages=[])
        for message in parsed_chat["messages"]:
            if "from" not in message:
                continue
            sender = chat.get_user(int(message["from_id"]), message["from"])
            new_message = Message(sender=sender, id=message["id"], reply_to_message_id=None, text=message["text"])
            if "reply_to_message_id" in message:
                new_message.reply_to_message_id = int(message["reply_to_message_id"])
            chat.messages.append(new_message)
        return chat
