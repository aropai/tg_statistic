#!/usr/bin/python3

import json

def main():
    fin = open("result.json", "r")
    js = json.load(fin)
    cnt_msg = dict()
    for message in js["messages"]:
        if message["from"] in cnt_msg.keys():
            cnt_msg[message["from"]] += 1
        else:
            cnt_msg[message["from"]] = 1

    for name in cnt_msg.keys():
        print("{} wrote {} message(s)".format(name, cnt_msg[name]))

if __name__ == "__main__":
    main()
