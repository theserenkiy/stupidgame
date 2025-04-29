from db import DB

players_db = DB("players")

def listPlayers():
    res = [dict(p) for p in players_db.select("SELECT * FROM players")]
    print(res)
    return res


if __name__ == '__main__':
    listPlayers()