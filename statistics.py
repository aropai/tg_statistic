from load_chat import Chat, User, Message
from typing import Dict, Callable, List, Tuple
import regex

BORDERS_LENGTH = 120
WORD_REGEX = regex.compile(r"((\p{L}+-\p{L}+)|(\p{L}+))")
FORBIDDEN_WORDS = ["то", "меж", "ага", "прежде", "нежели", "поперёк", "накануне", "сзади", "уж", "сбоку", "хоть", 
                   "кроме", "ежели", "пока", "ну", "снизу", "во", "но", "сквозь", "по", "ли", "буде", "кабы", "нет", 
                   "если", "вследствие", "под", "для", "ото", "же", "в", "возле", "вместо", "чуть", "вне", "дабы", 
                   "посредством", "угу", "подле", "абы", "наискось", "да", "изнутри", "уже", "поверх", "до", "вокруг", 
                   "внутри", "тоже", "из-под", "из-за", "коли", "коль", "ни", "словно", "свыше", "бы", "аж", "к", 
                   "после", "либо", "над", "чтобы", "позади", "притом", "через", "впереди", "ведь", "лишь", "итак", 
                   "разве", "ибо", "от", "причем", "сиречь", "при", "чтоб", "и", "без", "у", "вблизи", "покамест", 
                   "поскольку", "сверху", "б", "вдоль", "посреди", "наподобие", "почти", "даже", "покуда", "насчёт", 
                   "якобы", "из", "ввиду", "между", "с", "внутрь", "не", "против", "перед", "среди", "помимо", "близ", 
                   "вопреки", "ради", "ль", "хотя", "а", "на", "едва", "около", "посредине", "или", "ан", "ой", "хм",
                   "за"]



def statistic(name: str) -> Callable[[Callable[[Chat], None]], Callable[[Chat], None]]:
    def decorator(statistic_function: Callable[[Chat], None]) -> Callable[[Chat], None]:
        def wrapper(chat: Chat) -> None:
            print(f" {name.upper()} ".center(BORDERS_LENGTH, "="))
            statistic_function(chat)
            print("=" * BORDERS_LENGTH)
            print()

        return wrapper

    return decorator


def _get_messages_count_by_sender(chat: Chat) -> Dict[User, int]:
    messages_count_by_sender: Dict[User, int] = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in messages_count_by_sender:
            messages_count_by_sender[sender] = 0
        messages_count_by_sender[sender] += 1

    return messages_count_by_sender


def _get_total_messages_length_by_sender(chat: Chat) -> Dict[User, int]:
    total_messages_length_by_sender: Dict[User, int] = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in total_messages_length_by_sender:
            total_messages_length_by_sender[sender] = 0
        total_messages_length_by_sender[sender] += len(message.text)

    return total_messages_length_by_sender


def _sorted_by_value(value_by_sender: Dict[User, int]) -> List[User]:
    return sorted(value_by_sender, key=lambda sender: -value_by_sender[sender])


@statistic(name="number of messages")
def print_messages_count_by_sender(chat: Chat) -> None:
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    for sender in _sorted_by_value(messages_count_by_sender):
        print(f"{sender.name:20} wrote {messages_count_by_sender[sender]:<6} message(s)")


@statistic(name="total length of messages")
def print_total_messages_length_by_sender(chat: Chat) -> None:
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    for sender in _sorted_by_value(total_messages_length_by_sender):
        print(f"{sender.name:20} wrote {total_messages_length_by_sender[sender]:<8} symbol(s)")


@statistic(name="average len of message")
def print_average_message_length_by_sender(chat: Chat) -> None:
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    average_message_length_by_sender: Dict[User, int] = dict()
    for sender in total_messages_length_by_sender:
        average_message_length_by_sender[sender] = int(
            100 * total_messages_length_by_sender[sender] / messages_count_by_sender[sender])
    belongness = "\'s"
    for sender in _sorted_by_value(average_message_length_by_sender):
        print(
            f"The average len of {sender.name + belongness:22} message is {average_message_length_by_sender[sender] / 100:<6} symbols"
        )


