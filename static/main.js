const W = 100
const H = 100
const VISIBLE_CELLS = 21;
const cl = console.log

async function api(cmd,data={})
{
	try{
		//let q = data.entries.map(v => v[0]+'='+encodeURIComponent(v[1])).join('&');
		let res = await fetch(`/api/${cmd}`,{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});
		let json = await res.json();
		if(!json.ok)
		{
			if(json.error)throw json.error;
			throw 'Неизвестная ошибка сервера'
		}
		return json;
	}catch(e)
	{
		alert(`Штото пошло не так: ${e}`);
		return null;
	}
}

let objects = []
let map_colors = []
let pos = [95,95]

cl({map_colors})

function initMapColors()
{
	for(let x=0; x < W; x++)
	{
		map_colors[x] = []
		for(let y=0; y < H; y++)
		{
			let avg = 0
			if(x > 0)avg += map_colors[x-1][y]
			if(y > 0)avg += map_colors[x][y-1]
			if(x && y)avg /= 2;
			map_colors[x][y] = Math.round((Math.random()*100)+avg-50)
		}
	}
}

function getObjectAtCoord(x,y)
{
	let res = objects.find(v => (v.coord[0] == +x && v.coord[1] == +y)) 
	return res;
}

function drawMap(center)
{
	let h = ''
	let hvc = Math.floor(VISIBLE_CELLS/2);
	let dx = center[0]-hvc;
	let dy = center[1]-hvc;
	for(let ry=0;ry < VISIBLE_CELLS;ry++)
	{
		let y = ry+dy;
		for(let rx=0;rx < VISIBLE_CELLS;rx++)
		{
			let x = rx+dx;
			let color = (x >= 0 && y >= 0 && x < W && y < H) ? `hsl(${map_colors[x][y]} 40% 80%)` : '#fff'
			let cls = '';
			let o = getObjectAtCoord(x,y);
			
			if(rx==hvc && ry==hvc)
				cls = 'me'
			else if(o)
			{
				if(o.type=='user')
					cls = 'enemy'
				else cls = o.type
			}
			h += `<div style="background-color:${color}" class="${cls}"></div>`
		}
	}
	document.querySelector('.map').innerHTML = h
}




async function updObjects()
{
	let res = await api('get_map_objects');
	//cl({res})
	if(res)objects = res.objects;
	drawMap(pos)
	setTimeout(updObjects,500);
}

function move(dir)
{
	let p = [pos[0]+dir[0], pos[1]+dir[1]]
	if(p[0] < 0)p[0] = 0
	if(p[0] >= W)p[0] = W-1
	if(p[1] < 0)p[1] = 0
	if(p[1] >= W)p[1] = H-1
	if(!getObjectAtCoord(p[0],p[1]))
	{
		pos = p
		drawMap(pos)
	}
	
}