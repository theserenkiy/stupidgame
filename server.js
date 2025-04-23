const port = parseInt(process.argv[2]);
if(isNaN(port))
{
	console.log('Missing/incorrect port (1st argument)');
	process.exit();
}

const cl = console.log;

import express from 'express';
import bodyParser from 'body-parser';
import fs from 'fs';
import lib from './lib';

const users = lib.readUsers()
const user_tokens = {}



const field_objects = [
	{type: 'user', coord: [97,97]}	
	// {type: 'dick', coord: [12,10]}
]

let randcoords = []
function randCoord()
{
	let c;
	while(1)
	{
		c = []
		for(let i=0;i < 2;i++)
			c.push(Math.floor(Math.random()*100))

		if(randcoords.find(v => v[0]==c[0] && v[1]==c[1]))
			continue
		break;
	}
	
	randcoords.push(c)
	return c
}

for(let u of users)
{
	field_objects.push({
		type: 'user',
		id: u.id,
		coord: randCoord()
	})
}

let types = ['shit','apple','axe','beer']
for(let i=0; i < 150; i++)
{
	field_objects.push({
		type: types[Math.floor(Math.random()*4)],
		coord: randCoord()
	})
}

;(async() => {
let app = express();
app.use(express.static('static'));
app.use(bodyParser.json());
app.get('/',(req,res) => {
	res.send(fs.readFileSync('index.html','utf-8'));
});
app.post('/api/:cmd',async (req,res)=>{
	//cl('BODY',req.body)
	let out = {ok:1}
	let b = req.body;
	try{
		switch(req.params.cmd)
		{
			case 'login':
				if(!users.find(v => v.id == +b.id))
					throw 'Неизвестный пользователь'
				break;
			case 'user_step':
				
				break;
				
			case 'get_map_objects':
				out.objects = field_objects;
				break;
			default:
				throw 'Неизвестная команда'
		}
	}catch(e)
	{
		out = {ok:0, error:e+''}
	}
	res.json(out)
})
 q
app.listen(port,()=>{cl('Serving on port '+port)});	

cl(lib.genToken(32))

})()
