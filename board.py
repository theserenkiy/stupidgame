import map
from db import DB

boards = DB('boards')
maps = DB('maps')

def createBoard(map_id):
    m = map.getMap(map_id)
    res = boards.insert({"map_id":map_id, "w":m['w'], "h":m['h']})
    # print(res)

def initBoard(id):
    b = boards.selectOne("SELECT map_id,w,h FROM boards WHERE id=?",[id])
    if not b:
        raise Exception(f"Board {id} not found")
    m = maps.selectOne("SELECT * FROM maps WHERE id=?",[b['map_id']])
    return {"landscape": m["landscape"], "w":b["w"], "h":b["h"]}


if __name__ == "__main__":
    createBoard(1)