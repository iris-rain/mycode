#!/usr/bin/env python3
import json

from flask import Flask
from flask import session
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

app = Flask(__name__)
app.secret_key = "any random string"

#grab the value 'username'
@app.route("/login", methods=["GET", "POST"])
def login():
       ## if you sent us a POST because you clicked the login button
   if request.method == "POST":

      ## request.form["xyzkey"]: use indexing if you know the key exists
      ## request.form.get("xyzkey"): use get if the key might not exist
      session["username"] = request.form.get("username")
      return redirect(url_for("showhosts"))

   ## return this HTML data if you send us a GET
   return """
   <form action = "" method = "post">
      <p><input type = text name = username></p>
      <p><input type = submit value = Login></p>
   </form>
  """

@app.route("/logout")
def logout():
   # remove the username from the session if it is there
   session.pop("username", None)
   return redirect(url_for("showhosts"))

@app.route("/")
@app.route("/showhosts")
def showhosts():
    # render the jinja template "helloname.html"
    # apply the value of username for the var name
    with open("hostnames.json", "r") as hostinfos:
        hoststring = hostinfos.read()

    hosts = json.loads(hoststring) 
    return render_template("challenge.html", groups= hosts)

@app.route("/addhost", methods=["GET", "POST"])
def addhost():
    if "username" not in session:
        return "You are not logged in <br><a href = '/login'></b>" + \
      "click here to log in</b></a>"
    if request.method == "POST":
        hostname = request.form.get("hostname")
        ip = request.form.get("ip")
        fqdn = request.form.get("fqdn")
        y = {"hostname": hostname, "ip": ip, "fqdn": fqdn}
        with open("hostnames.json", "r+") as file:
          # First we load existing data into a dict.
            file_data = json.load(file)
        # Join new_dat3a with file_data
            file_data.append(y)
        # Sets file's current position at offset.
            file.seek(0)
        # convert back to json.
            json.dump(file_data, file, indent = 4)

        return redirect(url_for("showhosts"))

    return render_template("addhost.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224)

