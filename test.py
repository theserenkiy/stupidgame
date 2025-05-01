import json
def foo(vardict):
	for k in vardict:
		val = vardict[k]
		if type(val) is list or type(val) is dict:
			vardict[k] = json.dumps(val)

vardict = {"a":[1,2,3],"b": 12, "c": "hui"}

foo(vardict)

print(vardict)
