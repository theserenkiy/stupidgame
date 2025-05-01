from flask import Flask, request, make_response, request, send_file

globals()["cache"] = {}

import db
import api
import traceback

from os import system
system("title STUPIDGAME")

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')

field = {}


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/main.js")
def main():
    return send_file("static/main.js")


@app.route("/style.css")
def style():
    return send_file("static/style.css")


@app.route("/api/<cmd>", methods = ["POST"])
def runApi(cmd):
    out = {"ok":1}
    try:
        print(f"API: {cmd}; JSON: {request.json}")
        d = request.get_json(force=True)
        res = None
        if hasattr(api,cmd):
            res = getattr(api,cmd)(d)
        else:
            raise Exception("Неизвестная команда API")
        if res:
            out.update(res)
    except Exception as e:
        print(e, traceback.format_exc(), f"\ncmd:{cmd}")
        out["ok"] = 0
        out["error"] = str(e)
    return make_response(out, 200)



app.run(port=5000)