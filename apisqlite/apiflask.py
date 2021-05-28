#!/usr/bin/env python3
""" Author: RZFeeser || Alta3 Research
Gather data returned by various APIs published on OMDB, and cache in a local SQLite DB
"""

import json
import sqlite3
import requests

from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import abort
from flask import session

app = Flask(__name__)
app.secret_key = "any random string"

# Define the base URL
OMDBURL = "http://www.omdbapi.com/?"

@app.route("/")
def index():
    mykey = harvestkey()
    print(mykey)
    session["mykey"] = mykey
    return render_template("OMDBSearch.html")

@app.route("/searchstring", methods=["GET", "POST"])
def searchstring():
    if "mykey" not in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        sv = request.form.get("searchstring")
        mykey = session["mykey"]
        resp = movielookup(mykey, sv)
        if resp:
            # display the results
            resp = resp.get("Search")
            print(resp)
            # write the results into the database
            trackmeplease(resp)
            return redirect(url_for("index"))
        else:
                print("That search did not return any results.")
    else:
        return render_template("OMDBSearchstring.html")

# search for all movies containing string
def movielookup(mykey, searchstring):
    """Interactions with OMDB API
       mykey = omdb api key
       searchstring = string to search for"""
    try:
        # begin constructing API
        api = f"{OMDBURL}apikey={mykey}&s={searchstring}"

        ## open URL to return 200 response
        resp = requests.get(api)
        ## read the file-like object decode JSON to Python data structure
        return resp.json()
    except:
        return False

# search for all movies containing string
def movielookup2(mykey, searchstring, searchtype):
    """Interactions with OMDB API
       mykey = omdb api key
       searchstring = string to search for"""
    try:
        # begin constructing API
        api = f"{OMDBURL}apikey={mykey}&s={searchstring}&type={searchtype}"

        ## open URL to return 200 response
        resp = requests.get(api)
        ## read the file-like object decode JSON to Python data structure
        return resp.json()
    except:
        return False

def trackmeplease(datatotrack):
    conn = sqlite3.connect('mymovie.db')
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS MOVIES (TITLE TEXT PRIMARY KEY NOT NULL, YEAR INT  NOT NULL);''')

        # loop through the list of movies that was passed in
        for data in datatotrack:
            # in the line below, the ? are examples of "bind vars"
            # this is best practice, and prevents sql injection attacks
            # never ever use f-strings or concatenate (+) to build your executions
            conn.execute("INSERT INTO MOVIES (TITLE,YEAR) VALUES (?,?)",(data.get("Title"), data.get("Year")))
            conn.commit()

        print("Database operation done")
        conn.close()
        return True
    except:
        return False

# Read in API key for OMDB
def harvestkey():
    with open("/home/student/omdb.key") as apikeyfile:
        return apikeyfile.read().rstrip("\n") # grab the api key out of omdb.key

def printlocaldb():
    pass
    #cursor = conn.execute("SELECT * from MOVIES")
    #for row in cursor:
    #    print("MOVIE = ", row[0])
    #    print("YEAR = ", row[1])


def main():

    # read the API key out of a file in the home directory
    mykey = harvestkey()

    # enter a loop condition with menu prompting
    while True:
        # initialize answer
        answer = ""
        while answer == "":
            print("""\n**** Welcome to the OMDB Movie Client and DB ****
            ** Returned data will be written into the local database **
            1) Search for All Movies Containing String
            2) Search for Movies Containing String, and by Type
            99) Exit""")

            answer = input("> ") # collect an answer for testing

        # testing the answer
        if answer in ["1", "2"]:
            # All searches require a string to include in the search
            searchstring = input("Search all movies in the OMDB. Enter search string: ")

            if answer == "1":
                resp = movielookup(mykey, searchstring)
            elif answer == "2":
                searchtype = input("What's the type:")
                resp = movielookup2(mykey, searchstring, searchtype)
                #print("\nSearch by type coming soon!\n") # maybe you can write this code!
                #continue                                 # restart the while loop
            if resp:
                # display the results
                resp = resp.get("Search")
                print(resp)
                # write the results into the database
                trackmeplease(resp)
            else:
                print("That search did not return any results.")

        # user wants to exit
        elif answer == "99":
            print("See you next time!")
            break


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2224)
