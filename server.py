from flask import Flask, request, make_response, request, send_file

import db
import api

app = Flask(__name__)

field = {}


@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/<cmd>", methods = ["POST"])
def runApi(cmd):
    out = {"ok":1}
    try:
        print(f"API: {cmd}; JSON: {request.json}")
        d = request.get_json(force=True)
        if hasattr(api,cmd):
            getattr(api,cmd)(d,out)
        else:
            raise Exception("Неизвестная команда API")
    except Exception as e:
        print(e)
        out["ok"] = 0
        out["error"] = str(e)
    return make_response(out, 200)







# @app.route('/game/add_player/<string:id>')
# def CreatePlayer(id: str):
#     uIdent = sqlUser.execute(f"SELECT id, name FROM Players WHERE id='{id}'")
#     if len(uIdent) > 0:
#         uIdent = uIdent[0]
#         pl = Player(str(uIdent[0]), uIdent[1], field)
#         field[pl.Id] = pl.settings
#         print(field)
#         return make_response({'status': 'ok', 'answer': []}, 200)
#     else:
#         return make_response({'status': 'warning', 'answer': ['the player is not found']}, 200)


# @app.route('/game/remove_player/<string:Id>')
# def RemovePlayer(Id: str):
#     field.pop(Id)
#     print(field)
#     return make_response({'status': 'ok', 'answer': []}, 200)


# @app.route('/game/get_info')
# def GetInfo():
#     return make_response({'status': 'ok', 'answer': [field]}, 200)


# @app.route('/game/move_player')
# def PLayerMovement():
#     Id = request.args.get('id')
#     but = request.args.get('button')
#     cd = field[Id]['cords']
#     if but == 'up':
#         cd[1] += 1
#     if but == 'down':
#         cd[1] -= 1
#     if but == 'right':
#         cd[0] += 1
#     if but == 'left':
#         cd[0] -= 1
#     field[Id]['cords'] = cd
#     print(field)
#     return make_response({'status': 'ok', 'answer': []}, 200)


app.run(port=5000)