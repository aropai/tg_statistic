from load_chat import Chat


def statistic(name: str) -> None:
    def decorator(function: str) -> None:
        def wrapper(chat: Chat) -> None:
            func = function(chat)
            print("=" * 25 + "  " + name.upper() + "  " + 25 * "=")
            print(func[:-1])
            print("=" * 80, "\n\n")

        return wrapper

    return decorator


def _get_messages_count_by_sender(chat):
    messages_count_by_sender = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in messages_count_by_sender:
            messages_count_by_sender[sender] = 0
        messages_count_by_sender[sender] += 1

    return messages_count_by_sender


def _get_total_messages_length_by_sender(chat):
    total_messages_length_by_sender = dict()
    for message in chat.messages:
        sender = message.sender
        if sender not in total_messages_length_by_sender:
            total_messages_length_by_sender[sender] = 0
        total_messages_length_by_sender[sender] += len(message.text)

    return total_messages_length_by_sender


@statistic(name="number of messages")
def print_messages_count_by_sender(chat):
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    string_to_print: str = ""
    for sender in messages_count_by_sender:
        string_to_print += f"{sender.name} wrote {messages_count_by_sender[sender]} message(s)\n"
    return string_to_print


@statistic(name="total length of messages")
def print_total_messages_length_by_sender(chat):
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    string_to_print: str = ""
    for sender in total_messages_length_by_sender:
        string_to_print += f"{sender.name} wrote {total_messages_length_by_sender[sender]} symbol(s)\n"
    return string_to_print


@statistic(name="average len of message")
def print_average_messages_length_by_sender(chat):
    total_messages_length_by_sender = _get_total_messages_length_by_sender(chat)
    messages_count_by_sender = _get_messages_count_by_sender(chat)
    string_to_print: str = ""
    for sender in messages_count_by_sender:
        average_message_length = round(
            total_messages_length_by_sender[sender] / messages_count_by_sender[sender], 2
        )
        string_to_print += f"The average len of {sender.name}'s message is {average_message_length} symbols\n"
    return string_to_print
