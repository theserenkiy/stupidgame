import lib from './lib'

function getMap(id)
{
	return lib.getVar('maps/map'+id)
}


function generateUsers()
{
    let users = []
	for(let i=0; i < 100; i++)
	{
		users.push({
			id: Math.floor(Math.random()*1000000),
            name: lib.genCode(6),
            coord: [0,0],
            map: 0,
            hp: 100,
            
		})
	}
    lib.setVar('users',users)
}


export default {
	getMap,
	generateUsers
}