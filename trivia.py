#!/usr/bin/python3

import requests
import pprint
import html

def HandleMultiple(correct, incorrect):


def main():

    # issue an HTTP PUT transaction to store our data within /keys/requests
    # in this case, PUT created a 'file' called '/requests', with a 'value' of 'http for humans'
    # r is the response code resulting from the PUT
    r = requests.get("https://opentdb.com/api.php?amount=2&difficulty=hard&type=boolean")
    # pretty print the json in the response
    #pprint.pprint(r.json()['results'])

    for q in r.json()['results']:
        print(html.unescape(q['question']))
        if q['type'] == 'boolean':
            print("(True/False)")
        a = input()
        if a.lower() == q['correct_answer'].lower():
            print("\n---You got it---\n")
        else:
            print("\n---Wrong---\n")

    print('******')

if __name__ == "__main__":
    main()

