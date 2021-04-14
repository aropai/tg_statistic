#!/usr/bin/python3

import json

def main():
    fin = open("result.json", "r")
    chat = json.load(fin)
    count_messages = dict()
    for message in chat["messages"]:
        if message["from"] in count_messages:
            count_messages[message["from"]] += 1
        else:
            count_messages[message["from"]] = 1

    for name in count_messages:
        print("{} wrote {} message(s)".format(name, count_messages[name]))

if __name__ == "__main__":
    main()
