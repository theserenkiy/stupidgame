//import Nedb from 'nedb';
import fs from 'fs'

function initDB(dbfile){
    const db_ = new Nedb({filename: dbfile, autoload: true});
    db_.persistence.setAutocompactionInterval(5000);
    db_.persistence.compactDatafile()
    nedb_promisify(db_);
    return db_;
}

function nedb_promisify(db_){
    for(let n of ['insert', 'update', 'find', 'findOne'])
    {
        db_['a'+n] = (...args) => {
            return new Promise((resolve, reject) => {
                args.push((err, result) => {
                    //cl({err, result})
                    if (err) reject(err);
                    else resolve(result);
                })
                //cl({n,args,args_s: args.toString()})
                db_[n].call(db_,...args);
            })
        }
    };
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

function translit(s)
{
    let ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя';
    let direct = 'abcdefghijklmnopqrstuvwxyz0123456789-';
    let tr = 'a,b,v,g,d,e,yo,zh,z,i,y,k,l,m,n,o,p,r,s,t,u,f,kh,ts,ch,sh,sch,\',y,,e,yu,ya'.split(',');
    let sl = s.toLowerCase();
    let out = ''
    for(let i=0; i < sl.length; i++)
    {
        let n = ru.indexOf(sl[i])
        let c = n >= 0 ? tr[n] : (direct.indexOf(sl[i]) >= 0 ? sl[i] : '_');
        if(sl[i] != s[i])
            c = c[0].toUpperCase()+c.substring(1,c.length)
        out += c;
    }
    return out;
}

export default {
    initDB,
    genCode,
    delay,
    setVar,
    getVar,
    translit
}