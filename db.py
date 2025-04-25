import sqlite3

class DB:

	def __init__(self,name):
		self.name = name
		self.conn = sqlite3.connect(f"db/{name}.db", check_same_thread=False)
		self.conn.row_factory = sqlite3.Row
		self.cursor = self.conn.cursor()
		with open(f"sql/{name}.sql") as c:
			self.execute(c.read())

	def execute(self, query, vars=[]):
		self.cursor.execute(query, vars)
		self.conn.commit()
	
	def selectOne(self, query, vars=[]):
		self.cursor.execute(query, vars)
		return self.cursor.fetchone()
	
	def select(self, query, vars=[]):
		self.cursor.execute(query, vars)
		return self.cursor.fetchall()
	
	def insert(self, vardict):
		kk = vardict.keys()
		keys = ", ".join([f"`{k}`" for k in kk])
		value_qs = ("?,"*len(kk))[0:-1]
		q = f"INSERT INTO `{self.name}` ({keys}) VALUES ({value_qs})"
		self.cursor.execute(q,list(vardict.values()))
		self.conn.commit()
		return self.cursor.lastrowid
	
	def update(self, vardict, cond_id=None):
		if not cond_id: 
			raise Exception(f"Cannot update {self.name} without condition")
		pairs = ",".join([f"`{k}`=?" for k in vardict])
		q = f"UPDATE {self.name} SET {pairs} WHERE id=?"
		self.cursor.execute(q,list(vardict.values())+[cond_id])
		self.conn.commit()

	
