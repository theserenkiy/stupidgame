import sqlite3

class DB:
	def __init__(self,name):
		self.name = name
		self.dataBase = sqlite3.connect(f"db/{name}.db", check_same_thread=False)
		self.cursor = self.dataBase.cursor()
		with open(f"sql/{name}.sql") as c:
			self.execute(c.read())

	def execute(self, query, vars=[]):
		# print(query,vars)
		self.cursor.execute(query, vars)
		self.dataBase.commit()
		colnames = [x[0] for x in (self.cursor.description or [])]
		rows = [dict(zip(colnames,row)) for row in self.cursor.fetchall()]
		return rows
	
	def insert(self, vardict):
		kk = vardict.keys()
		keys = ", ".join([f"`{k}`" for k in kk])
		value_qs = ("?,"*len(kk))[0:-1]
		q = f"INSERT INTO `{self.name}` ({keys}) VALUES ({value_qs})"
		# print(q)
		self.execute(q,list(vardict.values()))
		return self.cursor.lastrowid
	
	def update(self, vardict, cond_id=None):
		if not cond_id: 
			raise Exception(f"Cannot update {self.name} without condition")
		pairs = ",".join([f"`{k}`=?" for k in vardict])
		q = f"UPDATE {self.name} SET {pairs} WHERE id=?"
		# print(q)
		return self.execute(q,list(vardict.values())+[cond_id])
	
