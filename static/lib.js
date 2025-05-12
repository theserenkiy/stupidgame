const cl = console.log

async function base_api(cmd,data={})
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

function prepJson(v)
{
	return typeof v == 'string' ? JSON.parse(v) : v
}

function remClass(el,n)
{
	let rex = new RegExp("(\\s|^)"+n+"(?=\\s|$)",'g')
	cl({rex})
	el.className = el.className.replace(rex,' ').replace(/\s+/g,' ')
}

function delay(ms)
{
	return new Promise(s => setTimeout(s,ms))
}

function mkDiv(html)
{
	let el = document.createElement('DIV')
	el.innerHTML = html
	return el
}