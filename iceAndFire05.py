#!/usr/bin/python3
"""Alta3 Research - Exploring OpenAPIs with requests"""
# documentation for this API is at
# https://anapioficeandfire.com/Documentation

import requests
import pprint

AOIF_CHAR = "https://www.anapioficeandfire.com/api/characters/"

def main():
        ## Ask user for input
        got_charToLookup = input("Pick a number between 1 and 1000 to return info on a GoT character! " )

        ## Send HTTPS GET to the API of ICE and Fire character resource
        gotresp = requests.get(AOIF_CHAR + got_charToLookup)

        ## Decode the response
        got_dj = gotresp.json()
        pprint.pprint(got_dj)

        house_apis = got_dj['allegiances']
        print(f'{got_dj["name"]} belongs to the following houses:\n')
        for house_api in house_apis:
            got_house = requests.get(house_api).json()
            pprint.pprint(got_house['name'])

        print(f'\n\n{got_dj["name"]} appears in the following books:\n')
        for book_api in got_dj['books']:
            got_book = requests.get(book_api).json()
            pprint.pprint(got_book['name'])

        for book_api in got_dj['povBooks']:
            got_book = requests.get(book_api).json()
            pprint.pprint(got_book['name'])

if __name__ == "__main__":
        main()

