let W = 100
let H = 100
const VISIBLE_CELLS = 11;
const CELL_SIZE = 64;

const INVENTORY_SLOTS = 10;
const INVENTORY_CELL_SIZE = 80
const WEARING_SLOTS = 5
let PLAYER_ID = 2623382
let timediff = 0
let objcfg = {}
let charcfg = {}
let player
let inventory

let popup_msg, popup_inv;

async function api(cmd,data={})
{
	let res = await base_api(cmd,data)
	if(res.game_error)
		msg(res.game_error,1)
	if(res.msg)
		msg(res.msg,1)
	processServerResponse(res)
	return res
}

function processServerResponse(res)
{
	let d = res.inventory || (res.player && res.player.inventory)
	if(d)
		updInventory(prepJson(d))

	d = res.wearing || (res.player && res.player.wearing)
	if(d)
		updWearing(prepJson(d))
}


function msg(s,error=0)
{
	popup_msg.show(s,error ? 'error' : '')
}

function hideMsg()
{
	popup_msg.hide(['error'])
}



function getServerTime()
{
	return Date.now()+timediff
}

function initCss()
{
	let invm = Math.ceil(INVENTORY_CELL_SIZE/20)
	let invw = 2*(INVENTORY_CELL_SIZE+invm+invm+2)
	let styles = `
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
	.inventory > div, .wearing > div{
		width: ${INVENTORY_CELL_SIZE}px;
		height: ${INVENTORY_CELL_SIZE}px;
		margin: ${invm}px;
	}
	`;

	for(let type in objcfg)
	{
		let c = objcfg[type]
		styles += `
		.object.${type}{
			background-image: url('/sprites/${c.icon.sprite}.png');
			background-repeat: no-repeat;
			background-size: 600%;
		}
		.map > div.object.${type}{
			background-position: ${-c.icon.x*CELL_SIZE}px ${-c.icon.y*CELL_SIZE}px;
		}
		.inventory > div.object.${type}, .wearing > div.object.${type}{
			background-position: ${-c.icon.x*INVENTORY_CELL_SIZE}px ${-c.icon.y*INVENTORY_CELL_SIZE}px;
		}
		`
	}
	let charid = 0
	for(let char of charcfg)
	{
		styles += `
		.player.char_${charid}{
			background: url('/sprites/${char.sprite}.png') no-repeat;
			background-size: 600%;
			background-position: ${-char.xr*CELL_SIZE}px ${-char.yr*CELL_SIZE}px;
		}
		.player.char_${charid}.left{
			background-position: ${-char.xl*CELL_SIZE}px ${-char.yl*CELL_SIZE}px;
		}
		`
		charid++
	}

	document.querySelector('style.custom').innerHTML = styles;
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
			let color = (x >= 0 && y >= 0 && x < W && y < H) ? `hsl(${landscape[x][y]} 40% 80%)` : 'transparent'
			let cls = '';
			let o = getObjectAtCoord(x,y);
			
			if(rx==hvc && ry==hvc)
				cls = 'player me char_'+player.char+' '+player.xdir
			else if(o)
			{
				if(o.type=='user')
					cls = 'player enemy char_'+o.char+' '+o.xdir
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
	hideMsg()
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
			let newpos;
			last_verified_stepnum = d.stepnum
			if(d.inventory)
			{
				//updInventory(d.inventory) - updated in api()
				if(d.objects_removed)
					removeObjects(d.objects_removed)

				newpos = d.pos
			}
			if(d.stepnum == STEPNUM && (pos[0] != d.pos[0] || pos[1] != d.pos[1]))
			{
				newpos = d.pos
			}

			if(d.xdir)
				player.xdir = d.xdir

			if(newpos)
			{
				pos = newpos
				player.x = pos[0]
				player.y = pos[1]
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
	
	if(dir[0])
		player.xdir = dir[0] < 0 ? "left" : "right"

	if(!getObjectAtCoord(p[0],p[1]))
	{
		pos = p
		drawMap(pos)
	}
}

function initInventory()
{
	document.onclick = ev => invHideMenu()
	h = ''
	for(let i=0; i < INVENTORY_SLOTS; i++)
	{
		h += `<div class="slot object" data-num="${i}" draggable="true"><div></div></div>`
	}
	document.querySelector(".inventory").innerHTML = h
	for(let slot of [...document.querySelectorAll(".inventory .slot")])
	{
		slot.onclick = ev => {
			ev.preventDefault()
			ev.stopPropagation()
			//useObject(slot)
			invShowMenu(slot)
		}
		slot.oncontextmenu = ev => {
			ev.preventDefault()
			cl('context menu')
			invShowMenu(slot)
		}
	}
}

async function useObject(slotnum)
{
	let res = await api('use_object',{player_id:PLAYER_ID, slotnum: +slotnum})
}

async function throwObject(slotnum)
{
	let res = await api('throw_object',{player_id:PLAYER_ID, slotnum: +slotnum})
}

function initWearing()
{
	h = ''
	for(let i=0; i < WEARING_SLOTS; i++)
	{
		h += `<div class="slot object" data-num="${i}"></div>`
	}
	document.querySelector(".wearing").innerHTML = h
}

function invShowMenu(slot_el)
{
	let slotnum = slot_el.dataset.num
	let slot = inventory[slotnum]
	cl({slot})
	if(slot.type=="empty")
	{
		popup_inv.hide()
		return
	}
	let obj = objcfg[slot["type"]]
	let el = mkDiv(`
	<div class="info">
		<div class="desc">${obj.desc}</div>
	</div>
	<a class="use">Использовать</a>
	<a class="throw">Выбросить</a>
	<a class="cancel">Отмена</a>
	`)

	el.querySelector('.use').onclick = () => {
		useObject(slotnum)
	}

	el.querySelector('.throw').onclick = () => {
		throwObject(slotnum)
	}

	let rect = slot_el.getBoundingClientRect()
	popup_inv.show(el,'',{
		left: (rect.x+rect.width+4)+'px',
		top: rect.y+'px'
	})
	
}

function invHideMenu()
{
	popup_inv.hide()
}

function updInventory(inv)
{
	inventory = inv
	let slots = [...document.querySelectorAll(".inventory > div")]
	for(let i=0; i < slots.length; i++)
	{
		if(!inv[i])
			break
		let cls = 'object '+inv[i].type
		if(inv[i].items && inv[i].items.length > 1)
		{
			cls += ' multi'
			slots[i].querySelector('div').innerHTML = inv[i].items.length
		}
			
		slots[i].className = cls
	}
}

function updWearing(inv)
{
	let slots = [...document.querySelectorAll(".wearing > div")]
	for(let i=0; i < slots.length; i++)
	{
		if(!inv[i])
			break
		let cls = 'object '+inv[i].item			
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
	initWearing()

	let res = await api("init_game",{board_id,player_id:PLAYER_ID})
	W = res.w
	H = res.h
	landscape = JSON.parse(res.landscape)
	pos = res.mycrd
	objects = res.objects
	player = res.player
	// res = await api("init_user")

	objcfg = res.objcfg
	charcfg = res.charcfg

	res = await api("timesync")
	timediff = res.time-Date.now()
	cl({timediff})

	initCss()


	popup_msg = new Popup('.message')
	popup_inv = new Popup('.inv_context')

	drawMap(pos)
	
}