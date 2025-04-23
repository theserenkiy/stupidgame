import fs from 'fs'

function genToken(len)
{
	let cc = 'abcdefghijklmnopqrstuvwxyz0123456789'.split('')
	let s = ''
	for(let i=0; i < len; i++)
	{
		let c = cc[Math.floor(Math.random()*cc.length)]
		s += Math.random() >= 0.5 ? c.toUpperCase() : c
	}
	return s;
}

function delay(ms)
{
    return new Promise(s => setTimeout(s, ms))
}


function getVarPath(name)
{
    return 'var/'+name+'.json';
}

function getVar(name,user=null)
{
    let path = getVarPath(name,user)
    if(!fs.existsSync(path))
        return null;
    let v = fs.readFileSync(path,'utf-8');
    try{
        return JSON.parse(v);
    }catch(e)
    {
        cl('Error parsing object '+name);
        return null;
    }
}


function setVar(name, value, user=null)
{
    fs.writeFileSync(getVarPath(name),JSON.stringify(value,null,'  '));
}

function genCode(len=4,use_uppercase=false,use_all_letters=false)
{
    let badwords = /sex|seks|secs|porn|[ei]b[laiueo]|h[uy][yi]|x[uy][ui]|pi[zs]|popa|go[vw]n|blya|pid[oa]?|f[au][ck]{1,2}|ped[oi]|[kc]al|[kg]ondo|mud|g[ae][iy]/i
    let c = use_all_letters ? ['bcdfghjklmnpqrstvwxz','aeiouy'] : ['bcdfgklmnprstvxz','aeiou']
    if(use_uppercase)
        c = c.map(v => v+v.toUpperCase())
    let r = c => c[Math.floor(Math.random()*c.length)]
    let types = [[0,1],[1,0],[0,1,0],[1,0,1]]
    while(1)
    {
        let pattern = []
        for(let i=0;;i++)
        {
            let p = []
            //avoiding double consonants
            while(1)
            {
                p = types[Math.floor(Math.random()*4)];
                if(!pattern.length || p[0] || pattern[pattern.length-1])
                    break
            }
            pattern.push(...p);
            if(pattern.length >= len-1)
                break;
        }
        let lastsym = '',sym;
        let res = ''
        for(let t of pattern)
        {
            while(1)
            {
                sym = r(c[t])
                if(sym != lastsym)
                    break
            }
            res += sym
            lastsym = sym
        }
        let m;
        if(m = badwords.exec(res))
        {
            // console.log('TEST FAILED: ',m[0])
            continue;
        }
        return res;
    }
}

export default {
	genToken,
    getVar,
    setVar,
    genCode
}