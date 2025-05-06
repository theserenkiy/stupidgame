import sqlite3
from util import dotdict
from threading import Lock, Timer
import lib
import json

lock = Lock()

class DB:

	def __init__(self,name):
		print(f"Init database {name}")
		self.name = name
		self.locked = 0
		self.need_commit = 0
		self.conn = sqlite3.connect(f"db/{name}.db", check_same_thread=False)
		self.conn.row_factory = sqlite3.Row
		self.cursor = self.conn.cursor()
		self.doCommit()
		with open(f"sql/{name}.sql") as c:
			self.execute(c.read())

	def lock(self):
		lock.acquire(True)
		self.locked = 1

	def unlock(self):
		if not self.locked:
			return
		lock.release()
		self.locked = 0

	def execute(self, query, vars=[]):
		try:
			if not self.locked:
				lock.acquire(True)
			self.cursor.execute(query, vars)
		finally:
			if not self.locked:
				lock.release()

		return self.cursor
	
	def commit(self):
		self.need_commit = 1

	def doCommit(self):
		if self.need_commit:
			print("doCommit")
			self.conn.commit()
			self.need_commit = 0
		tim = Timer(1, self.doCommit)
		tim.start()
		
	
	def selectOne(self, query, vars=[]):
		self.execute(query, vars)
		return dotdict(dict(self.cursor.fetchone()))
	
	def select(self, query, vars=[]):
		self.execute(query, vars)
		return self.cursor.fetchall()
	
	def insert(self, vardict):
		vardict["updated"] = lib.time_ms()
		kk = vardict.keys()
		keys = ", ".join([f"`{k}`" for k in kk])
		value_qs = ("?,"*len(kk))[0:-1]
		q = f"INSERT INTO `{self.name}` ({keys}) VALUES ({value_qs})"
		self.execute(q,list(vardict.values()))
		self.commit()
		return self.cursor.lastrowid
	
	def update(self, vardict, cond, condvars=[]):
		print(vardict)
		if not cond: 
			raise Exception(f"Cannot update {self.name} without condition")
		vardict["updated"] = lib.time_ms()
		pairs = ",".join([f"`{k}`=?" for k in vardict])
		q = f"UPDATE {self.name} SET {pairs} WHERE {cond}"
		self.execute(q,list(vardict.values())+condvars)
		self.commit()

	def delete(self, cond, condvars=[]):
		self.execute(f"DELETE FROM {self.name} WHERE {cond}",condvars)
		self.commit()

	def c_selectId(self, id, fields=None):
		flist = ",".join(fields) if fields else '*'
		return self.selectOne(f"SELECT {flist} FROM {self.name} WHERE id=?",[id])
	
	def c_insert(self,vardict):
		self.prepVarDict(vardict)
		return self.insert(vardict)
	
	def c_updateId(self,vardict,id):
		self.prepVarDict(vardict)
		return self.update(vardict,'id=?',[id])
	
	def c_selectMany(self,conditions,fields=None):
		flist = ",".join([f"`{f}`" for f in fields]) if fields else '*'
		cond = " AND ".join([f"`{k}`=?" for k in conditions.keys()])
		q = f"SELECT {flist} FROM {self.name} WHERE {cond}"
		# print(q,conditions.values())
		return self.select(q,list(conditions.values()))

	def prepVarDict(self,vardict):
		for k in vardict:
			val = vardict[k]
			if type(val) is list or type(val) is dict:
				vardict[k] = json.dumps(val)