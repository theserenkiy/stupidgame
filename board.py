import map
from db import DB

boards = DB('boards')

def createBoard(map_id):
    m = map.getMap(map_id)
    res = boards.insert({"map_id":map_id, "w":m.w, "h":m.h})
    print(res)



if __name__ == "__main__":
    createBoard(123)