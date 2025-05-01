let W = 100
let H = 100
const VISIBLE_CELLS = 11;
const CELL_SIZE = 64;

const INVENTORY_SLOTS = 10;
const INVENTORY_CELL_SIZE = 80
let PLAYER_ID = 4962376
let timediff = 0
let objcfg = {}

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
		if(json.game_error)
			alert(json.game_error)
		if(json.msg)
			alert(json.msg)
		return json;
	}catch(e)
	{
		alert(`Штото пошло не так: ${e}`);
		return null;
	}
}

function getServerTime()
{
	return Date.now()+timediff
}

function initCss()
{
	let invm = Math.ceil(INVENTORY_CELL_SIZE/20)
	let invw = 2*(INVENTORY_CELL_SIZE+invm+invm+2)
	document.querySelector('style.custom').innerHTML = `
	.map {
		width: ${VISIBLE_CELLS*(CELL_SIZE+1)}px;
	}
	.map > div {
		width: ${CELL_SIZE}px;
		height: ${CELL_SIZE}px;
		font-size: ${Math.round(CELL_SIZE/2)}px;
	}
	.inventory {
		width: ${invw}px;
	}
	.inventory > div{
		width: ${INVENTORY_CELL_SIZE}px;
		height: ${INVENTORY_CELL_SIZE}px;
		margin: ${invm}px;
	}
	`
}

let objects = []
let players = []
let landscape = []
let pos = [95,95]

cl({map_colors: landscape})


function getObjectAtCoord(x,y)
{
	let res = objects.find(v => (v.x == +x && v.y == +y)) 
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
			let color = (x >= 0 && y >= 0 && x < W && y < H) ? `hsl(${landscape[x][y]} 40% 80%)` : '#fff'
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
			if(cls)
				cls += ' object'
			h += `<div style="background-color:${color}" class="${cls}"></div>`
		}
	}
	document.querySelector('.map').innerHTML = h;
}


async function updObjects()
{
	let res = await api('get_map_objects');
	//cl({res})
	if(res)objects = res.objects;
	drawMap(pos)
	setTimeout(updObjects,500);
}


let STEPNUM = 0
let lastmove = 0
let last_verified_stepnum = 0
function move(dir)
{
	if(Date.now()-lastmove < 100)
		return;
	lastmove = Date.now() 
	if(STEPNUM-last_verified_stepnum > 5)
		return
	STEPNUM++
	//cl('MOVE',dir);
	(async () => {
		try{
			let d = await api('move',{player_id: PLAYER_ID, dir, stepnum: STEPNUM}) 
			//cl('POS',d.pos)
			last_verified_stepnum = d.stepnum
			if(d.inventory)
			{
				updInventory(d.inventory)
				if(d.objects_removed)
					removeObjects(d.objects_removed)

				pos = d.pos
				drawMap(pos)
			}
			if(d.stepnum == STEPNUM && (pos[0] != d.pos[0] || pos[1] != d.pos[1]))
			{
				pos = d.pos
				drawMap(pos)
			}
		}
		catch(e)
		{
			cl(e)
		}
	})()
	
	let p = [pos[0]+dir[0], pos[1]+dir[1]]
	
	
	if(p[0] < 0)p[0] = 0;
	else if(p[0] >= W)p[0] = W-1;
	if(p[1] < 0)p[1] = 0;
	else if(p[1] >= H)p[1] = H-1;
	
	if(!getObjectAtCoord(p[0],p[1]))
	{
		pos = p
		drawMap(pos)
	}
}

function initInventory()
{
	document.onclick = ev => console.log('win click')
	h = ''
	for(let i=0; i < INVENTORY_SLOTS; i++)
	{
		h += `<div class="slot" data-num="${i}" draggable="true"><div></div></div>`
	}
	document.querySelector(".inventory").innerHTML = h
	for(let slot of [...document.querySelectorAll(".inventory .slot")])
	{
		slot.onclick = async () => {
			res = await api('use_object',{player_id:PLAYER_ID, slotnum: +slot.dataset.num})
			if(res.inventory)
				updInventory(res.inventory)
		}
		slot.oncontextmenu = ev => {
			ev.preventDefault()
			cl('context menu')
			invShowMenu(slot)
		}
	}
}

function invShowMenu(slot)
{
	let rect = slot.getBoundingClientRect()
	cl(rect)
	let menu_el = document.querySelector('.inv_context');
	menu_el.style.left = (rect.x+rect.width+4)+'px';
	menu_el.style.top = rect.y+'px';
}

function updInventory(inv)
{
	let slots = [...document.querySelectorAll(".inventory > div")]
	for(let i=0; i < slots.length; i++)
	{
		if(!inv[i])
			break
		let cls = inv[i].type
		if(inv[i].items && inv[i].items.length > 1)
		{
			cls += ' multi'
			slots[i].querySelector('div').innerHTML = inv[i].items.length
		}
			
		slots[i].className = cls
	}
}

function removeObjects(ids)
{
	objects = objects.filter(v => !ids.includes(v.id))
}

async function initGame(board_id)
{
	initInventory()

	let res = await api("init_game",{board_id,player_id:PLAYER_ID})
	W = res.w
	H = res.h
	landscape = JSON.parse(res.landscape)
	pos = res.mycrd
	objects = res.objects

	if(res.player.inventory)
		updInventory(JSON.parse(res.player.inventory))
	// res = await api("init_user")

	objcfg = res.objcfg

	res = await api("timesync")
	timediff = res.time-Date.now()
	cl({timediff})

	initCss()

	drawMap(pos)
	
}