def _get_replies_count_by_users(chat: Chat) -> Dict[User, Dict[User, int]]:
    replies_count_by_users: Dict[User, Dict[User, int]] = dict()
    for message in chat.messages:
        if not message.reply_to_message_id or message.reply_to_message_id not in chat.message_by_id:
            continue
        sender = message.sender
        replied_message = chat.message_by_id[message.reply_to_message_id]
        if sender not in replies_count_by_users:
            replies_count_by_users[sender] = dict()
        if replied_message.sender not in replies_count_by_users[sender]:
            replies_count_by_users[sender][replied_message.sender] = 0
        replies_count_by_users[sender][replied_message.sender] += 1

    return replies_count_by_users


def _get_replies_count_to_users(chat: Chat) -> Dict[User, Dict[User, int]]:
    replies_count_to_users: Dict[User, Dict[User, int]] = dict()
    for message in chat.messages:
        if not message.reply_to_message_id or message.reply_to_message_id not in chat.message_by_id:
            continue
        sender = message.sender
        replied_message = chat.message_by_id[message.reply_to_message_id]
        if replied_message.sender not in replies_count_to_users:
            replies_count_to_users[replied_message.sender] = dict()
        if sender not in replies_count_to_users[replied_message.sender]:
            replies_count_to_users[replied_message.sender][sender] = 0
        replies_count_to_users[replied_message.sender][sender] += 1

    return replies_count_to_users


def _get_top_replies(replies_count: Dict[User, int]) -> List[Tuple[User, int]]:
    top_replies = list(replies_count.items())
    top_replies.sort(key=lambda x: -x[1])
    top_replies = top_replies[:3]
    return top_replies


def _sorted_by_username(users_replies: List[User]) -> List[User]:
    return sorted(users_replies, key=lambda user: user.name.lower())


@statistic(name="most often replies")
def print_most_often_replies(chat: Chat) -> None:
    replies_count_by_users = _get_replies_count_by_users(chat)
    for sender in _sorted_by_username(chat.users):
        if sender not in replies_count_by_users:
            top_replies = []
        else:
            top_replies = _get_top_replies(replies_count_by_users[sender])
        if len(top_replies) == 0:
            print(f"{sender.name:20} replies nobody")
        else:
            print(
                f"{sender.name:20} most often replies",
                ", ".join([f"{entry[0].name} ({entry[1]} times)" for entry in top_replies])
            )


@statistic(name="most often replied by")
def print_most_often_replies_to(chat: Chat) -> None:
    replies_count_to_users = _get_replies_count_to_users(chat)
    for replied_sender in _sorted_by_username(chat.users):
        if replied_sender not in replies_count_to_users:
            top_replies = []
        else:
            top_replies = _get_top_replies(replies_count_to_users[replied_sender])
        if len(top_replies) == 0:
            print(f"{replied_sender.name:20} was replied by nobody")
        else:
            print(
                f"{replied_sender.name:20} was most often replied by",
                ", ".join([f"{entry[0].name} ({entry[1]} times)" for entry in top_replies])
            )


def _parse_string_to_words(text: str) -> List[str]:
    matches = WORD_REGEX.findall(text)
    words = []
    for match in matches:
        words.append(match[0])
    return words


def _parse_message_to_words(message: Message) -> List[str]:
    if isinstance(message.text, str):
        return _parse_string_to_words(message.text)
    assert isinstance(message.text, list)
    words: List[str] = []
    for text_component in message.text:
        if isinstance(text_component, str):
            words += _parse_string_to_words(text_component)
        if "text" not in text_component:
            continue
        if "type" in text_component and text_component["type"] == "link":
            words.append("<link>")
        else:
            words += _parse_string_to_words(text_component["text"])
    return words


@statistic(name="most often used words")
def print_most_often_used_words(chat: Chat) -> None:
    words_count_by_user: Dict[User, Dict[str, int]] = dict()
    for message in chat.messages:
        sender = message.sender
        words = _parse_message_to_words(message)
        if sender not in words_count_by_user:
            words_count_by_user[sender] = dict()
        for word in words:
            word = word.lower()
            if word in FORBIDDEN_WORDS:
                continue
            if word not in words_count_by_user[sender]:
                words_count_by_user[sender][word] = 0
            words_count_by_user[sender][word] += 1
    for sender in _sorted_by_username(chat.users):
        if sender not in words_count_by_user:
            print(f"{sender.name} writes nothing")
        else:
            top_words = list(words_count_by_user[sender].items())
            top_words.sort(key=lambda x: -x[1])
            top_words = top_words[:10]
            print(f"{sender.name} most often writes", ", ".join([f"{word[0]} ({word[1]} times)" for word in top_words]))
